from flask import Blueprint, request, jsonify
from app.database import execute_query

ai_admin = Blueprint("ai_admin", __name__)

@ai_admin.route("/ai/logs", methods=["POST"])
def log_ai_response():
    data = request.get_json()
    query = "INSERT INTO AIAdminLogs (query_text, response_text) VALUES (%s, %s)"
    execute_query(query, (data.get("query"), data.get("response")))

    return jsonify({"message": "AI response logged"}), 201