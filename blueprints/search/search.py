from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

search_bp = Blueprint("search", __name__, template_folder="templates", static_folder="static")

def register_to_app(flask_app, bcrypt):
	from app import db, request
	from models import User

	@search_bp.route('/search')
	@search_bp.route('/search/')
	def search():
		return render_template("search.html")


	flask_app.register_blueprint(search_bp)


