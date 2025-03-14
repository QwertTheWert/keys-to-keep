from flask import Blueprint, render_template, redirect, url_for

register_bp = Blueprint("register", __name__, template_folder="templates")

def register_to_app(flask_app):
	from app import db, request
	from models import User

	@register_bp.route('/register', methods=["GET", "POST"])
	def register():
		message = ""
		f_nm = request.form.get("full_name")
		usrnm = request.form.get("username")
		eml = request.form.get("email")
		pwd = request.form.get("password")
		bk_nbr = request.form.get("bank_number")
		result = db.session.execute(db.select(User).filter_by(username=usrnm))
		if request.method == "POST" and f_nm and usrnm and eml and pwd and bk_nbr:
			if result.first() is None:
				new_user = User(full_name=f_nm, username=usrnm, email=eml, password=pwd, bank_number=bk_nbr)
				db.session.add(new_user)
				db.session.commit()
				return redirect(url_for("register.index"))
			else:
				message = "Username is taken. Please use another one."
		elif request.method == "POST":
			message = "Incomplete registration data. Please fill all fields." 
		return render_template('register/register.html', message=message, full_name=f_nm, username=usrnm, email=eml, password=pwd, bank_number=bk_nbr)


	@register_bp.route('/')
	def index():
		return render_template("main_page.html")

	@register_bp.route('/login')
	def login():
		return render_template("login.html")


	flask_app.register_blueprint(register_bp)


