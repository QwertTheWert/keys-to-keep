import sys
sys.path.insert(0, "C:/UnivProjects/keys_to_keep")

from models import User, Transaction, Review
from flask import url_for

def test_main(client):
	response = client.get("/")
	assert response.status_code == 200
	assert b"<title>Keys 2 Keep</title>" in response.data


def test_register(client, flask_app, register_user):
	register_user(client)
	with flask_app.app_context():
		assert User.query.count() == 1
		assert User.query.first().email == "test@email.com"
		
def test_login_with_username(client, register_user, login_user):
	register_user(client)
	with client:
		response = login_user(client)

		from flask_login import current_user
		assert response.status_code == 302
		assert response.headers["Location"].endswith("/")
		assert current_user.is_authenticated

def test_login_with_email(client, register_user):
	register_user(client)
	with client:
		response = client.post("/login", data={
			"identifier": "test@email.com",
			"password": "123456",
		})

		from flask_login import current_user
		assert response.status_code == 302
		assert response.headers["Location"].endswith("/")
		assert current_user.is_authenticated

def test_keybaord(client_d):
	with client_d:
		keyboard_id = 1
		response = client_d.get(f"/keyboard/{keyboard_id}")
		assert response.status_code == 200

def test_add_to_cart(add_to_cart_response):
	assert add_to_cart_response.status_code == 200
	assert add_to_cart_response.get_json()["success"] is True


def test_cart_without_login(client):
	response = client.get("/cart/")
	assert response.status_code == 302
	assert response.headers["Location"].endswith("login")


def test_cart_empty(client_d, register_user, login_user):
	register_user(client_d)
	with client_d:
		response = login_user(client_d)
		response = client_d.get("/cart/")
		assert response.status_code == 200
		assert b'disabled="true"' in response.data

def test_cart(client_d, add_to_cart_response):
	response = client_d.get("/cart/")
	assert response.status_code == 200
	assert b'Remove' in response.data


def test_payment_empty(client_d, register_user, login_user):
	register_user(client_d)
	with client_d:
		response = login_user(client_d)
		response = client_d.get("/payment/")
		assert response.status_code == 302
		assert response.headers["Location"].endswith("/")

def test_payment(client_d, add_to_cart_response):
	response = client_d.get("/payment/")
	assert response.status_code == 200
	assert b'Payment Options' in response.data


def test_create_transaction(flask_app_d, client_d, add_to_cart_response):
	response = client_d.post("/payment/create_transaction", json={
		"delivery_id": 1,
		"total_price": 200000,
	})
	assert response.json["transaction_id"]
	with flask_app_d.app_context():
		assert Transaction.query.count() == 1 

def test_complete(client_d, add_to_cart_response):
	client_d.post("/payment/create_transaction", json={"delivery_id": 1, "total_price": 200000,})
	response = client_d.get("/complete/")
	assert response.status_code == 405
	response = client_d.post("/complete/", data={"transaction_id": 1})
	assert response.status_code == 200

def test_profile_page(client, register_user, login_user):
	response = client.get("/profile")
	assert response.status_code == 302
	assert response.headers["Location"].endswith("login")
	register_user(client)
	with client:
		login_user(client)
		response = client.get("/profile")
		assert response.status_code == 200

def test_logout(client, register_user, login_user):
	register_user(client)
	with client:
		response = client.get("/profile/logout")
		assert response.status_code == 302
		assert response.headers["Location"].endswith("login")

def test_delete_account(client, register_user, login_user):
	register_user(client)
	with client:
		response = client.get("/profile/delete")
		assert response.status_code == 302
		assert response.headers["Location"].endswith("/")
		assert User.query.count() == 0

def test_edit_user(client, register_user, login_user):
	response = client.get("/profile/edit")
	assert response.status_code == 302
	assert response.headers["Location"].endswith("login")
	register_user(client)
	with client:
		response = client.get("/profile/edit")
		assert response.status_code == 200
		assert b'<input type="text" name="address"' in response.data

		response=client.post('/profile/edit', data={
			"full_name": "Robert",
			"email": "Robert@gmail.com",
			"address": "new address",
		})
		assert response.status_code == 302
		assert response.headers["Location"].endswith("profile")
		assert User.query.filter(User.full_name == "Robert")


def test_compare(client_d):
	response = client_d.get("/compare")
	assert response.status_code == 200
	assert b'<title>Compare Keyboards</title>' in response.data
	response = client_d.post("/compare/get_data", json={"id":-1})
	assert response.json["valid"] == False
	response = client_d.post("/compare/get_data", json={"id":1})
	assert response.json["valid"] == True

def test_complete(client_d, add_to_cart_response, flask_app_d):
	client_d.post("/payment/create_transaction", json={"delivery_id": 1, "total_price": 200000})
	client_d.post("/complete/", data={"transaction_id": 1})
	response = client_d.get("review/19")
	assert response.status_code == 200
	response = client_d.post("/review/19", data={"selected_rating":5, "description": "Olala"})
	assert response.status_code == 302
	assert response.headers["Location"].endswith("profile")
	assert b'<button type="button" class="btn btn-sm btn-dark">' not in response.data
	with flask_app_d.app_context():
		review = Review.query.filter(Review.id == 19).first()
		assert review.rating == 5
		assert review.description == "Olala"

def test_additional_info(client):
	response = client.get("/about_us")
	assert response.status_code == 200
	assert b"<title>About Us - Keys 2 Keep</title>" in response.data
	response = client.get("/support")
	assert response.status_code == 200
	assert b"<title>Support - Keys 2 Keep</title>" in response.data

