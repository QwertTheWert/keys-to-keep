import pytest
import sys

sys.path.insert(0, "C:/UnivProjects/keys_to_keep")
from app import create_app, db, create_dummy_data


@pytest.fixture()
def flask_app():
	flask_app = create_app("sqlite://")

	with flask_app.app_context():
		db.create_all()

	yield flask_app

@pytest.fixture()
def flask_app_d():
	flask_app = create_app("sqlite://")

	with flask_app.app_context():
		db.create_all()
		create_dummy_data()

	yield flask_app

@pytest.fixture()
def client(flask_app):
	return flask_app.test_client()


@pytest.fixture()
def client_d(flask_app_d):
	return flask_app_d.test_client()


@pytest.fixture
def register_user():
	def _register(client):
		return client.post("/register", data={
			"full_name": "TestUsername",
			"username": "test_username",
			"email": "test@email.com",
			"password": "123456",
			"address": "Test Address",
		})
	return _register


@pytest.fixture
def login_user():
	def _login(client):
		return client.post("/login", data={
				"identifier": "test@email.com",
				"password": "123456",
			})
	return _login

@pytest.fixture
def add_to_cart_response(client_d, register_user, login_user):
    register_user(client_d)
    with client_d:
        login_user(client_d)
        return client_d.post("/keyboard/add_to_cart/", json={
            "keyboard_id": 1,
            "variant_info": {
                "color": 2,
                "switch": 3
            },
            "quantity": 1
        })

