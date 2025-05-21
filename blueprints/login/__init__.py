from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user
from app import request
from models import User

class LoginPage:
	
	login_bp = Blueprint("login", __name__, template_folder="templates", static_folder="static", static_url_path="/login/static/")

	def __init__(self, flask_app, bcrypt):
		@self.login_bp.route('/login', methods=["GET", "POST"])
		def login():
			message = ""
			if request.method == "POST":
				identifier = request.form.get("identifier")
				password = request.form.get("password")
				if self.validate_login(identifier, password, bcrypt):
					return redirect(url_for("main_page.main_page"))
				else:
					message = "Invalid username or password."		
			return render_template('login.html', message=message)
		

		flask_app.register_blueprint(self.login_bp)

	def validate_login(self, identifier, password, bcrypt):
		user = (User.get_by_email(identifier) if "@" in identifier else User.get_by_username(identifier))
		if user is not None:
			if bcrypt.check_password_hash(user.password, password):
				login_user(user)
				return True
		return False
