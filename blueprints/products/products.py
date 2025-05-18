from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from app import db, request

class Products:
	products_bp = Blueprint("products", __name__, template_folder="templates", static_folder="static", static_url_path="/showcase/static/")
	
	def __init__(self, flask_app, bcrypt):		
		from models import Keyboard, Color, Switch

		@self.products_bp.route('/keyboards')
		def keyboards():
			return render_template("keyboards.html", keyboard_data=Keyboard.get_data_all())
		
		@self.products_bp.route('/keyboards/add_to_cart', methods=['POST'])
		def get_variants():
			keyboard = Keyboard.get_by_id(request.get_json()["keyboard_id"])
			return jsonify({'colors': keyboard.get_variants(Color), 'switches' : keyboard.get_variants(Switch)})

		@self.products_bp.route('/keyboards/add_to_cart', methods=['POST'])
		def add_to_cart():
			keyboard = Keyboard.get_by_id(request.get_json()["keyboard_id"])
			current_user.add_to_cart(keyboard)
			return jsonify({'keyboard_name': keyboard.name})
		
		@self.products_bp.route('/accessories')
		def accessories():
			return render_template("keyboards.html")
		
		@self.products_bp.route('/products_details')
		def products_details():
			# Mock data for testing
			product = {
				"name": "Mechanical Keyboard",
				"subtitle": "RGB Backlit, Hot-Swappable",
				"price_discounted": 750000,
				"price_original": 1000000,
				"discount_percent": 25,
				"image_url": "/static/sample_image.jpg",
				"colors": ["Hitam", "Putih"],
				"switches": ["Blue", "Red", "Brown"],
				"estimated_delivery": 3,
				"specifications": [
					{"name": "Switch Type", "value": "Hot-Swappable"},
					{"name": "Keycaps", "value": "PBT Double-Shot"},
				],
				"rating": 4.5,
				"review_count": 120,
				"reviews": [
					{"name": "John Doe", "stars": 5, "text": "Produk sangat bagus!"},
					{"name": "Jane Smith", "stars": 4, "text": "Kualitas oke, pengiriman cepat."},
				],
			}
			return render_template("products_details.html", product=product)

		flask_app.register_blueprint(self.products_bp)