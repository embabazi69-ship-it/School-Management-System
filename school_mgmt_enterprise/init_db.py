
from app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    if not User.query.filter_by(email="admin@example.com").first():
        u = User(email="admin@example.com", name="Administrator", role="admin")
        u.set_password("adminpass")
        db.session.add(u)
        db.session.commit()
        print("Admin user created: admin@example.com / adminpass")
    else:
        print("Admin user already exists.")
