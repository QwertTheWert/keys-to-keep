from app import create_app, create_dummy_data

flask_app = create_app()


if __name__ == "__main__":
	# db.create_all()
	# from app import db, create_app, create_dummy_data
	# new_app = create_app()
	# new_app.app_context().push()
	# create_dummy_data()
	
	flask_app.run(debug=True)


# from app import db, create_app, create_dummy_data
# new_app = create_app()
# new_app.app_context().push()
# create_dummy_data()
# exit()
#