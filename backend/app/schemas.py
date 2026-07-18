from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class CarCreate(BaseModel):
    make: str
    model: str
    year: int
    price: float
    status: str = "available"

class CarResponse(BaseModel):
    id: int
    make: str
    model: str
    year: int
    price: float
    status: str

    class Config:
        from_attributes = True