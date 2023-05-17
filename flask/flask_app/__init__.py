from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Set Up SQLAlchemy Object
db = SQLAlchemy()

# Define Start Method
def create_app():
    
    # Create a Flask Instance
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super duper secret key'

    # Initialize MySQL Database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@10.0.0.2:5432/webcad_db'
    db.init_app(app)
    
    from .routes import admin_bp, user_bp, error_bp
    
    app.register_blueprint(user_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/')
    app.register_blueprint(error_bp)

    # Set Up Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user_bp.index'

    from .tables import Admins

    @login_manager.user_loader
    def load_user(user_id):
        return Admins.query.get(int(user_id))

    return app

