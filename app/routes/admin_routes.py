from flask import Blueprint, request, jsonify, render_template
from app.constants.http_status_codes import SUCCESS_CODE
# Blueprint for user routes
import os
admins_bp = Blueprint('admins_bp', __name__)

@admins_bp.route('/', methods=['GET'])
@admins_bp.route('/home', methods=['GET'])
@admins_bp.route('/dashboard', methods=['GET'])
def home_page():
    return render_template('admin_templates/dashboard.html'), SUCCESS_CODE

@admins_bp.route('/add/long-text')
def add_long_text():
    return render_template('admin_templates/add_long_text.html'), SUCCESS_CODE

@admins_bp.route('/add/bot')
def add_bot():
    return render_template('admin_templates/new_bot.html'), SUCCESS_CODE