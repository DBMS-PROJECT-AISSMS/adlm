from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import bcrypt
from app.database import execute_query

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username, email, password = data.get("username"), data.get("email"), data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    query = "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)"
    execute_query(query, (username, email, hashed_password))

    return jsonify({"message": "User registered successfully"}), 201

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email, password = data.get("email"), data.get("password")

    query = "SELECT user_id, password_hash FROM Users WHERE email = %s"
    user = execute_query(query, (email,), fetch_one=True)

    if not user or not bcrypt.check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=user["user_id"])
    return jsonify({"message": "Login successful", "token": token}), 200
