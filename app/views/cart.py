from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required
from ..models import CartItem, db


bp = Blueprint(
    "cart",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/cart",
)


@bp.route("/")
@login_required
def cart_detail():
    pass


@bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():

    cart_item_id = request.form.get("cart_item_id")
    cart_item = CartItem.query.filter_by(id=cart_item_id).first()
    
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)
        db.session.commit()
        flash("Product removed from cart", "success")
    else:
        flash("Product not found in cart", "danger")

    return redirect(url_for("cart.cart_detail"))
