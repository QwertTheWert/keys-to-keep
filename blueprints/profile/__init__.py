from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user, current_user
from app import db, request
from models import User

class ProfilePage:

	def __init__(self, flask_app, bcrypt):
		profile_bp = Blueprint("profile", __name__, template_folder="templates", static_folder="static", static_url_path="/profile/static/")

		@profile_bp.route('/profile')
		def profile():
			if current_user.is_authenticated:
				review_data = current_user.get_reviews()
				return render_template("profile.html", user=current_user, username=str(current_user.username), full_name=str(current_user.full_name), address=str(current_user.full_name), email=str(current_user.email), review_data=review_data)
			else:
				return redirect(url_for("login.login"))

		@profile_bp.route('/profile/edit', methods=["GET", "POST"])
		def edit():
			if current_user.is_authenticated:
				if request.method == "POST":
					full_name = request.form.get("full_name")
					email = request.form.get("email")
					address = request.form.get("address")
					print(full_name, email, address)
					if full_name != "" and email != "" and address != "":
						current_user.update(full_name, email, address)
						return redirect(url_for("profile.profile"))
					else:
						return render_template("edit_profile.html", user=current_user, full_name=str(full_name), email=str(email), address=str(address))
				else:
					return render_template("edit_profile.html", user=current_user, full_name=str(current_user.full_name), email=str(current_user.email), address=str(current_user.address))
			else:
				return redirect(url_for("login.login"))

		@profile_bp.route('/profile/logout')
		def logout():
			logout_user()
			return redirect(url_for("login.login"))
		
		@profile_bp.route('/profile/delete')
		def delete():
			user_to_delete = User.query.filter(User.id == current_user.id).first()
			logout_user()
			user_to_delete.delete()
			return redirect(url_for("main_page.main_page"))


		flask_app.register_blueprint(profile_bp)


