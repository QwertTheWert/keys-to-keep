from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from app import request

class CompletePage:
	complete_bp = Blueprint("complete", __name__, template_folder="templates", static_folder="static", static_url_path="/complete/static/")

	def __init__(self, flask_app, bcrypt):

		@self.complete_bp.route('/complete/<cart>', methods=['POST'])
		def complete(cart):
			return "Test"
		
		flask_app.register_blueprint(self.complete_bp)
