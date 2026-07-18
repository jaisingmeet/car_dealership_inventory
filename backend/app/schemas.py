from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Authentication Schemas
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Vehicle Schemas (Car ko badalkar Vehicle kar diya hai)
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

    # Pydantic V2 standard configuration
    model_config = ConfigDict(from_attributes=True)