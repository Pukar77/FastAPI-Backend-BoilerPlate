from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.model.cart_model import CartItem
from app.model.product_model import Product
from app.schema.cart_schema import CartAddInput, CartUpdateInput, CartItemOutput, CartOutput
from app.core.security import get_current_user
from app.model.user_model import User
from app.core.exceptions import NotFoundException, BadRequestException


router = APIRouter(prefix='/cart', tags=['Cart'])


@router.post('/', response_model=CartItemOutput, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    data: CartAddInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise NotFoundException("Product not found")
    if product.stock < data.quantity:
        raise BadRequestException(f"Insufficient stock. Only {product.stock} available")

    existing = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == current_user.id,
            CartItem.product_id == data.product_id,
        )
        .first()
    )

    if existing:
        new_qty = existing.quantity + data.quantity
        if product.stock < new_qty:
            raise BadRequestException(f"Insufficient stock. Only {product.stock} available")
        existing.quantity = new_qty
        db.commit()
        db.refresh(existing)
        cart_item = existing
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=data.product_id,
            quantity=data.quantity,
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)

    return CartItemOutput(
        id=cart_item.id,
        product_id=product.id,
        product_name=product.name,
        price=product.price,
        quantity=cart_item.quantity,
        total=round(product.price * cart_item.quantity, 2),
        image_url=product.image_url,
        created_at=cart_item.created_at,
        updated_at=cart_item.updated_at,
    )


@router.get('/', response_model=CartOutput)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id)
        .all()
    )

    cart_items = []
    grand_total = 0.0

    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue
        total = round(product.price * item.quantity, 2)
        grand_total += total
        cart_items.append(CartItemOutput(
            id=item.id,
            product_id=product.id,
            product_name=product.name,
            price=product.price,
            quantity=item.quantity,
            total=total,
            image_url=product.image_url,
            created_at=item.created_at,
            updated_at=item.updated_at,
        ))

    return CartOutput(items=cart_items, grand_total=round(grand_total, 2))


@router.put('/{item_id}', response_model=CartItemOutput)
def update_cart_item(
    item_id: int,
    data: CartUpdateInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.user_id == current_user.id)
        .first()
    )
    if not cart_item:
        raise NotFoundException("Cart item not found")

    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if product.stock < data.quantity:
        raise BadRequestException(f"Insufficient stock. Only {product.stock} available")

    cart_item.quantity = data.quantity
    db.commit()
    db.refresh(cart_item)

    return CartItemOutput(
        id=cart_item.id,
        product_id=product.id,
        product_name=product.name,
        price=product.price,
        quantity=cart_item.quantity,
        total=round(product.price * cart_item.quantity, 2),
        image_url=product.image_url,
        created_at=cart_item.created_at,
        updated_at=cart_item.updated_at,
    )


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.user_id == current_user.id)
        .first()
    )
    if not cart_item:
        raise NotFoundException("Cart item not found")

    db.delete(cart_item)
    db.commit()


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
