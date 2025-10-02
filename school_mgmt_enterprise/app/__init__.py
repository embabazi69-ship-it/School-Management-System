
import os
from flask import Flask
from flask_login import LoginManager
from .models import db, User
from .views import main_bp

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///school.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Sentry (optional)
    sentry_dsn = os.environ.get('SENTRY_DSN')
    if sentry_dsn:
        try:
            import sentry_sdk
            from sentry_sdk.integrations.flask import FlaskIntegration
            sentry_sdk.init(dsn=sentry_dsn, integrations=[FlaskIntegration()], traces_sample_rate=0.0)
        except Exception:
            pass

    db.init_app(app)

    # Migrations (Flask-Migrate)
    try:
        from flask_migrate import Migrate
        migrate = Migrate(app, db)
    except Exception:
        pass

    login_manager = LoginManager()
    login_manager.login_view = "main.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
