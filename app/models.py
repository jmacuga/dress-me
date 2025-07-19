import datetime
from .database import db
from flask_login import UserMixin


class Size(db.Model):
    __tablename__ = "size"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    size_type_id = db.Column(db.Integer, db.ForeignKey("size_type.id", ondelete="CASCADE"), nullable=False, index=True)
    product_item = db.relationship(
        "ProductItem",
        backref="size",
        cascade="all, delete",
    )


class SizeType(db.Model):
    __tablename__ = "size_type"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    size = db.relationship(
        "Size",
        backref="size_type",
        cascade="all, delete",
    )


class ProductType(db.Model):
    __tablename__ = "product_type"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(120))
    color = db.Column(db.String(120))
    db.Column()
    price = db.Column(db.Float, nullable=False, server_default="0.0")
    img_url = db.Column(db.String(200), unique=True)
    product_item = db.relationship(
        "ProductItem",
        backref="product_type",
        cascade="all, delete",
    )
    product_category_id = db.Column(db.Integer, db.ForeignKey("product_category.id", ondelete="CASCADE"), index=True)


class ProductCategory(db.Model):
    __tablename__ = "product_category"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    subcategory_name = db.Column(db.String(120), unique=True, index=True)
    category_name = db.Column(db.String(120), nullable=False, index=True)
    product_type = db.relationship(
        "ProductType",
        backref="product_category",
        cascade="all, delete",
    )
    size_type_id = db.Column(db.Integer, db.ForeignKey("size_type.id", ondelete="CASCADE"), nullable=False)


class ProductItem(db.Model):
    __tablename__ = "product_item"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    stock_number = db.Column(db.Integer, nullable=False, server_default="0")
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey("size.id", ondelete="CASCADE"), nullable=False, index=True)
    product_type_id = db.Column(db.Integer, db.ForeignKey("product_type.id", ondelete="CASCADE"), nullable=False, index=True)
    cart_item = db.relationship(
        "CartItem",
        backref="product_item",
        cascade="all, delete",
    )
    product_monthly_reports = db.relationship("ProductMonthlyReports", backref="product_item")


class CartItem(db.Model):
    __tablename__ = "cart_item"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    shopping_cart_id = db.Column(db.Integer, db.ForeignKey("cart.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, server_default="1")
    product_item_id = db.Column(db.Integer, db.ForeignKey("product_item.id", ondelete="CASCADE"))


class ShoppingCart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    total = db.Column(db.Float, nullable=False, server_default="0.0")
    cart_item = db.relationship(
        "CartItem",
        backref="cart",
        cascade="all, delete",
    )
    order = db.relationship("Order", backref="cart")
    auth_user_id = db.Column(db.Integer, db.ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False, index=True)


class AuthUser(UserMixin, db.Model):
    __tablename__ = "auth_user"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cart = db.relationship(
        "ShoppingCart",
        backref="auth_user",
        cascade="all, delete",
    )


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    total = db.Column(db.Float, nullable=False, server_default="0.0")
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    order_status_id = db.Column(db.Integer, db.ForeignKey("order_status.id", ondelete="SET NULL"))
    delivery_method_id = db.Column(db.Integer, db.ForeignKey("delivery_method.id", ondelete="SET NULL"))
    address_id = db.Column(db.Integer, db.ForeignKey("address.id", ondelete="SET NULL"))
    invoice = db.relationship("Invoice", backref="order")
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id", ondelete="SET NULL"))

    def update_stock(self):
        for cart_item in self.cart.cart_item:
            product_item = ProductItem.filter_by(id=cart_item.product_item_id).first()

            if product_item.stock_number - cart_item.quantity < 0:
                raise ValueError("Not enough stock")
            product_item.stock_number -= cart_item.quantity
            product_item.timestamp = datetime.datetime.utcnow()
            product_item.save()


class DeliveryMethod(db.Model):
    __tablename__ = "delivery_method"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Float, unique=True, nullable=False)
    order = db.relationship("Order", backref="delivery_method")


class OrderStatus(db.Model):
    __tablename__ = "order_status"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    order = db.relationship("Order", backref="order_status")


class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    street = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    zip_code = db.Column(db.String(120), nullable=False)
    order = db.relationship("Order", backref="address")


class Invoice(db.Model):
    __tablename__ = "invoice"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    total = db.Column(db.Float, nullable=False, server_default="0.0")
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id", ondelete="SET NULL"))


class CityMonthlyReports(db.Model):
    __tablename__ = "city_monthly_reports"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    city = db.Column(db.String(120), nullable=False)
    month = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)


class InvoiceMonthlyReports(db.Model):
    __tablename__ = "invoice_monthly_reports"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    month = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)


class ProductMonthlyReports(db.Model):
    __tablename__ = "product_monthly_reports"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    product_item_id = db.Column(db.Integer, db.ForeignKey("product_item.id", ondelete="SET NULL"))
    month = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

