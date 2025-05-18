from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app import db, request, format_money
from models import Keyboard, Switch, Color

class KeyboardPage: 
	keyboard_bp = Blueprint("keyboard", __name__, template_folder="templates", static_folder="static", static_url_path="/keyboard/static/")
	
	def __init__(self, flask_app, bcrypt):
		from models import Keyboard, Switch, Color

		@self.keyboard_bp.route('/keyboard/<int:keyboard_id>')
		def keyboard_details(keyboard_id):
			keyboard = Keyboard.get_by_id(keyboard_id)
			data = keyboard.get_data()
			return render_template("keyboard.html", data=data)
		flask_app.register_blueprint(self.keyboard_bp)