from ..models import Address, db, ShoppingCart, Order, AuthUser, DeliveryMethod
import datetime


def get_saved_address_list(current_user_id: int):
    return (
        db.session.query(Address)
        .join(Order, Address.id == Order.address_id)
        .join(ShoppingCart, ShoppingCart.id == Order.cart_id)
        .join(AuthUser, AuthUser.id == ShoppingCart.auth_user_id)
        .filter((AuthUser.id == current_user_id))
        .all()
    )


def create_new_cart(current_user_id: id):

    cart = ShoppingCart(auth_user_id=current_user_id, timestamp=datetime.datetime.now(), total=0.0)
    db.session.add(cart)
    db.session.commit()
    return cart
