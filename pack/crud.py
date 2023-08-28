from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    hashed_password = pwd_context.hash(user.password)
    # fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_blogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Blog).offset(skip).limit(limit).all()



def create_user_blog(db: Session, blog: schemas.BlogCreate, user_id: int):
    db_blog = models.Blog(**blog.model_dump(), author_id=user_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def delete_blog_by_id(db: Session, blog_id: int):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not db_blog.first():
        return 1 
    db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session=False)
    db.commit()
    return {"detail" : f"blog with the `id`{blog_id} has been deleted"}


def update_blog(db: Session, blog_id: int, updated_blog:schemas.BlogCreate):

    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not db_blog.first():
        return 1 
    db_blog.update(updated_blog)
    db.commit()
    return {"detail" : f"blog with the `id`{blog_id} has been updated"}