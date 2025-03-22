class Showcase:
	def __init__(self, flask_app, bcrypt):
		from flask import Blueprint, render_template, redirect, url_for, request
		from flask_login import current_user
		from app import db, request
		from models import User
		
		showcase_bp = Blueprint("showcase", __name__, template_folder="templates", static_folder="static")

		@showcase_bp.route('/showcase')
		def search():
			return render_template("showcase.html")


		flask_app.register_blueprint(showcase_bp)