from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SignUpUserInput(BaseModel):
    name:str
    email:str
    phone_number:str
    password:str

class SignUpUserOutput(BaseModel):
    id:int
    name:str
    email:str
    phone_number:str
    hashed_password:str
    role:str
    created_at:datetime
    updated_at:datetime

class loginUserInput(BaseModel):
    email:str
    password:str


    

    
