from flask import Blueprint, render_template

class MainPage:
	
	def __init__(self, flask_app, bcrypt):
		main_page_bp = Blueprint("main_page", __name__, template_folder="templates", static_folder="static", static_url_path="/main_page/static/")
		from models import Keyboard
		
		@main_page_bp.route('/')
		def main_page():

			trending = Keyboard.get_trending()
			newest = Keyboard.get_newest()



			return render_template("main_page.html", trending=trending, newest=newest)


		flask_app.register_blueprint(main_page_bp)