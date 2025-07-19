from flask import render_template, Blueprint
from ..models import ProductType, ProductCategory, db
from flask_login import current_user
from ..utils.admin_utils import products_monthly_reports_hist, cities_monthly_reports_hist
from ..utils.admin_utils import invoices_monthly_reports_hist, products_monthly_reports_pie, admin_records
from datetime import datetime


bp = Blueprint(
    "admin",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/admin",
)


@bp.route("/products/<int:year>/")
def admin_view_products(year=2024):
    lowest_year = admin_records()
    actual_year = datetime.now().year
    years = [i for i in range(lowest_year, actual_year+1)]
    months = [str(i) for i in range(1, 13)]
    months_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    is_info_products = products_monthly_reports_hist(year, months, months_names)
    is_info_categories = products_monthly_reports_pie(year, months, months_names)
    return render_template("admin/admin_products.html", years=years, months=months_names, year=year, 
                           is_info_products=is_info_products, is_info_categories=is_info_categories)

@bp.route("/cities/<int:year>/")
def admin_view_cities(year=2024):
    lowest_year = admin_records()
    actual_year = datetime.now().year
    years = [i for i in range(lowest_year, actual_year+1)]
    months = [str(i) for i in range(1, 13)]
    months_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    is_info = cities_monthly_reports_hist(year, months, months_names)
    return render_template("admin/admin_cities.html", years=years, months=months_names, year=year, is_info=is_info)

@bp.route("/invoices/<int:year>/")
def admin_view_invoices(year=2024):
    lowest_year = admin_records()
    actual_year = datetime.now().year
    years = [i for i in range(lowest_year, actual_year+1)]
    months = [str(i) for i in range(1, 13)]
    months_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    is_info = invoices_monthly_reports_hist(year, months, months_names)
    return render_template("admin/admin_invoices.html", years=years, months=months_names, year=year, is_info=is_info)
