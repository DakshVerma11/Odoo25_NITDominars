# Import and register all blueprints here
from .auth import auth_bp
from .questions import questions_bp
from .answers import answers_bp
from .users import users_bp
from .notifications import notifications_bp
from .admin import admin_bp

# Function to register all blueprints with Flask app
def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(answers_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(admin_bp)