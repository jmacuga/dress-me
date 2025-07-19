from sqlalchemy import event
from sqlalchemy.orm import Session
from .models import ShoppingCart, CartItem, Order, Invoice, db
from sqlalchemy import text, bindparam
import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_cart_total_direct(connection, shopping_cart_id):
    cart = connection.execute(
        db.text("SELECT id FROM cart WHERE id = :cart_id"),
        {"cart_id": shopping_cart_id}
    ).fetchone()
    
    if cart:
        total = connection.execute(
            db.text("""
                SELECT SUM(ci.quantity * pt.price) as total
                FROM cart_item ci
                JOIN product_item pi ON ci.product_item_id = pi.id
                JOIN product_type pt ON pi.product_type_id = pt.id
                WHERE ci.shopping_cart_id = :cart_id
            """),
            {"cart_id": shopping_cart_id}
        ).scalar()
        
        connection.execute(
            db.text("UPDATE cart SET total = :total WHERE id = :cart_id"),
            {"total": total if total is not None else 0, "cart_id": shopping_cart_id}
        )
        logger.info(f"Updating cart_id {shopping_cart_id} total to {total}")


@event.listens_for(CartItem, 'after_insert')
@event.listens_for(CartItem, 'after_update')
@event.listens_for(CartItem, 'after_delete')
def after_cart_item_change(mapper, connection, target):
    logger.info(f"cart_item_id: {target.id}")
    update_cart_total_direct(connection, target.shopping_cart_id)



def decrease_stock_number(connection, order_id):
    order_items = connection.execute(
        db.text("""
            SELECT ci.product_item_id, ci.quantity
            FROM cart_item ci
            JOIN cart sc ON ci.shopping_cart_id = sc.id
            WHERE sc.id = (
                SELECT o.cart_id
                FROM "order" o
                WHERE o.id = :order_id
            )
        """),
        {"order_id": order_id}
    ).fetchall()
    
    for item in order_items:
        connection.execute(
            db.text("""
                UPDATE product_item
                SET stock_number = stock_number - :quantity
                WHERE id = :product_item_id
            """),
            {"quantity": item.quantity, "product_item_id": item.product_item_id}
        )
        logger.info(f"Decreased stock for product_item_id {item.product_item_id} by {item.quantity}")


@event.listens_for(Order, 'after_insert')
def create_invoice_after_order_insert(mapper, connection, target):
    connection.execute(
        Invoice.__table__.insert().values(
            total=target.total,
            order_id=target.id
        )
    )
    datetime_val = datetime.datetime.now()
    stmt_invoice = text("CALL invoice_reports(:p_month, :p_year, :p_total)")
    stmt_invoice = stmt_invoice.bindparams(
        bindparam('p_month', value=str(datetime_val.month)),
        # bindparam('p_month', value='7'),
        bindparam('p_year', value=datetime_val.year),
        bindparam('p_total', value=target.total)
    )
    connection.execute(stmt_invoice)
