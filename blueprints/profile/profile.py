from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user, current_user

profile_bp = Blueprint("profile", __name__, template_folder="templates", static_folder="static")

def register_to_app(flask_app, bcrypt):
	from app import db, request
	from models import User
	

	@profile_bp.route('/profile')
	def profile():
		if current_user.is_authenticated:
			return render_template("profile.html", username=str(current_user.username), full_name=str(current_user.full_name), email=str(current_user.email))
		else:
			return redirect(url_for("login.login"))

	@profile_bp.route('/profile/edit', methods=["GET", "POST"])
	def edit():
		if request.method == "POST":
			current_user.full_name = request.form.get("full_name")
			current_user.email = request.form.get("email")
			current_user.bank_number = request.form.get("bank_number")
			db.session.commit()
			return redirect(url_for("profile.profile"))
		else:
			return render_template("edit_profile.html", full_name=str(current_user.full_name), email=str(current_user.email), bank_number=str(current_user.bank_number))


	@profile_bp.route('/profile/logout')
	def logout():
		logout_user()
		return redirect(url_for("login.login"))


	flask_app.register_blueprint(profile_bp)


