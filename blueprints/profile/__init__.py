from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user, current_user
from app import db, request
from models import User

class ProfilePage:
	profile_bp = Blueprint("profile", __name__, template_folder="templates", static_folder="static", static_url_path="/profile/static/")

	def __init__(self, flask_app, bcrypt):

		@self.profile_bp.route('/profile', methods=["GET", "POST"])
		def profile():
			if current_user.is_authenticated:
				return render_template("profile.html", user=current_user, username=str(current_user.username), full_name=str(current_user.full_name), email=str(current_user.email))
			else:
				return redirect(url_for("login.login"))

		@self.profile_bp.route('/profile/edit', methods=["GET", "POST"])
		def edit():
			if request.method == "POST":
				current_user.update(request.form.get("full_name"), request.form.get("email"), request.form.get("bank_number"))
				return redirect(url_for("profile.profile"))
			else:
				return render_template("edit_profile.html", user=current_user, full_name=str(current_user.full_name), email=str(current_user.email), bank_number=str(current_user.bank_number))


		@self.profile_bp.route('/profile/logout')
		def logout():
			logout_user()
			return redirect(url_for("login.login"))
		
		@self.profile_bp.route('/profile/delete')
		def delete():
			user_to_delete = User.query.filter(User.id == current_user.id).first()
			logout_user()
			user_to_delete.delete()
			return redirect(url_for("main_page.main_page"))


		flask_app.register_blueprint(self.profile_bp)


