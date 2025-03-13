from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(200), nullable=False)
	password = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False)
		
	def __repr__(self):
		return '<User %r>' % self.id

class ProductCategory(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(200), nullable=False)
	
	def __repr__(self):
		return '<ProductCategory %r>' % self.id

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	category_id = db.Column(db.Integer, nullable=False)
	name = db.Column(db.String(200), nullable=False)
	
	category = db.relationship('ProductCategory', foreign_keys = "Product.category_id")

	def __repr__(self):
		return '<Product %r>' % self.id

class ProductModel(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	product_id = db.Column(db.Integer, nullable=False)
	name = db.Column(db.String(200), nullable=False)
	price = db.Column(db.Integer, nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	product = db.relationship('Product', foreign_keys = "ProductModel.product_id")

	def __repr__(self):
		return '<ProductModel %r>' % self.id


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/register')
def register():
	return render_template("register.html")

@app.route('/login')
def login():
	return render_template("login.html")

if __name__ == "__main__":
	app.run(debug=True)
