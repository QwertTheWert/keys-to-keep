from flask_login import UserMixin
from app import db, add_and_commit, format_money
from datetime import datetime, timezone


class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(200), nullable=False, unique=True)
	full_name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False, unique=True)
	password = db.Column(db.String(200), nullable=False)
	address = db.Column(db.String(200), nullable=False)
		
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

	def get_total(self, cart_data=None):
		if cart_data == None:
			cart_data = [cart.get_data() for cart in db.session.query(Cart).filter(Cart.user_id == self.id).all()]
		return sum([cart_datum["subtotal_int"] for cart_datum in cart_data])

	def get_reviews(self):
		review_data = db.session.query(Review, Keyboard, Color, Switch)\
			.join(Keyboard, Review.keyboard_id == Keyboard.id)\
			.join(Color, Review.color_id == Color.id)\
			.join(Switch, Review.switch_id == Switch.id)\
			.filter(Review.user_id == self.id)\
			.all()
		return [{
			"data" : data,
			"stars" : data[0].get_stars(),
		} for data in review_data]

	def get_carts(self):
		carts = db.session.query(Cart).filter(Cart.user_id == self.id).all()
		cart_data = [cart.get_data() for cart in carts]
		total = self.get_total(cart_data)
		return {
			"cart_data": cart_data,
			"total": format_money(total),
			"total_int": total,
		}


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
	image_url = db.Column(db.String(200), nullable=False, default="assets/Vortex series 82.png")
	description = db.Column(db.String(1024))
	switch_type = db.Column(db.Integer, db.ForeignKey('switch_type.id'))
	keycaps = db.Column(db.Integer, db.ForeignKey('keycaps.id'))
	discount = db.Column(db.Integer, nullable=False, default=0)
	date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
	sold = db.Column(db.Integer, nullable=False, default=0)
	price = db.Column(db.Integer, nullable=False, default=0)
	quantity = db.Column(db.Integer, nullable=False, default=0)

	@staticmethod
	def get_data_all(is_ascending):
		keyboards = db.session.query(Keyboard).order_by(Keyboard.price.asc() if is_ascending else Keyboard.price.desc()).all()
		return [keyboard.get_data() for keyboard in keyboards]
	
	@staticmethod
	def get_trending():
		keyboards = db.session.query(Keyboard).order_by(Keyboard.sold.desc()).limit(6).all()
		return [keyboard.get_data() for keyboard in keyboards]

	@staticmethod
	def get_newest():
		keyboards = db.session.query(Keyboard).order_by(Keyboard.date_added.desc()).limit(6).all()
		return [keyboard.get_data() for keyboard in keyboards]

	@staticmethod
	def get_by_id(query_id):
		return db.session.query(Keyboard).filter(Keyboard.id == query_id).first()

	def add_review(self, user, rating, description):
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
			"discounted_price_int": self.get_discounted_price(),
			"number_of_reviews" : str(reviews["count"]) if reviews["count"] < 100 else (str(round(reviews["count"], -2)) + "+"),
			"switches" : self.get_variants(Switch),
			"colors" : self.get_variants(Color),
			"stars" : ('★' * int(reviews["average"])) + ('☆' * (5 - int(reviews["average"]))) if int(reviews["average"]) != -1 else "",
		}

	def get_discounted_price(self):
		return int(self.price - self.price * (self.discount / 100))
	
	def get_reviews(self):
		reviews = db.session.query(Review).filter(Review.keyboard_id == self.id).all()
		reviewers = [review.get_reviewer() for review in reviews]
		count = len(reviews)
		sum = 0
		for rating in reviews: sum += rating.rating if rating.rating else 0
		return {
			"reviews" : reviews,
			"reviewers" : reviewers,
			"stars" : [review.get_stars() for review in reviews],
			"count" : count,
			"average" : round((float(sum) / float(count)) if count > 0 else -1, 1),
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
		return '<Switch %r>' % self.id

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
	
	def get_data(self):
		keyboard_data = self.get_keyboard_data()
		subtotal = keyboard_data["keyboard"].get_discounted_price() * self.quantity
		return {
			"cart": self,
			"keyboard_data": keyboard_data,
			"color": Item.get(Color, self.color_id),
			"switch": Item.get(Switch, self.switch_id),
			"subtotal" : format_money(subtotal),
			"subtotal_int" : subtotal,
		}

	def get_keyboard_data(self):
		return db.session.query(Keyboard).filter(Keyboard.id == self.keyboard_id).first().get_data()

	def __repr__(self):
		return '<Cart %r>' % self.id
	
class Review(db.Model):
	__tablename__ = 'review'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	keyboard_id = db.Column(db.Integer, db.ForeignKey('keyboard.id'), nullable=False)
	transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
	color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
	switch_id = db.Column(db.Integer, db.ForeignKey('switch.id'), nullable=False)
	rating = db.Column(db.Integer, default="-1")
	description = db.Column(db.String(1024), default="-1")

	@staticmethod
	def create(cart, transaction_id):
		review = Review(user_id=cart.user_id, keyboard_id=cart.keyboard_id, color_id=cart.color_id, switch_id=cart.switch_id, transaction_id=transaction_id)
		add_and_commit(review)
		return review

	def __repr__(self):
		return '<Rating %r>' % self.id
	
	@staticmethod
	def get_edit_data(query_id):
		review = db.session.query(Review, Keyboard, Color, Switch, User)\
			.join(Keyboard, Review.keyboard_id == Keyboard.id)\
			.join(Color, Review.color_id == Color.id)\
			.join(Switch, Review.switch_id == Switch.id)\
			.join(User, Review.user_id == User.id)\
			.filter(Review.id == query_id)\
			.first()

		return review
	

	def get_stars(self):
		rating_int = self.rating if self.rating else 0
		return ('★' * rating_int) + ('☆' * (5 - rating_int)) if rating_int != -1 else ""

	def get_reviewer(self):
		return db.session.query(User).filter(User.id == self.user_id).first()


class DeliveryService(Item):
	__tablename__ = 'delivery_service'
	price = db.Column(db.Integer, nullable=False)

	@staticmethod
	def get_all():
		return db.session.query(DeliveryService).all()

	@staticmethod
	def get_price(query_id):
		return db.session.query(DeliveryService).filter(DeliveryService.id == query_id).first()

	def __repr__(self):
		return '<Delivery Service -- %r>' % self.name
	

class Transaction(db.Model):
	__tablename__ = 'transaction'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	delivery_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
	total_price = db.Column(db.Integer, nullable=False)


	@staticmethod
	def get_data(query_id):
		transaction = db.session.query(Transaction).filter(Transaction.id == query_id).first()
		review_data = db.session.query(Review, Keyboard, Color, Switch)\
			.join(Keyboard, Review.keyboard_id == Keyboard.id)\
			.join(Color, Review.color_id == Color.id)\
			.join(Switch, Review.switch_id == Switch.id)\
			.filter(Review.transaction_id == transaction.id)\
			.all()

		return {
			"transaction" : transaction,
			"review_data": review_data
		}

	def __repr__(self):
		return '<Transaction %r>' % self.id