from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(200), nullable=False, unique=True)
	full_name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False, unique=True)
	password = db.Column(db.String(200), nullable=False)
	bank_number = db.Column(db.String(200), nullable=False)
		
	def __repr__(self):
		return '<User %r>' % self.id
	
	def get_id(self):
		return self.id

class ProductCategory(db.Model):
	__tablename__ = 'product_category'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(200), nullable=False)
	
	def __repr__(self):
		return '<ProductCategory %r>' % self.id

class Product(db.Model):
	__tablename__ = 'product'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)
	name = db.Column(db.String(200), nullable=False)
	slogan = db.Column(db.String(200), nullable=True)
	description = db.Column(db.String(1024), nullable=True)
	discount = db.Column(db.Integer, nullable=False, default=0)

	def __repr__(self):
		return '<Product %r>' % self.id

class ProductModel(db.Model):
	__tablename__ = 'product_model'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	name = db.Column(db.String(200), nullable=False)
	price = db.Column(db.Integer, nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	description = db.Column(db.String(1024), nullable=True)

	def __repr__(self):
		return '<ProductModel %r>' % self.id

class Cart(db.Model):
	__tablename__ = 'cart'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	product_model_id = db.Column(db.Integer, db.ForeignKey('product_model.id'), nullable=False)
	quantity = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return '<Cart %r>' % self.id
	
	def get_id(self):
		return self.id
	
class Rating(db.Model):
	__tablename__ = 'rating'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	description = db.Column(db.String(1024), nullable=True)

	def __repr__(self):
		return '<Rating %r>' % self.id