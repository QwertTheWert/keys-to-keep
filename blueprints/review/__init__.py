from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from app import request

class ReviewPage: 
	
	def __init__(self, flask_app, bcrypt):
		from models import Review
		review_bp = Blueprint("review", __name__, template_folder="templates", static_folder="static", static_url_path="/keyboard/static/")

		@review_bp.route('/review/<int:review_id>', methods=["GET", "POST"])
		def review(review_id):
			if request.method == "GET":
				return render_template("review.html", data=Review.get_edit_data(review_id))

		
		flask_app.register_blueprint(review_bp)
