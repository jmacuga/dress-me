from flask import render_template, Blueprint, request, url_for, redirect
from ..models import ProductType, ProductCategory
from flask_login import current_user
from sqlalchemy import distinct

bp = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)
page_limit = 18

@bp.route("/")
@bp.route("/category/<string:category_name>")
@bp.route("/subcategory/<int:subcategory_id>")
def home(category_name=None, subcategory_id=None):
    page = request.args.get('page', 1, type=int)
    color_filter = request.args.get('color', None)
    min_price = request.args.get('min_price', None, type=float)
    max_price = request.args.get('max_price', None, type=float)

    categories = ProductCategory.query.order_by(ProductCategory.category_name, ProductCategory.subcategory_name).all()

    query = ProductType.query
    if category_name:
        # Pobierz wszystkie podkategorie w ramach tej głównej kategorii
        subcategories = ProductCategory.query.filter_by(category_name=category_name).all()
        subcategory_ids = [subcategory.id for subcategory in subcategories]
        query = query.filter(ProductType.product_category_id.in_(subcategory_ids))
    elif subcategory_id:
        query = query.filter_by(product_category_id=subcategory_id)
    if color_filter:
        query = query.filter_by(color=color_filter)
    if min_price is not None:
        query = query.filter(ProductType.price >= min_price)
    if max_price is not None:
        query = query.filter(ProductType.price <= max_price)

    total_products = query.count()
    products = query.offset((page - 1) * page_limit).limit(page_limit).all()

    colors = ProductType.query.with_entities(distinct(ProductType.color)).order_by(ProductType.color).all()

    pagination = {
        'page': page,
        'per_page': page_limit,
        'total': total_products,
        'pages': (total_products + page_limit - 1) // page_limit,  # number of pages
    }

    return render_template("main/main.html", 
                           products=products, 
                           categories=categories, 
                           current_user=current_user,
                           colors=[color[0] for color in colors],
                           pagination=pagination,
                           color_filter=color_filter,
                           category_name=category_name,
                           subcategory_id=subcategory_id,
                           min_price=min_price,
                           max_price=max_price)
