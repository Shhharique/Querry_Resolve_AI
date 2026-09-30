from sqlalchemy import select

from app.config.database import SessionLocal
from app.models import Order


def get_order(order_number: str) -> dict:
    """
    Retrieve an order by its order number.
    """

    db = SessionLocal()

    try:
        statement = select(Order).where(
            Order.order_number == order_number
        )

        order = db.execute(statement).scalar_one_or_none()

        if order is None:
            return {
                "found": False,
                "message": f"Order {order_number} was not found.",
            }

        return {
            "found": True,
            "order": {
                "id": order.id,
                "order_number": order.order_number,
                "customer_id": order.customer_id,
                "status": order.status,
                "total_amount": order.total_amount,
                "tracking_number": order.tracking_number,
                "created_at": order.created_at.isoformat(),
            },
        }

    finally:
        db.close()