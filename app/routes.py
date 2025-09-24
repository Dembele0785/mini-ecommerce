from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/products")
def products():
    produits = [
        {"name": "Produit 1", "price": 10},
        {"name": "Produit 2", "price": 20},
        {"name": "Produit 3", "price": 30},
    ]
    return render_template("products.html", produits=produits)

@main.route("/contact")
def contact():
    return render_template("contact.html")
