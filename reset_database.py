import os
from app import db, create_app, create_dummy_data

file_path = 'instance/database.db'
if os.path.exists(file_path):
    os.remove(file_path)
new_app = create_app()
new_app.app_context().push()
db.create_all()
create_dummy_data()
exit()
