from flask import render_template, Blueprint, request, flash, redirect, url_for
from ..models import Address, db, ShoppingCart, Order, AuthUser, DeliveryMethod, CartItem, ProductItem
from flask_login import login_required, current_user
import logging
import datetime
from ..utils.order_utils import get_saved_address_list, create_new_cart
from sqlalchemy import text, bindparam

bp = Blueprint(
    "order",
    __name__,
    template_folder="templates/",
    static_folder="static",
    url_prefix="/order",
)


@bp.route("/")
@login_required
def index():
    cart = ShoppingCart.query.filter_by(auth_user_id=current_user.id).order_by(ShoppingCart.timestamp.desc()).first()
    cart_items = CartItem.query.filter_by(shopping_cart_id=cart.id).all()
    if len(cart_items) == 0:
        flash("Your cart is empty!")
        return redirect("/cart")
    saved_address_list = get_saved_address_list(current_user.id)
    delivery_methods = db.session.query(DeliveryMethod).all()
    return render_template(
        "order/make_order.html",
        saved_address_list=saved_address_list,
        delivery_methods=delivery_methods,
    )


@bp.route("/submit_order", methods=["POST"])
@login_required
def submit_order():
    cart = ShoppingCart.query.filter_by(auth_user_id=current_user.id).order_by(ShoppingCart.timestamp.desc()).first()
    cart_items = CartItem.query.filter_by(shopping_cart_id=cart.id).all()

    if len(cart_items) == 0:
        flash("Your cart is empty!")
        return redirect("/cart")
    address_from_history = True if request.form["address_from_history"] == "true" else False
    logging.info(f"address_from_history: {address_from_history}")

    if address_from_history is True:
        logging.info("address_from_history is True")
        address_id = request.form["saved_address_select"]
        address = Address.query.filter_by(id=address_id).first()
    else:
        street = request.form["street"]
        city = request.form["city"]
        country = request.form["country"]
        zip_code = request.form["zip_code"]

        if not all([street, city, country, zip_code]):
            flash("All address fields are required!")
            return redirect("/order")

        address = Address(street=street, city=city, country=country, zip_code=zip_code)

        db.session.add(address)
        db.session.commit()

    cart = ShoppingCart.query.filter_by(auth_user_id=current_user.id).order_by(ShoppingCart.timestamp.desc()).first()

    if cart.total is None:
        flash("Your cart is empty!")
        return redirect("/cart")

    # Check if any items in the cart are out of stock
    cart_items = CartItem.query.filter_by(shopping_cart_id=cart.id).all()
    out_of_stock_items = []
    for item in cart_items:
        product_item = ProductItem.query.filter_by(id=item.product_item_id).first()
        if product_item.stock_number < item.quantity:
            out_of_stock_items.append(product_item)

    if out_of_stock_items:
        for product in out_of_stock_items:
            flash(f"Product {product.product_type.name} in size {product.size.name} is out of stock!", "danger")
        return redirect("/cart")

    delivery_method_id = request.form["delivery_method_id"]
    delivery_method = DeliveryMethod.query.filter_by(id=delivery_method_id).first()
    order_status_id = 1
    datetime_val = datetime.datetime.now()
    total = cart.total + delivery_method.price
    order = Order(
        address_id=address.id,
        cart_id=cart.id,
        total=total,
        datetime=datetime_val,
        order_status_id=order_status_id,
        delivery_method_id=delivery_method_id,
    )
    db.session.add(order)
    db.session.commit()
    create_new_cart(current_user.id)
    flash("Order successfull!")

    p_city = address.city
    p_month = str(datetime_val.month)
    p_year = datetime_val.year
    stmt_city = text("CALL city_reports(:p_city, :p_month, :p_year, :p_total)")
    stmt_city = stmt_city.bindparams(
        bindparam("p_city", value=p_city),
        bindparam("p_month", value=p_month),
        bindparam("p_year", value=p_year),
        bindparam("p_total", value=total),
    )

    db.session.execute(stmt_city)

    cart_items = CartItem.query.filter_by(shopping_cart_id=cart.id).all()

    for cart_item in cart_items:
        product_id = cart_item.product_item_id
        stmt_prod = text("CALL product_reports(:p_product_id, :p_month, :p_year, :p_count)")
        stmt_prod = stmt_prod.bindparams(
            bindparam("p_product_id", value=product_id),
            bindparam("p_month", value=p_month),
            bindparam("p_year", value=p_year),
            bindparam("p_count", value=cart_item.quantity),
        )
        db.session.execute(stmt_prod)
    db.session.commit()

    return redirect(url_for("order.success", order_id=order.id))


@bp.route("/success", methods=["GET"])
@login_required
def success():
    order_id = request.args.get("order_id")
    order = Order.query.filter_by(id=order_id).first()
    return render_template("order/success.html", order=order)
