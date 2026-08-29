from sqlalchemy.orm import Session

from app.db.models import Activity


class ActivityRepository:
    """
    Database repository for learning activities.
    """

    # ========================================================
    # CREATE ACTIVITY
    # ========================================================

    def create(
        self,
        db: Session,
        user_id: int,
        activity_type: str,
        course_id: int | None,
        description: str,
    ) -> Activity:
        """
        Create and save a learning activity.
        """

        activity = Activity(
            user_id=user_id,
            activity_type=activity_type,
            course_id=course_id,
            description=description,
        )

        db.add(activity)
        db.commit()
        db.refresh(activity)

        return activity

    # ========================================================
    # GET USER ACTIVITIES
    # ========================================================

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[Activity]:
        """
        Return all activities belonging to a user.
        """

        return (
            db.query(Activity)
            .filter(Activity.user_id == user_id)
            .order_by(Activity.id.desc())
            .all()
        )

    # ========================================================
    # GET ACTIVITY BY ID
    # ========================================================

    def get_by_id(
        self,
        db: Session,
        activity_id: int,
    ) -> Activity | None:
        """
        Return an activity by ID.
        """

        return (
            db.query(Activity)
            .filter(Activity.id == activity_id)
            .first()
        )


activity_repository = ActivityRepository()