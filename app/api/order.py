from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.model.order_model import Order, OrderItem
from app.model.cart_model import CartItem
from app.model.product_model import Product
from app.schema.order_schema import OrderOutput, OrderItemOutput
from app.core.security import get_current_user
from app.model.user_model import User
from app.core.exceptions import BadRequestException, NotFoundException


router = APIRouter(prefix='/orders', tags=['Orders'])


@router.post('/', response_model=OrderOutput, status_code=status.HTTP_201_CREATED)
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_items = (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id)
        .all()
    )

    if not cart_items:
        raise BadRequestException("Cart is empty")

    order_items_data = []
    total = 0.0

    for cart_item in cart_items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if not product:
            raise BadRequestException(f"Product (ID {cart_item.product_id}) no longer exists")

        if product.stock < cart_item.quantity:
            raise BadRequestException(
                f"Insufficient stock for '{product.name}'. Only {product.stock} available"
            )

        line_total = round(product.price * cart_item.quantity, 2)
        total += line_total
        order_items_data.append({
            "product_id": product.id,
            "product_name": product.name,
            "quantity": cart_item.quantity,
            "price": product.price,
        })

    order = Order(
        user_id=current_user.id,
        total=round(total, 2),
    )
    db.add(order)
    db.flush()

    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            **item_data,
        )
        db.add(order_item)

        product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
        product.stock -= item_data["quantity"]

    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()

    db.commit()
    db.refresh(order)

    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    return OrderOutput(
        id=order.id,
        status=order.status,
        total=order.total,
        items=[
            OrderItemOutput(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price,
                total=round(item.price * item.quantity, 2),
                created_at=item.created_at,
            )
            for item in items
        ],
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


@router.get('/', response_model=list[OrderOutput])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    result = []
    for order in orders:
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        result.append(OrderOutput(
            id=order.id,
            status=order.status,
            total=order.total,
            items=[
                OrderItemOutput(
                    id=item.id,
                    product_id=item.product_id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    price=item.price,
                    total=round(item.price * item.quantity, 2),
                    created_at=item.created_at,
                )
                for item in items
            ],
            created_at=order.created_at,
            updated_at=order.updated_at,
        ))

    return result


@router.get('/{order_id}', response_model=OrderOutput)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == current_user.id)
        .first()
    )
    if not order:
        raise NotFoundException("Order not found")

    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    return OrderOutput(
        id=order.id,
        status=order.status,
        total=order.total,
        items=[
            OrderItemOutput(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price,
                total=round(item.price * item.quantity, 2),
                created_at=item.created_at,
            )
            for item in items
        ],
        created_at=order.created_at,
        updated_at=order.updated_at,
    )
