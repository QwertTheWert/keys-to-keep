from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from app import db, request
from models import User

class Cart:
	
	cart_bp = Blueprint("cart", __name__, template_folder="templates", static_folder="static")

	def __init__(self, flask_app, bcrypt):
		@self.cart_bp.route('/cart')		
		def cart():
			from models import Cart, ProductModel
			cart_data = []
			carts = db.session.query(Cart).filter(Cart.user_id == current_user.id).all()
			for cart in carts:
				product_model = db.session.query(ProductModel).filter(ProductModel.id == cart.product_model_id).first()
				cart_data.append({
					"product_model" : product_model,
					"cart" : cart,
					"price" : '{:,}'.format(product_model.price).replace(',', '.')
				})
			return render_template("cart.html", cart_data=cart_data)

		
		flask_app.register_blueprint(self.cart_bp)