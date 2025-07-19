from flask import render_template, Blueprint, request, flash, redirect, url_for
from ..models import Address, db, ShoppingCart, Order, AuthUser, DeliveryMethod, CartItem, ProductItem, OrderStatus
from flask_login import login_required, current_user

bp = Blueprint(
    "orders",
    __name__,
    template_folder="templates/",
    static_folder="static",
    url_prefix="/orders",
)

@bp.route("/", methods=["GET"])
@login_required
def orders_detail():
    orders = Order.query.join(ShoppingCart).filter(ShoppingCart.auth_user_id == current_user.id).all()
    order_details = []
    for order in orders:
        cart_items = CartItem.query.filter_by(shopping_cart_id=order.cart_id).all()
        delivery_method = DeliveryMethod.query.filter_by(id=order.delivery_method_id).first()
        address = Address.query.filter_by(id=order.address_id).first()
        order_status = OrderStatus.query.filter_by(id=order.order_status_id).first()
        order_details.append({
            'order': order,
            'cart_items': cart_items,
            'delivery_method': delivery_method,
            'address': address,
            'order_status': order_status
        })
    return render_template("orders/orders_detail.html", order_details=order_details)
