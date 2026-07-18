from pydantic import BaseModel, ConfigDict

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

    # Pydantic V2 standard syntax
    model_config = ConfigDict(from_attributes=True)