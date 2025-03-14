from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

register_bp = Blueprint("register", __name__, template_folder="templates")

def register_to_app(flask_app, bcrypt):
	from app import db, request
	from models import User
	
	@register_bp.route('/register', methods=["GET", "POST"])
	@register_bp.route('/register/', methods=["GET", "POST"])
	def register():
		message = ""
		full_name = request.form.get("full_name")
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
		bank_number = request.form.get("bank_number")
		hashed_password = bcrypt.generate_password_hash(password) if password else ""
		select_by_username = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
		select_by_email = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
		if request.method == "POST":
			if select_by_username is None and select_by_email is None:
				new_user = User(full_name=full_name, username=username, email=email, password=hashed_password, bank_number=bank_number)
				db.session.add(new_user)
				db.session.commit()				
				return redirect(url_for("register.index"))
			elif select_by_username is not None:
				message = "Username is taken. Please use another one."
			elif select_by_email is not None:
				message = "Username is taken. Please use another one."
		return render_template('register.html', message=message, full_name=full_name, username=username, email=email, password=password, bank_number=bank_number)


	@register_bp.route('/')
	def index():
		if current_user.is_authenticated:
			print(str(current_user.username))
		else:
			print("No user")

		return render_template("main_page.html")

	flask_app.register_blueprint(register_bp)


