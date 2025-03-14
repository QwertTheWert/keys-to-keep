from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

login_bp = Blueprint("login", __name__, template_folder="templates")

def register_to_app(flask_app):
	from app import db, request
	from models import User
	
	@login_bp.route('/login', methods=["GET", "POST"])
	def login():
		message = ""
		idntf = request.form.get("identifier")
		pwd = request.form.get("password")
		user_by_username = db.session.execute(db.select(User).filter_by(username=idntf)).scalar_one_or_none()
		user_by_email = db.session.execute(db.select(User).filter_by(email=idntf)).scalar_one_or_none()
		login_successfully = False
		if request.method == "POST" and idntf and pwd:
			if user_by_username is not None:
				login_user(user_by_username)
				login_successfully = True
			elif user_by_email:
				login_user(user_by_username)
				login_successfully = True	
			
			if login_successfully:
				# message = f"Successfully logged in as {user_by_username.username}"
				return redirect(url_for("register.index"))
			else:
				message = "No username."
			
		elif request.method == "POST":
			message = "Please fill all fields."
		return render_template('login.html', message=message, identifier=idntf, password=pwd)
	

	flask_app.register_blueprint(login_bp)


