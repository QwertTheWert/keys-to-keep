from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db, format_money
from models import Review, Keyboard


class ReviewPage: 
	def __init__(self, flask_app, bcrypt):
		review_bp = Blueprint("review", __name__, template_folder="templates", static_folder="static", static_url_path="/review/static")

		@review_bp.route('/review/<int:review_id>', methods=["POST", "GET"])
		def review(review_id):
			if request.method == "GET":
				data = Review.get_edit_data(review_id)
				if data[0].rating == -1:
					return render_template("review.html", data=data, price=format_money(data[1].get_discounted_price()))
				else:
					return redirect(url_for('profile.profile'))
			elif request.method == "POST":
				review = Review.get_edit_data(review_id)[0]
				review.rating = int(request.form.get("selected_rating"))
				review.description = request.form.get("description", "")
				db.session.commit()
				return redirect(url_for('profile.profile'))

		flask_app.register_blueprint(review_bp)
