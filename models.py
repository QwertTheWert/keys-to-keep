from app import db

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(200), nullable=False)
	full_name = db.Column(db.String(200), nullable=False)
	username = db.Column(db.String(200), nullable=False, unique=True)
	password = db.Column(db.String(200), nullable=False)
	bank_number = db.Column(db.String(200), nullable=False)
		
	def __repr__(self):
		return '<User %r>' % self.id

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

	def __repr__(self):
		return '<Product %r>' % self.id

class ProductModel(db.Model):
	__tablename__ = 'product_model'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	name = db.Column(db.String(200), nullable=False)
	price = db.Column(db.Integer, nullable=False)
	quantity = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return '<ProductModel %r>' % self.id