from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database import execute_query

asset = Blueprint("asset", __name__)

@asset.route("/assets", methods=["GET"])
@jwt_required()
def get_assets():
    user_id = get_jwt_identity()
    query = "SELECT * FROM DigitalAssets WHERE user_id = %s"
    assets = execute_query(query, (user_id,), fetch_all=True)
    return jsonify(assets), 200
