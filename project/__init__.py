from datetime import timedelta

from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Initialize SQLAlchemy instance (outside create_app for import access)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Session configuration
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
    app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XSS
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
    
    # Initialize extensions with app
    db.init_app(app)
    migrate = Migrate(app, db)
    
    @app.cli.command("migrate-up")
    def migrate_up():
        from flask_migrate import migrate, upgrade
        migrate()
        upgrade()
        print("Done!")
        
    @app.cli.command("recreate-db")
    def recreate_db():
        db.drop_all()
        db.create_all()
        print("Database recreated!")
        
    # Configure Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # User loader function for Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .challenges import challenges as challenges_blueprint
    app.register_blueprint(challenges_blueprint)
    
    return app