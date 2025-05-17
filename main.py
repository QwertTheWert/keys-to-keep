from app import create_app, create_dummy_data

flask_app = create_app()


if __name__ == "__main__":
	
	
	flask_app.run(debug=True)

## Create Database and Dummy Data, paste to terminal
# py
# from app import db, create_app, create_dummy_data
# db.create_all()
# new_app.app_context().push()
# create_dummy_data()
# exit()
#