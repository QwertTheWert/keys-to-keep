from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app import db, request

class Products:
	def __init__(self, flask_app, bcrypt):		
		products_bp = Blueprint("products", __name__, template_folder="templates", static_folder="static", static_url_path="/showcase/static/")

		@products_bp.route('/keyboards')
		def keyboards():
			return render_template("keyboards.html")
		
		@products_bp.route('/accessories')
		def accessories():
			return render_template("keyboards.html")



		flask_app.register_blueprint(products_bp)