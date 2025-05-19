from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import current_user
from app import db, request
from models import User

class ComparePage:
	compare_bp = Blueprint("compare", __name__, template_folder="templates", static_folder="static", static_url_path="/compare/static/")
	
	def __init__(self, flask_app, bcrypt):
		@self.compare_bp.route('/compare')
		def compare():

			return render_template("compare.html")


		flask_app.register_blueprint(self.compare_bp)