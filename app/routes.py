from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/products")
def products():
    return render_template("products.html")

@main.route("/contact")
def contact():
    return render_template("contact.html")
