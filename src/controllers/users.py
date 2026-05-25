from fastapi import HTTPException;
from sqlalchemy.orm import Session;

from src.dtos.users import UserCreateDTO, UserLoginDTO;
from src.models.users import Users;
from src.utils.constants import INVALID_CREDENTIALS, USER_INACTIVE, USER_NOT_FOUND, USERS_NOT_FOUND_FOR_ORGANIZATION;


def get_all_users(db: Session):
    return db.query(Users).all();


def add_user(user: UserCreateDTO, db: Session):
    data = user.model_dump();
    new_user = Users(**data);
    db.add(new_user);
    db.commit();
    db.refresh(new_user);
    return new_user;


def login_user(credentials: UserLoginDTO, db: Session):
    user = db.query(Users).filter(Users.email == credentials.email).first();
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=401, detail=INVALID_CREDENTIALS);
    if not user.active:
        raise HTTPException(status_code=403, detail=USER_INACTIVE);
    return user;


def get_user_by_id(user_id: str, db: Session):
    user = db.query(Users).filter(Users.id == user_id).first();
    if user is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND);
    return user;


def delete_user_by_id(user_id: str, db: Session):
    user = db.query(Users).filter(Users.id == user_id).first();
    if user is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND);
    db.delete(user);
    db.commit();
    return {"message": "User deleted successfully"};


def update_user_by_id(user_id: str, user: UserCreateDTO, db: Session):
    existing_user = db.query(Users).filter(Users.id == user_id).first();
    if existing_user is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND);
    existing_user.name = user.name;
    existing_user.email = user.email;
    existing_user.password = user.password;
    existing_user.organization_id = user.organization_id;
    existing_user.role_id = user.role_id;
    existing_user.active = user.active;
    db.commit();
    db.refresh(existing_user);
    return existing_user;

def get_users_by_organization_id(organization_id: str, db: Session):
    users = db.query(Users).filter(Users.organization_id == organization_id).all();
    if users is None:
        raise HTTPException(status_code=404, detail=USERS_NOT_FOUND_FOR_ORGANIZATION);
    return users;