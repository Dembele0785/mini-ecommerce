from flask import Blueprint, render_template
from .models import Product
from app.models import Product  # ajoute cette ligne si ce n'est pas déjà fait

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/products")
def products():
    all_products = Product.query.all()  # récupère tous les produits de la base
    return render_template("products.html", products=all_products)

@main.route("/contact")
def contact():
    return render_template("contact.html")
