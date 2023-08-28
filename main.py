from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from sqlalchemy.orm import Session

from pack import crud, models, schemas
from pack.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/blogs/", response_model=schemas.Blog)
def create_blog_for_user(
    user_id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    return crud.create_user_blog(db=db, blog=blog, user_id=user_id)


@app.get("/blogs/", response_model=list[schemas.Blog])
def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blogs = crud.get_blogs(db, skip=skip, limit=limit)
    return blogs


@app.put("/blogs/{blog_id}/update", response_model=schemas.BlogCreate)
def update(blog_id: int, updated_blog: schemas.BlogCreate, db:Session=Depends(get_db)):

    if crud.update_blog(db=db, blog_id=blog_id, updated_blog=updated_blog.model_dump()) == 1:
        raise HTTPException(status_code=404, detail="Blog does not exists")
    else:
        pass
    
    

@app.delete("/blogs/{blog_id}")
def destroy(blog_id: int, db: Session = Depends(get_db)):
    # return 
    if crud.delete_blog_by_id(blog_id=blog_id, db=db) == 1:
        raise HTTPException(status_code=404, detail="Blog does not exists")
    else:
        pass
        # return crud.delete_blog_by_id(blog_id=blog_id, db=db)
        
    
if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')