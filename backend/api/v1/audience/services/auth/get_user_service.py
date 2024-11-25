from sqlmodel import Session, select

from backend.models.user import User


def get_user_by_email(db: Session, email: str, role_code: str) -> User | None:
    """
    Get active user or None
    """
    user = db.exec(
        select(User).where(
            User.email == email,
            User.role_code == role_code,
            User.deleted_at.is_(None),
        )
    ).first()

    return user
