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

	@staticmethod
	def get(class_name, query_id):
		return db.session.query(class_name).filter(class_name.id == query_id).first()

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
		return [keyboard.get_data() for keyboard in keyboards]

	@staticmethod
	def get_by_id(query_id):
		return db.session.query(Keyboard).filter(Keyboard.id == query_id).first()

	def add_rating(self, user, rating, description):
		new_rating = Review(user_id=user.id, keyboard_id=self.id, rating=rating, description=description)
		add_and_commit(new_rating)

	def add_variant(self, variant_type, name):
		new_variant = variant_type(keyboard_id=self.id, name=name)
		add_and_commit(new_variant)

	def get_data(self):
		reviews =  self.get_reviews()
		return {
			"keyboard" : self,
			"keycaps" : Item.get(Keycaps, self.keycaps),
			"switch_type" : Item.get(SwitchType, self.switch_type),
			"reviews" : reviews,
			"price" : format_money(self.price),
			"discounted_price": format_money(self.get_discounted_price()),
			"number_of_reviews" : str(reviews["count"]) if reviews["count"] < 100 else (str(round(reviews["count"], -2)) + "+"),
			"switches" : self.get_variants(Switch),
			"colors" : self.get_variants(Color),
			"stars" : ('★' * int(reviews["average"])) + ('☆' * (5 - int(reviews["average"]))) if int(reviews["average"]) != -1 else "",
		}

	def get_discounted_price(self):
		return int(self.price - self.price * (self.discount / 100))
	
	def get_reviews(self):
		reviews = db.session.query(Review).filter(Review.id == self.id).all()
		reviewers = [review.get_reviewer() for review in reviews]
		count = len(reviews)
		sum = 0
		for rating in reviews: sum += rating.rating
		return {
			"reviews" : reviews,
			"reviewers" : reviewers,
			"stars" : [review.get_stars() for review in reviews],
			"count" : count,
			"average" : round((sum / count) if count > 0 else -1, 1),
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
	
class Review(db.Model):
	__tablename__ = 'review'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	keyboard_id = db.Column(db.Integer, db.ForeignKey('keyboard.id'), nullable=False)
	rating = db.Column(db.Integer)
	description = db.Column(db.String(1024))

	def __repr__(self):
		return '<Rating %r>' % self.id

	def get_stars(self):
		return ('★' * self.rating) + ('☆' * (5 - self.rating)) if self.rating != -1 else ""


	def get_reviewer(self):
		return db.session.query(User).filter(User.id == self.user_id).first()