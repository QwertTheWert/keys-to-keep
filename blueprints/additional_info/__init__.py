from flask import Blueprint, render_template

class AdditionalInfoPage:
    additional_info_bp = Blueprint("additional_info", __name__, template_folder="templates", 
                                 static_folder="static", static_url_path="/additional_info/static/")
    
    def __init__(self, flask_app, bcrypt):
        
        @self.additional_info_bp.route('/about-us')
        def about_us():
            return render_template("aboutUs.html")

        @self.additional_info_bp.route('/support')
        def support():
            return render_template("support.html")

        flask_app.register_blueprint(self.additional_info_bp)