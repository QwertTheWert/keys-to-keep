from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(200), nullable=False)
	full_name = db.Column(db.String(200), nullable=False)
	username = db.Column(db.String(200), nullable=False)
	password = db.Column(db.String(200), nullable=False)
	bank_number = db.Column(db.String(200), nullable=False)
		
	def __repr__(self):
		return '<User %r>' % self.id

class ProductCategory(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(200), nullable=False)
	
	def __repr__(self):
		return '<ProductCategory %r>' % self.id

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)
	name = db.Column(db.String(200), nullable=False)

	def __repr__(self):
		return '<Product %r>' % self.id

class ProductModel(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	name = db.Column(db.String(200), nullable=False)
	price = db.Column(db.Integer, nullable=False)
	quantity = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return '<ProductModel %r>' % self.id


@app.route('/')
def index():
	return render_template("main_page.html")

@app.route('/login')
def login():
	return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
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
			return redirect(url_for("index"))
		else:
			message = "Username is taken. Please use another one."
	elif request.method == "POST":
		message = "Incomplete registration data. Please fill all fields." 
	return render_template('register.html', message=message, full_name=f_nm, username=usrnm, email=eml, password=pwd, bank_number=bk_nbr)

if __name__ == "__main__":
	app.run(debug=True)
