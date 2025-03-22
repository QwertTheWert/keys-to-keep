from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, current_user
from app import db, request
from models import User

class Login:
	login_bp = Blueprint("login", __name__, template_folder="templates", static_folder="static")

	def __init__(self, flask_app, bcrypt):
		@self.login_bp.route('/login', methods=["GET", "POST"])
		def login():
			message = ""
			login_successfully = False
			if request.method == "POST":
				identifier = request.form.get("identifier")
				password = request.form.get("password")
				if self.validate_login(identifier, password, bcrypt):
					return redirect(url_for("register.index"))
				else:
					message = "Invalid username or password."		
			return render_template('login.html', message=message)
		

		flask_app.register_blueprint(self.login_bp)

	def validate_login(self, identifier, password, bcrypt):
		user = (User.query.filter(User.email == identifier) if "@" in identifier else User.query.filter(User.username == identifier)).first()
		if user is not None:
			if bcrypt.check_password_hash(user.password, password):
				login_user(user)
				return True
		return False
