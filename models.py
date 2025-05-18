from flask_login import UserMixin
from app import db, add_and_commit, format_money

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
		
	@staticmethod
	def get_by_email(email_query):
		return db.session.query(User).filter(User.email == email_query).first()
	
	@staticmethod
	def get_by_username(username_query):
		return db.session.query(User).filter(User.username == username_query).first()

	def add_to_cart(self, keyboard, color_id, switch_id, quantity):
		new_cart = Cart(user_id=self.id, keyboard_id=keyboard.id, color_id=color_id, switch_id=switch_id, quantity=quantity)
		add_and_commit(new_cart)
	
	def update(self, new_full_name, new_email, new_bank_number):
		self.full_name = new_full_name 
		self.email = new_email
		self.bank_number = new_bank_number
		db.session.commit()
	
	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def get_carts(self):
		return db.session.query(Cart).filter(Cart.user_id == self.id).all()


class Item(db.Model):
	__abstract__ = True
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(200), nullable=False)

	def delete(self):
		db.session.delete(self)
		db.session.commit()

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
	price = db.Column(db.Integer, nullable=False, default=0)
	quantity = db.Column(db.Integer, nullable=False, default=0)

	@staticmethod
	def get_data_all(is_ascending):
		keyboards = db.session.query(Keyboard).order_by(Keyboard.price.asc() if is_ascending else Keyboard.price.desc()).all()
		data = []
		for keyboard in keyboards:
			ratings =  keyboard.get_ratings()
			data.append({
				"keyboard" : keyboard,
				"price" : format_money(keyboard.price),
				"discounted_price": format_money(keyboard.get_discounted_price()),
				"number_of_ratings" : str(ratings["count"]) if ratings["count"] < 100 else (str(round(ratings["count"], -2)) + "+"),
				"stars" : ('★' * ratings["average"]) + ('☆' * (5 - ratings["average"])) if ratings["average"] != -1 else "",
			})
		return data

	@staticmethod
	def get_by_id(query_id):
		return db.session.query(Keyboard).filter(Keyboard.id == query_id).first()

	def add_rating(self, user, rating, description):
		new_rating = Rating(user_id=user.id, keyboard_id=self.id, rating=rating, description=description)
		add_and_commit(new_rating)

	def add_variant(self, variant_type, name):
		new_variant = variant_type(keyboard_id=self.id, name=name)
		add_and_commit(new_variant)

	def get_discounted_price(self):
		return int(self.price - self.price * (self.discount / 100))
	
	def get_ratings(self):
		ratings = db.session.query(Rating).filter(Rating.id == self.id).all()
		count = len(ratings)
		sum = 0
		for rating in ratings: sum += rating.rating
		return {
			"ratings" : ratings,
			"count" : count,
			"average" : int(round((sum / count) if count > 0 else -1, 1)),
		}

	def get_variants(self, variant_type):
		return db.session.query(variant_type).filter(variant_type.keyboard_id == self.id).all()

	def __repr__(self):
		return '<Keyboard %r>' % self.name

class Variant(Item):
	__abstract__ = True
	keyboard_id = db.Column(db.Integer, db.ForeignKey('keyboard.id'), nullable=False)

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'keyboard_id': self.keyboard_id
		}

class Color(Variant):
	__tablename__ = 'color'
	def __repr__(self):
		return '<Color %r>' % self.id

class Switch(Variant):
	__tablename__ = 'switch'
	def __repr__(self):
		return '<Color %r>' % self.id

class Cart(db.Model):
	__tablename__ = 'cart'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	keyboard_id = db.Column(db.Integer, db.ForeignKey('keyboard.id'), nullable=False)
	color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
	switch_id = db.Column(db.Integer, db.ForeignKey('switch.id'), nullable=False)
	quantity = db.Column(db.Integer, nullable=False)

	@staticmethod
	def get_by_id(cart_id):
		return db.session.query(Cart).filter(Cart.id == cart_id).first()

	def get_keyboard(self):
		return db.session.query(Keyboard).filter(Keyboard.id == self.keyboard_id).first() 

	def __repr__(self):
		return '<Cart %r>' % self.id
	
class Rating(db.Model):
	__tablename__ = 'rating'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	keyboard_id = db.Column(db.Integer, db.ForeignKey('keyboard.id'), nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	description = db.Column(db.String(1024), nullable=True)

	def __repr__(self):
		return '<Rating %r>' % self.id
