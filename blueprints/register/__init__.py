from app import db, request, add_and_commit
from flask_login import login_user, current_user
from flask import Blueprint, render_template, redirect, url_for
from models import User 
from models import Keyboard, Cart

class Register:
	
	register_bp = Blueprint("register", __name__, template_folder="templates", static_folder="static", static_url_path="/register/static/")
	
	def __init__(self, flask_app, bcrypt):
		
		@self.register_bp.route('/register', methods=["GET", "POST"])
		def register():
			message = ""
			full_name = request.form.get("full_name")
			username = request.form.get("username")
			email = request.form.get("email")
			password = request.form.get("password")
			address = request.form.get("address")
			hashed_password = bcrypt.generate_password_hash(password) if password else ""
			if request.method == "POST":
				validation_results = self.validate_data(username, email)
				if validation_results["valid"]:
					self.create_user(full_name, username, email, hashed_password, address)
					return redirect(url_for("main_page.main_page"))
				else:
					message = validation_results["reason"]
			return render_template('register.html', message=message, full_name=full_name, username=username, email=email, password=password, address=address)

		flask_app.register_blueprint(self.register_bp)
	
	

	
	def validate_data(self, username, email):
		select_by_username = User.get_by_username(username)
		select_by_email = User.get_by_email(email)
		return_json = { "valid": False, "reason": "" }
		return_json["valid"] = select_by_username is None and select_by_email is None
		if not return_json["valid"]:
			return_json["reason"] = "Username is taken. Please use another one." if select_by_username is not None else "Email is taken. Please use another one."
		return return_json

	def create_user(self, full_name, username, email, password, address):
		new_user = User(full_name=full_name, username=username, email=email, password=password, address=address)
		add_and_commit(new_user)
		login_user(new_user)