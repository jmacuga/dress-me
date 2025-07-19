from flask import (
    render_template,
    Blueprint,
    request,
    redirect,
    url_for,
    flash,
)
from ..models import db, AuthUser, ShoppingCart
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates/",
    static_folder="static",
    url_prefix="/auth",
)


@bp.route("/signup")
def signup():
    return render_template("auth/signup.html")


@bp.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    user_email = AuthUser.query.filter_by(email=email).first()
    user_name = AuthUser.query.filter_by(username=username).first()

    if user_email:
        flash("Email address already exists.")
        return redirect(url_for("auth.signup"))
    if user_name:    
        flash("Username already exists.")
        return redirect(url_for("auth.signup"))
    

    new_user = AuthUser(
        email=email,
        username=username,
        password=generate_password_hash(password, method="pbkdf2:sha256"),
    )
    db.session.add(new_user)
    db.session.commit()
    
    create_shopping_cart(new_user.id)

    flash("You have successfully signed up.")
    return redirect(url_for("auth.login"))


@bp.route("/login")
def login():
    return render_template("auth/login.html")


@bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = AuthUser.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for("main.home"))

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.home"))

def create_shopping_cart(user_id):
    shopping_cart = ShoppingCart(auth_user_id=user_id, total=0)
    db.session.add(shopping_cart)
    db.session.commit()
