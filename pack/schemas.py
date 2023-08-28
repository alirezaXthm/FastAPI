from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    description: str


class BlogCreate(BlogBase):
    pass


class Blog(BlogBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    blogs: list[Blog] = []

    class Config:
        orm_mode = True
