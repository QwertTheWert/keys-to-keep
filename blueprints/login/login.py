from flask import Blueprint, render_template, redirect, url_for

login_bp = Blueprint("register", __name__, template_folder="templates")

def register_to_app(flask_app):
	from app import db, request
	from models import User
	
	@login_bp.route('/login')
	def login():
		message = ""
		idntf = request.form.get("identifier")
		pwd = request.form.get("password")
		username_row = db.session.execute(db.select(User).filter_by(username=idntf))
		email_row = db.session.execute(db.select(User).filter_by(email=idntf))
		
		if request.method == "POST" and idntf and pwd:
			if result.first() is None:
				# new_user = User(full_name=f_nm, username=usrnm, email=eml, password=pwd, bank_number=bk_nbr)
				# db.session.add(new_user)
				# db.session.commit()
				return redirect(url_for("register.index"))
			else:
				message = "Username is taken. Please use another one."
		elif request.method == "POST":
			message = "Please fill all fields."
		return render_template('login.html', message=message, identifier=idntf, password=pwd)
	


	flask_app.register_blueprint(login_bp)


