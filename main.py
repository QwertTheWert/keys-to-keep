from app import create_app, db, create_dummy_data
import os


flask_app = create_app()


if __name__ == "__main__":
	
	file_path = 'instance/database.db'
	if not os.path.exists(file_path):
		flask_app.app_context().push()
		db.create_all()
		create_dummy_data()

	flask_app.run(host="0.0.0.0", port=int("3000"), debug=True)
