from app.config.database import Base, engine

# Import models so SQLAlchemy knows about them.
from app.models import Customer, Order, Ticket, Refund


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")