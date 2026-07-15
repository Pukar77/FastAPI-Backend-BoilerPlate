from app.model.user_model import User
from app.schema.user_schema import SignUpUserInput, SignUpUserOutput, loginUserInput
from fastapi import APIRouter, Depends, status
from app.database.session import get_db
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import DuplicateResourceException, UnauthorizedException
from app.core.validators import validate_email, validate_password, validate_phone_number, validate_name


router = APIRouter(prefix='/auth', tags=['Auth API'])


@router.post('/signup', response_model=SignUpUserOutput, status_code=status.HTTP_201_CREATED)
def signup(userinput: SignUpUserInput, db: Session = Depends(get_db)):
    validate_name(userinput.name)
    validate_email(userinput.email)
    validate_phone_number(userinput.phone_number)
    validate_password(userinput.password)

    existing_user = (
        db.query(User).filter(User.email == userinput.email).first()
    )

    if existing_user:
        raise DuplicateResourceException("Email already registered")

    new_user = User(
         name=userinput.name,
         email=userinput.email,
         phone_number=userinput.phone_number,
         hashed_password=hash_password(userinput.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user


@router.post('/login')
def login(userinput: loginUserInput, db: Session = Depends(get_db)):
    validate_email(userinput.email)

    user = db.query(User).filter(User.email == userinput.email).first()

    if not user or not verify_password(userinput.password, user.hashed_password):
        raise UnauthorizedException("Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }



    



