from datetime import datetime, timedelta
import random

from sqlalchemy import delete

from app.config.database import SessionLocal
from app.models import Customer, Order, Refund, Ticket


def seed_database():
    db = SessionLocal()

    try:
        # Clear existing data so we can safely re-run the script
        db.execute(delete(Refund))
        db.execute(delete(Ticket))
        db.execute(delete(Order))
        db.execute(delete(Customer))
        db.commit()

        customers = []
        orders = []
        refunds = []
        tickets = []

        # -------------------------
        # Customers
        # -------------------------
        for i in range(1, 51):
            customer = Customer(
                name=f"Customer {i}",
                email=f"customer{i}@example.com",
                phone=f"98765000{i:02d}",
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
            )

            customers.append(customer)

        db.add_all(customers)
        db.flush()

        # -------------------------
        # Orders
        # -------------------------
        order_statuses = [
            "pending",
            "processing",
            "shipped",
            "delivered",
            "cancelled",
        ]

        for i in range(1, 101):
            customer = random.choice(customers)

            order = Order(
                order_number=f"ORD-{1000 + i}",
                customer_id=customer.id,
                status=random.choice(order_statuses),
                total_amount=round(random.uniform(20, 1000), 2),
                tracking_number=(
                    f"TRK{random.randint(100000, 999999)}"
                    if random.random() > 0.3
                    else None
                ),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 90)),
            )

            orders.append(order)

        db.add_all(orders)
        db.flush()

        # -------------------------
        # Refunds
        # -------------------------
        refund_reasons = [
            "Product damaged",
            "Wrong product received",
            "Order cancelled",
            "Product not required",
        ]

        for order in random.sample(orders, 30):
            refund = Refund(
                order_id=order.id,
                amount=order.total_amount,
                status=random.choice(["pending", "approved", "completed", "rejected"]),
                reason=random.choice(refund_reasons),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            )

            refunds.append(refund)

        db.add_all(refunds)

        # -------------------------
        # Support Tickets
        # -------------------------
        ticket_data = [
            ("Where is my order?", "My order has not arrived yet.", "shipping"),
            ("I want a refund", "I would like to get a refund for my order.", "refund"),
            ("Cancel my order", "Please cancel my order before it is shipped.", "cancellation"),
            ("Wrong product received", "The product I received is not what I ordered.", "product_issue"),
            ("Payment problem", "I was charged but my order is not showing.", "payment"),
            ("Account problem", "I am unable to access my account.", "account"),
        ]

        priorities = ["low", "medium", "high"]

        for i in range(1, 51):
            customer = random.choice(customers)

            title, description, intent = random.choice(ticket_data)

            related_order = (
                random.choice(orders)
                if random.random() > 0.2
                else None
            )

            ticket = Ticket(
                customer_id=customer.id,
                order_id=related_order.id if related_order else None,
                subject=title,
                description=description,
                status=random.choice(["open", "in_progress", "resolved"]),
                priority=random.choice(priorities),
                intent=intent,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            )

            tickets.append(ticket)

        db.add_all(tickets)
        db.commit()

        print("Database seeded successfully!")
        print(f"Customers: {len(customers)}")
        print(f"Orders: {len(orders)}")
        print(f"Refunds: {len(refunds)}")
        print(f"Tickets: {len(tickets)}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()