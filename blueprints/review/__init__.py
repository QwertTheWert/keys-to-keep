from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from models import Review, Keyboard


class ReviewPage: 
    def __init__(self, flask_app, bcrypt):
        review_bp = Blueprint("review", __name__, template_folder="templates", static_folder="static", static_url_path="/review/static")

        @review_bp.route('/review/<int:keyboard_id>', methods=["GET"])
        def review(keyboard_id):
            keyboard = Keyboard.query.get_or_404(keyboard_id)
            reviews = Review.query.filter_by(keyboard_id=keyboard_id).all()
            return render_template("review.html", data=(keyboard_id, keyboard), reviews=reviews)

        @review_bp.route('/review/<int:review_id>', methods=["POST"])
        @login_required
        def submit_review(review_id):
            try:
                keyboard_id = int(request.form.get("keyboard_id"))
                rating = int(request.form.get("selected_rating"))
                description = request.form.get("description", "")

                # You may also want to check if the user already submitted a review, and update instead.
                new_review = Review(
                    user_id=current_user.id,
                    keyboard_id=keyboard_id,
                    rating=rating,
                    description=description
                )
                db.session.add(new_review)
                db.session.commit()
                flash("Review submitted successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Failed to submit review: {str(e)}", "danger")

            return redirect(url_for('profile.profile', keyboard_id=keyboard_id))

        flask_app.register_blueprint(review_bp)
