from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app import db, request, format_money

class Products:
	def __init__(self, flask_app, bcrypt):		
		from models import Keyboard
		products_bp = Blueprint("products", __name__, template_folder="templates", static_folder="static", static_url_path="/showcase/static/")

		@products_bp.route('/keyboards')
		def keyboards():
			keyboards = db.session.query(Keyboard).all()
			data = []
			for keyboard in keyboards:
				data.append({
					"keyboard" : keyboard,
					"price" : format_money(keyboard.price),
					"discounted_price": format_money(keyboard.get_discounted_price()),
				})
			print(data)
			return render_template("keyboards.html", keyboard_data=data)
		
		@products_bp.route('/accessories')
		def accessories():
			return render_template("keyboards.html")
		
		@products_bp.route('/products_details')
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

		flask_app.register_blueprint(products_bp)