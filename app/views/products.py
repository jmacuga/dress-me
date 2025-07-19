from flask import flash, render_template, Blueprint, request, redirect, url_for
from ..models import ProductType, Size, ProductItem, db, ShoppingCart, CartItem
from flask_login import login_required, current_user

bp = Blueprint(
    "products",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/<int:product_id>")
def product_type(product_id):
    product = ProductType.query.get_or_404(product_id)
    sizes = Size.query.filter(
        Size.id.in_(
            db.session.query(ProductItem.size_id).filter(
                ProductItem.product_type_id == product_id, ProductItem.stock_number > 0
            )
        )
    ).all()
    return render_template("product_type/product_type.html", product=product, sizes=sizes)


@bp.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if not current_user.is_authenticated:
        flash("You need to be logged in to add products to cart", "danger")
        return redirect(url_for("auth.login"))
    product_id = request.form.get("product_id")
    size_id = request.form.get("size")
    quantity = int(request.form.get("quantity", 1))

    product_item = ProductItem.query.filter_by(product_type_id=product_id, size_id=size_id).first_or_404()
    quantity_with_cart = quantity

    shopping_cart = (
        ShoppingCart.query.filter_by(auth_user_id=current_user.id).order_by(ShoppingCart.timestamp.desc()).first()
    )
    cart_item = CartItem.query.filter_by(shopping_cart_id=shopping_cart.id, product_item_id=product_item.id).first()
    if cart_item:
        quantity_with_cart += cart_item.quantity

    if product_item.stock_number < quantity_with_cart:
        flash("Sorry, we don't have enough items in stock", "danger")
        return redirect(url_for("products.product_type", product_id=product_id))

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(shopping_cart_id=shopping_cart.id, product_item_id=product_item.id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    flash("Product added to cart", "success")

    return redirect(url_for("products.product_type", product_id=product_id))
