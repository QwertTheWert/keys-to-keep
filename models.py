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

class Item(db.Model):
	__abstract__ = True
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(200), nullable=False)

class SwitchType(Item):
	__tablename__ = 'switch_type'
	def __repr__(self):
		return '<SwitchType %r>' % self.id

class Keycaps(Item):
	__tablename__ = 'keycaps'
	def __repr__(self):
		return '<Keycaps %r>' % self.id

class Keyboard(Item):
	__tablename__ = 'keyboard'
	subtitle = db.Column(db.String(200))
	description = db.Column(db.String(1024))
	switch_type = db.Column(db.Integer, db.ForeignKey('switch_type.id'))
	keycaps = db.Column(db.Integer, db.ForeignKey('keycaps.id'))
	discount = db.Column(db.Integer, nullable=False, default=0)
	sold = db.Column(db.Integer, nullable=False, default=0)
	price = db.Column(db.Integer, nullable=False)
	quantity = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return '<Keyboard %r>' % self.name

class Variant(Item):
	__abstract__ = True
	keyboard_id = db.Column(db.Integer, db.ForeignKey('keyboard.id'), nullable=False)

class Color(Variant):
	__tablename__ = 'color'
	def __repr__(self):
		return '<Color %r>' % self.id

class Switch(Variant):
	__tablename__ = 'switch'
	def __repr__(self):
		return '<Color %r>' % self.id

class Cart(Variant):
	__tablename__ = 'cart'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	keyboard_id = db.Column(db.Integer, db.ForeignKey('keyboard.id'), nullable=False)
	quantity = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return '<Cart %r>' % self.id
	
	def get_id(self):
		return self.id
	
class Rating(db.Model):
	__tablename__ = 'rating'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	keyboard_id = db.Column(db.Integer, db.ForeignKey('keyboard.id'), nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	description = db.Column(db.String(1024), nullable=True)

	def __repr__(self):
		return '<Rating %r>' % self.id