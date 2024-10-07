# init_db.py
from app import create_app, db
from app.models import User, Contest
from datetime import datetime, timedelta

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()

        # Create admin user
        admin = User(username="admin", is_admin=True)
        admin.set_password("admin_password")
        db.session.add(admin)

        # Create regular user
        user = User(username="user")
        user.set_password("user_password")
        db.session.add(user)

        # Create sample contests
        now = datetime.utcnow()
        contest1 = Contest(
            name="Pumpkin Carving Contest 2024",
            start_date=now,
            end_submission_date=now + timedelta(days=7),
            end_voting_date=now + timedelta(days=14),
            theme="Halloween Horrors"
        )
        contest2 = Contest(
            name="Gingerbread House Contest 2024",
            start_date=now + timedelta(days=30),
            end_submission_date=now + timedelta(days=37),
            end_voting_date=now + timedelta(days=44),
            theme="Winter Wonderland"
        )
        db.session.add(contest1)
        db.session.add(contest2)

        db.session.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized with sample data.")