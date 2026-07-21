from fastapi import APIRouter, Depends, status, Form, UploadFile, File
from typing import Optional
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.model.product_model import Product
from app.schema.product_schema import ProductOutput
from app.core.security import require_admin
from app.core.exceptions import NotFoundException
from app.core.file_utils import save_image, delete_image


router = APIRouter(prefix='/products', tags=['Products'])


@router.post('/', response_model=ProductOutput, status_code=status.HTTP_201_CREATED)
def create_product(
    name: str = Form(...),
    price: float = Form(...),
    description: Optional[str] = Form(None),
    stock: int = Form(0),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    admin: None = Depends(require_admin),
):
    image_url = save_image(image) if image else None

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_url=image_url,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get('/', response_model=list[ProductOutput])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get('/{product_id}', response_model=ProductOutput)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise NotFoundException("Product not found")
    return product


@router.put('/{product_id}', response_model=ProductOutput)
def update_product(
    product_id: int,
    name: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    description: Optional[str] = Form(None),
    stock: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    admin: None = Depends(require_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise NotFoundException("Product not found")

    if name is not None:
        product.name = name
    if price is not None:
        product.price = price
    if description is not None:
        product.description = description
    if stock is not None:
        product.stock = stock
    if image:
        if product.image_url:
            delete_image(product.image_url)
        product.image_url = save_image(image)

    db.commit()
    db.refresh(product)
    return product


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: None = Depends(require_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise NotFoundException("Product not found")

    if product.image_url:
        delete_image(product.image_url)
    db.delete(product)
    db.commit()
