from app.db.database import SessionLocal
from app.db.models import Course


COURSES = [
    {
        "title": "Introduction to Quantum Computing",
        "description": (
            "Learn the fundamentals of quantum computing, "
            "qubits, quantum states, and quantum gates."
        ),
        "level": "beginner",
        "duration": "4 weeks",
        "category": "quantum-computing",
    },
    {
        "title": "Quantum Gates and Circuits",
        "description": (
            "Understand single-qubit and multi-qubit gates "
            "and build basic quantum circuits."
        ),
        "level": "beginner",
        "duration": "3 weeks",
        "category": "quantum-circuits",
    },
    {
        "title": "Superposition and Entanglement",
        "description": (
            "Explore superposition, measurement, entanglement, "
            "and their role in quantum computation."
        ),
        "level": "intermediate",
        "duration": "3 weeks",
        "category": "quantum-concepts",
    },
    {
        "title": "Quantum Algorithms",
        "description": (
            "Study important quantum algorithms including "
            "Deutsch-Jozsa, Grover's algorithm, and introductory "
            "quantum algorithm design."
        ),
        "level": "intermediate",
        "duration": "5 weeks",
        "category": "quantum-algorithms",
    },
    {
        "title": "Quantum Programming with Qiskit",
        "description": (
            "Learn how to create, simulate, and execute "
            "quantum circuits using Qiskit."
        ),
        "level": "intermediate",
        "duration": "4 weeks",
        "category": "qiskit",
    },
]


def seed_courses():
    db = SessionLocal()

    try:
        existing_courses = db.query(Course).count()

        if existing_courses > 0:
            print(
                f"Courses already exist ({existing_courses})."
            )
            return

        for course_data in COURSES:
            course = Course(**course_data)
            db.add(course)

        db.commit()

        print(
            f"Successfully created {len(COURSES)} courses."
        )

    finally:
        db.close()


if __name__ == "__main__":
    seed_courses()