from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from app import request

class MarketplacePage:
	
	def __init__(self, flask_app, bcrypt):		
		from models import Keyboard, Color, Switch
		marketplace_bp = Blueprint("marketplace", __name__, template_folder="templates", static_folder="static", static_url_path="/showcase/static/")

		@marketplace_bp.route('/marketplace')
		def marketplace():
			is_ascending = request.args.get("asc", "true") == "true"
			is_compare = request.args.get("compare", "false")
			return render_template("marketplace.html", 
                         keyboard_data=Keyboard.get_data_all(is_ascending),
                         request=request)
		
		@marketplace_bp.route('/marketplace/get_variants', methods=['POST'])
		def get_variants():
			if current_user.is_authenticated:
				data = request.get_json()
				keyboard_id = int(data["keyboard_id"])
				keyboard = Keyboard.get_by_id(keyboard_id)
				colors = [color.to_dict() for color in keyboard.get_variants(Color)]
				switches = [switch.to_dict() for switch in keyboard.get_variants(Switch)]
				return jsonify({'success' : True, 'colors': colors, 'switches' : switches})
			else:
				return jsonify({'success' : False})

		@marketplace_bp.route('/marketplace/add_to_cart', methods=['POST'])
		def add_to_cart():
			data = request.get_json()
			keyboard_id = int(data["keyboard_id"])
			keyboard = Keyboard.get_by_id(keyboard_id)
			color_id = int(data["variant_info"]["color"])
			switch_id = int(data["variant_info"]["switch"])
			current_user.add_to_cart(keyboard, color_id, switch_id, 1)
			return jsonify({'keyboard_name': keyboard.name})
				
		@marketplace_bp.route('/accessories')
		def accessories():
			return render_template("marketplace.html")

		flask_app.register_blueprint(marketplace_bp)