
class Search:
	def __init__(self, flask_app, bcrypt):
		from flask import Blueprint, render_template, redirect, url_for, request
		from flask_login import current_user
		from app import db, request
		from models import User
		
		search_bp = Blueprint("search", __name__, template_folder="templates", static_folder="static", static_url_path="/search/static/")

		@search_bp.route('/search')
		def search():
			# return request.args
			return render_template("search.html")

		flask_app.register_blueprint(search_bp)


