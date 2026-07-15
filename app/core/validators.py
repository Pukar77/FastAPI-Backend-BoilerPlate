import re
from app.core.exceptions import BadRequestException


def validate_email(email: str) -> str:
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise BadRequestException("Invalid email format")
    return email


def validate_password(password: str) -> str:
    if len(password) < 8:
        raise BadRequestException("Password must be at least 8 characters long")
    if not re.search(r'[A-Z]', password):
        raise BadRequestException("Password must contain at least one uppercase letter")
    if not re.search(r'[a-z]', password):
        raise BadRequestException("Password must contain at least one lowercase letter")
    if not re.search(r'\d', password):
        raise BadRequestException("Password must contain at least one digit")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_]', password):
        raise BadRequestException("Password must contain at least one special character")
    return password


def validate_phone_number(phone: str) -> str:
    digits = re.sub(r'\D', '', phone)
    if len(digits) < 7 or len(digits) > 15:
        raise BadRequestException("Phone number must be between 7 and 15 digits")
    return phone


def validate_name(name: str) -> str:
    if not name or not name.strip():
        raise BadRequestException("Name cannot be empty")
    if len(name.strip()) < 2:
        raise BadRequestException("Name must be at least 2 characters long")
    if len(name.strip()) > 100:
        raise BadRequestException("Name must not exceed 100 characters")
    return name.strip()
