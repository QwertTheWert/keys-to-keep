from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from app import request

class KeyboardPage: 
	keyboard_bp = Blueprint("keyboard", __name__, template_folder="templates", static_folder="static", static_url_path="/keyboard/static/")
	
	def __init__(self, flask_app, bcrypt):
		from models import Keyboard, User

		@self.keyboard_bp.route('/keyboard/<int:keyboard_id>')
		def keyboard_details(keyboard_id):
			keyboard = Keyboard.get_by_id(keyboard_id)
			data = keyboard.get_data()
			return render_template("keyboard.html", data=data)

		@self.keyboard_bp.route('/keyboard/add_to_cart', methods=['POST'])
		def add_to_cart():
			if current_user.is_authenticated:
				data = request.get_json()
				keyboard_id = int(data["keyboard_id"])
				keyboard = Keyboard.get_by_id(keyboard_id)
				color_id = int(data["variant_info"]["color"])
				switch_id = int(data["variant_info"]["switch"])
				current_user.add_to_cart(keyboard, color_id, switch_id, int(data["quantity"]))
				return jsonify({"success" : True})
			else:
				return jsonify({"success" : False})

		flask_app.register_blueprint(self.keyboard_bp)