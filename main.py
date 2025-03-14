from app import create_app

flask_app = create_app()


if __name__ == "__main__":
	# from app import db
	# flask_app.app_context().push()
	# db.create_all()


	flask_app.run(debug=True)
