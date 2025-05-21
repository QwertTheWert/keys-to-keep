from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from app import request

class CompletePage:
	complete_bp = Blueprint("complete", __name__, template_folder="templates", static_folder="static", static_url_path="/complete/static/")

	def __init__(self, flask_app, bcrypt):
		from models import Transaction

		@self.complete_bp.route('/complete/', methods=['POST'])
		def complete():
			transaction_id = request.form.get("transaction_id")
			data = Transaction.get_data(transaction_id) # Review / Keyboard / Color / Switch 			
			return render_template('complete.html', data=data)
		
		flask_app.register_blueprint(self.complete_bp)
