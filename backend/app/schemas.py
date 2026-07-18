from pydantic import BaseModel, EmailStr, ConfigDict

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class VehicleCreate(BaseModel):
    make: str
    model: str
    year: int
    price: float
    status: str = "available"
    category: str
    quantity: int

class VehicleResponse(BaseModel):
    id: int
    make: str
    model: str
    year: int
    price: float
    status: str
    category: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)