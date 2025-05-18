from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app import db, request, format_money
from models import Keyboard

class KeyboardPage: 
	keyboard_bp = Blueprint("keyboard", __name__, template_folder="templates", static_folder="static", static_url_path="/keyboard/static/")
	
	def __init__(self, flask_app, bcrypt):
		from models import Keyboard

		@self.keyboard_bp.route('/keyboard/<int:keyboard_id>')
		def keyboard_details(keyboard_id):
			keyboard = Keyboard.get_by_id(keyboard_id)
			data = {
				"keyboard" : keyboard,
				"reviews" : keyboard.get_reviews(),
				"price" : format_money(keyboard.price),
				"discounted_price" : format_money(keyboard.get_discounted_price()),
			}
			return render_template("keyboard_details.html", data=data)

		flask_app.register_blueprint(self.keyboard_bp)