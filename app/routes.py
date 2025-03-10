from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.database import execute_query
from app import bcrypt

routes = Blueprint("routes", __name__)

# Home Route
@routes.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to Digital Legacy Management API"}), 200

# Register User
@routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username, email, password = data.get("username"), data.get("email"), data.get("password")
    role = data.get("role", "user")  # Default role is 'user'

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    # Check if email already exists
    existing_user = execute_query("SELECT email FROM Users WHERE email = %s", (email,), fetch_one=True)
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    
    query = "INSERT INTO Users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)"
    execute_query(query, (username, email, hashed_password, role))

    if role == 'admin':
        return jsonify({"message": f"Admin {username} registered successfully"}), 201
    else:
        return jsonify({"message": f"User  {username} registered successfully"}), 201

# Login User
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    query = "SELECT user_id, password_hash, username, role FROM Users WHERE email = %s"
    result = execute_query(query, (email,), fetch_one=True)

    if not result:
        return jsonify({"error": "Invalid email or password"}), 401

    user_id, hashed_password, username, role = result["user_id"], result["password_hash"], result["username"], result["role"]

    if not bcrypt.check_password_hash(hashed_password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user_id))
    
    return jsonify({"message": f"{username} logged in successfully", "access_token": access_token}), 200

# Get Logged-in User
@routes.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()

    query = "SELECT user_id, username, email, role FROM Users WHERE user_id = %s"
    result = execute_query(query, (user_id,), fetch_one=True)

    if not result:
        return jsonify({"error": "User  not found"}), 404

    return jsonify({"user": result}), 200

# Add Digital Asset
@routes.route("/assets", methods=["POST"])
@jwt_required()
def add_asset():
    user_id = get_jwt_identity()
    data = request.get_json()

    valid_asset_types = {"document", "image", "video", "social_media", "finance", "business", "other"}
    asset_type = data.get("asset_type")

    if asset_type not in valid_asset_types:
        return jsonify({"error": "Invalid asset type"}), 400

    is_encrypted = 1 if data.get("is_encrypted", False) else 0

    query = """
        INSERT INTO DigitalAssets (owner_id, asset_name, asset_type, asset_url, is_encrypted)
        VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(query, (user_id, data["asset_name"], asset_type, data["asset_url"], is_encrypted))

    return jsonify({"message": "Asset added"}), 201

# Modify Digital Asset
@routes.route("/assets/<int:asset_id>", methods=["PUT"])
@jwt_required()
def modify_asset(asset_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    query = """
        UPDATE DigitalAssets 
        SET asset_name = %s, asset_type = %s, asset_url = %s, is_encrypted = %s 
        WHERE asset_id = %s AND owner_id = %s
    """
    is_encrypted = 1 if data.get("is_encrypted", False) else 0
    execute_query(query, (data["asset_name"], data["asset_type"], data["asset_url"], is_encrypted, asset_id, user_id))

    return jsonify({"message": "Asset updated"}), 200

# Delete Digital Asset
@routes.route("/assets/<int:asset_id>", methods=["DELETE"])
@jwt_required()
def delete_asset(asset_id):
    user_id = get_jwt_identity()

    query = "DELETE FROM DigitalAssets WHERE asset_id = %s AND owner_id = %s"
    result = execute_query(query, (asset_id, user_id))

    if result.rowcount == 0:
        return jsonify({"error": "Asset not found or not owned by user"}), 404

    return jsonify({"message": "Asset deleted"}), 200

# View All Digital Assets
@routes.route("/assets", methods=["GET"])
@jwt_required()
def view_assets():
    user_id = get_jwt_identity()

    query = """
        SELECT asset_id, asset_name, asset_type, asset_url, is_encrypted 
        FROM DigitalAssets WHERE owner_id = %s
    """
    assets = execute_query(query, (user_id,), fetch_all=True)

    return jsonify({"assets": assets}), 200

# Add Beneficiary
@routes.route("/beneficiaries", methods=["POST"])
@jwt_required()
def add_beneficiary():
    user_id = get_jwt_identity()
    data = request.get_json()

    query = "INSERT INTO Beneficiaries (user_id, name, relationship, email) VALUES (%s, %s, %s, %s)"
    execute_query(query, (user_id, data["name"], data["relationship"], data["email"]))

    return jsonify({"message": "Beneficiary added"}), 201

# View Beneficiaries
@routes.route("/beneficiaries", methods=["GET"])
@jwt_required()
def get_beneficiaries():
    user_id = get_jwt_identity()

    query = "SELECT beneficiary_id, name, relationship, email FROM Beneficiaries WHERE user_id = %s"
    beneficiaries = execute_query(query, (user_id,), fetch_all=True)

    return jsonify({"beneficiaries": beneficiaries}), 200

# Verify Death by Admin
@routes.route("/admin/verify_death/<int:user_id>", methods=["POST"])
@jwt_required()
def admin_verify_death(user_id):
    admin_id = get_jwt_identity()  # Get the admin's user ID

    # Check if the admin has the right role
    admin_check = execute_query("SELECT role FROM Users WHERE user_id = %s", (admin_id,), fetch_one=True)
    if not admin_check or admin_check['role'] != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    # Mark the user as deceased
    update_user = "UPDATE Users SET is_deceased = TRUE WHERE user_id = %s"
    execute_query(update_user, (user_id,))

    return jsonify({"message": "User  marked as deceased."}), 200

# Transfer Assets to Beneficiaries
@routes.route("/admin/transfer_assets", methods=["POST"])
@jwt_required()
def admin_transfer_assets():
    admin_id = get_jwt_identity()
    data = request.get_json()

    user_id = data.get("user_id")
    beneficiary_id = data.get("beneficiary_id")
    asset_id = data.get("asset_id")

    # Check if the user is deceased
    user_check = execute_query("SELECT is_deceased FROM Users WHERE user_id = %s", (user_id,), fetch_one=True)
    if not user_check or not user_check['is_deceased']:
        return jsonify({"error": "User  is not marked as deceased."}), 400

    # Transfer the asset
    transfer_query = """
        INSERT INTO AssetTransfers (asset_id, previous_owner_id, new_owner_id)
        VALUES (%s, %s, %s)
    """
    execute_query(transfer_query, (asset_id, user_id, beneficiary_id))

    return jsonify({"message": "Asset successfully transferred to beneficiary."}), 201