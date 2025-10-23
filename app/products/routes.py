from flask import render_template, request
from . import products_bp

@products_bp.route("/products")
def product_list():
    products = [
        {"name": "Laptop", "price": 1200},
        {"name": "Mouse", "price": 25},
        {"name": "Keyboard", "price": 70}
    ]
    return render_template("products/list.html", products=products)
