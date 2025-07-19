import pytest
from app.models import db
from app.models import (Size, SizeType, ProductType, ProductCategory, ProductItem, CartItem, ShoppingCart, AuthUser, 
                          Order, DeliveryMethod, OrderStatus, Address, Invoice, CityMonthlyReports, 
                          InvoiceMonthlyReports, ProductMonthlyReports)
from flask_sqlalchemy import SQLAlchemy

def test_size(test_client):
    size_type = SizeType(id = 100000, name='Clothing')
    db.session.add(size_type)
    db.session.commit()

    size = Size(id = 100000, name='Medium', size_type_id=size_type.id)
    db.session.add(size)
    db.session.commit()

    assert size.id is not None
    assert size.name == 'Medium'
    assert size.size_type_id == size_type.id


def test_product_type(test_client):
    category = ProductCategory(id = 100000, subcategory_name='Shirts', category_name='Clothing', size_type_id=1)
    db.session.add(category)
    db.session.commit()

    product_type = ProductType(id = 100000, name='T-shirt', color='Red', price=19.99, img_url='http://example.com/tshirt.png', product_category_id=category.id)
    db.session.add(product_type)
    db.session.commit()

    assert product_type.id is not None
    assert product_type.name == 'T-shirt'
    assert product_type.color == 'Red'
    assert product_type.price == 19.99
    assert product_type.img_url == 'http://example.com/tshirt.png'
    assert product_type.product_category_id == category.id

def test_product_item(test_client):
    size = Size(id = 100001, name='Large', size_type_id=1)
    db.session.add(size)
    db.session.commit()

    product_type = ProductType(id = 100001, name='Hoodie', color='Blue', price=39.99, img_url='http://example.com/hoodie.png', product_category_id=1)
    db.session.add(product_type)
    db.session.commit()

    product_item = ProductItem(id = 100001, stock_number=50, size_id=size.id, product_type_id=product_type.id)
    db.session.add(product_item)
    db.session.commit()

    assert product_item.id is not None
    assert product_item.stock_number == 50
    assert product_item.size_id == size.id
    assert product_item.product_type_id == product_type.id

def test_cart_item(test_client):
    auth_user = AuthUser(id = 100002, username='testuser1', password='password', email='test1@example.com')
    db.session.add(auth_user)
    db.session.commit()

    cart = ShoppingCart(id = 100002, auth_user_id=auth_user.id)
    db.session.add(cart)
    db.session.commit()

    product_item = ProductItem(id = 100002, stock_number=100, size_id=1, product_type_id=100001)
    db.session.add(product_item)
    db.session.commit()

    cart_item = CartItem(id = 100002, shopping_cart_id=cart.id, quantity=2, product_item_id=product_item.id)
    db.session.add(cart_item)
    db.session.commit()

    assert cart_item.id is not None
    assert cart_item.shopping_cart_id == cart.id
    assert cart_item.quantity == 2
    assert cart_item.product_item_id == product_item.id

def test_order(test_client):
    delivery_method = DeliveryMethod(id = 100003, name='Express', price=9.99)
    db.session.add(delivery_method)
    db.session.commit()

    order_status = OrderStatus(id = 100003, name='Pending')
    db.session.add(order_status)
    db.session.commit()

    address = Address(id = 100003, street='123 Main St', city='Hometown', country='Country', zip_code='12345')
    db.session.add(address)
    db.session.commit()

    cart = ShoppingCart(id = 100003, auth_user_id=100002)
    db.session.add(cart)
    db.session.commit()

    order = Order(id = 100003, total=49.99, cart_id=cart.id, delivery_method_id=delivery_method.id, order_status_id=order_status.id, address_id=address.id)
    db.session.add(order)
    db.session.commit()

    assert order.id is not None
    assert order.total == 49.99
    assert order.cart_id == cart.id
    assert order.delivery_method_id == delivery_method.id
    assert order.order_status_id == order_status.id
    assert order.address_id == address.id

def test_invoice(test_client):
    order = Order(id = 100004, total=49.99, cart_id=100002, delivery_method_id=1, order_status_id=1, address_id=100003)
    db.session.add(order)
    db.session.commit()

    invoice = Invoice(id = 100004, total=49.99, order_id=order.id)
    db.session.add(invoice)
    db.session.commit()

    assert invoice.id is not None
    assert invoice.total == 49.99
    assert invoice.order_id == order.id

def test_reports_city(test_client):
    city_report = CityMonthlyReports(id = 100005, city='New York', month='January', year=2023, count=100, total=5000.0)
    db.session.add(city_report)
    db.session.commit()

    assert city_report.id is not None
    assert city_report.city == 'New York'
    assert city_report.month == 'January'
    assert city_report.year == 2023
    assert city_report.count == 100
    assert city_report.total == 5000.0

def test_reports_invoice(test_client):

    invoice_report = InvoiceMonthlyReports(id = 100005, month='January', year=2023, count=50, total=2500.0)
    db.session.add(invoice_report)
    db.session.commit()

    assert invoice_report.id is not None
    assert invoice_report.month == 'January'
    assert invoice_report.year == 2023
    assert invoice_report.count == 50
    assert invoice_report.total == 2500.0

def test_reports_product(test_client):
    product_report = ProductMonthlyReports(id = 100005, product_item_id=1, month='January', year=2023, count=20, total=1000.0)
    db.session.add(product_report)
    db.session.commit()

    assert product_report.id is not None
    assert product_report.product_item_id == 1
    assert product_report.month == 'January'
    assert product_report.year == 2023
    assert product_report.count == 20
    assert product_report.total == 1000.0
