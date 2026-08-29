from app.db.database import SessionLocal
from app.db.models import User
from app.auth.security import hash_password


def create_student():
    db = SessionLocal()

    try:
        email = "student@example.com"

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            print("Student already exists.")
            return

        student = User(
            email=email,
            name="Demo Student",
            role="student",
            password_hash=hash_password("student123"),
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        print("Student created successfully.")
        print(f"ID: {student.id}")
        print(f"Email: {student.email}")
        print("Password: student123")

    finally:
        db.close()


if __name__ == "__main__":
    create_student()