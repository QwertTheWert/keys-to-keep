from flask import Blueprint, render_template, request, jsonify
from app import db, request

class ComparePage:
	compare_bp = Blueprint("compare", __name__, template_folder="templates", static_folder="static", static_url_path="/compare/static/")
	
	def __init__(self, flask_app, bcrypt):
		from models import Keyboard

		@self.compare_bp.route('/compare')
		def compare():
			
			return render_template("compare.html")

		@self.compare_bp.route('/compare/get_data', methods=["POST"])
		def get_data():
			data = request.get_json()
			keyboard = Keyboard.get_by_id(data["id"])
			if keyboard:
				return jsonify({"valid": True, "keyboard_data" : keyboard.get_data()})
			else:
				return jsonify({"valid": False})

		flask_app.register_blueprint(self.compare_bp)