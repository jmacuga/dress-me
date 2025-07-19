import pytest
from flask import url_for
from app.models import AuthUser, ProductType, Size, ProductItem, ShoppingCart, CartItem, db
from app.views.auth import create_shopping_cart
from flask_login import login_user

def test_add_to_cart(test_client):
    with test_client:
        user = AuthUser.query.filter_by(username='testuser').first()
        create_shopping_cart(user_id=user.id)

        product = ProductType.query.first()
        size = Size.query.first()
        quantity = 1
        
        cart = ShoppingCart.query.filter_by(auth_user_id=user.id).first()
        print(cart.id)
        cart_item = CartItem(shopping_cart_id=cart.id, product_item_id=product.id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()

        response = test_client.post(url_for('products.add_to_cart'), data={
            'product_id': product.id,
            'size': size.id,
            'quantity': quantity
        }, follow_redirects=True)
        
        print(ProductItem.query.filter_by(product_type_id=product.id, size_id=size.id).first())
        assert response.status_code == 200
        assert cart.id is not None
        assert cart_item is not None
        assert cart_item.quantity == 1


def test_cart_detail(test_client):
    with test_client:

        user = AuthUser.query.filter_by(username='testuser').first()
        login_user(user=user)
        response = test_client.get(url_for('cart.cart_detail'))
        assert response.status_code == 200

        # Verify cart details
        cart = ShoppingCart.query.filter_by(auth_user_id=user.id).first()
        assert cart is not None
        


def test_remove_from_cart(test_client):
    with test_client:
        user = AuthUser.query.filter_by(username='testuser').first()
        login_user(user)

        cart = ShoppingCart.query.filter_by(auth_user_id=user.id).first()
        cart_item = CartItem.query.filter_by(shopping_cart_id=cart.id).first()

        response = test_client.post(url_for('cart.remove_from_cart'), data={
            'cart_item_id': cart_item.id
        }, follow_redirects=True)

        assert response.status_code == 200

        cart_item = CartItem.query.filter_by(id=cart_item.id).first()
        assert cart_item is None
