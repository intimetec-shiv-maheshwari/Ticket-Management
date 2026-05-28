from sqlalchemy.orm import Session

from src.models.users import Users


def get_all_users(db: Session):
    return db.query(Users).all()


def create_user(user: Users, db: Session):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email: str, db: Session):
    return db.query(Users).filter(Users.email == email).first()


def get_user_by_id(user_id: str, db: Session):
    return db.query(Users).filter(Users.id == user_id).first()


def update_user(user: Users, db: Session):
    db.commit()
    db.refresh(user)
    return user


def delete_user(user: Users, db: Session):
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


def get_users_by_organization_id(organization_id: str, db: Session):
    return db.query(Users).filter(Users.organization_id == organization_id).all()
