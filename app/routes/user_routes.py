from flask import Blueprint, request, jsonify
from app.constants.http_status_codes import SUCCESS_CODE
# Blueprint for user routes

users_bp = Blueprint('users_bp', __name__)
