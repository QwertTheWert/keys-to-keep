from flask import Blueprint, render_template

class MainPage:
	main_page_bp = Blueprint("main_page", __name__, template_folder="templates", static_folder="static", static_url_path="/main_page/static/")
	
	def __init__(self, flask_app, bcrypt):
		@self.main_page_bp.route('/')
		def main_page():

			return render_template("main_page.html")


		flask_app.register_blueprint(self.main_page_bp)