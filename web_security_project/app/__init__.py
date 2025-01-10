from flask import Flask, url_for
from flask_login import LoginManager, UserMixin

# Define your User class inheriting from UserMixin
class User(UserMixin):
    def __init__(self, id):
        self.id = id

def create_app():
    """ Factory function to create the Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'main_blueprint.login'
    login_manager.init_app(app)

    from app.routes import main_blueprint

    
    # Register the Blueprint
    app.register_blueprint(main_blueprint)

    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """
        Load user by ID for Flask-Login.
        Replace with database lookup in production.
        """
        return User(user_id)

    return app
