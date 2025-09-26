from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import Product

main = Blueprint('main', __name__)

@main.route("/")
def index():
    products = Product.query.limit(3).all()
    return render_template("index.html", products=products)

@main.route("/products")
def products():
    products = Product.query.all()
    return render_template("products.html", products=products)

@main.route("/contact")
def contact():
    return render_template("contact.html")

@main.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")
    if not product_id:
        flash("Produit introuvable.", "error")
        return redirect(request.referrer or url_for("main.index"))

    try:
        pid = int(product_id)
    except ValueError:
        flash("Identifiant produit invalide.", "error")
        return redirect(request.referrer or url_for("main.index"))

    qty = request.form.get("quantity", 1)
    try:
        qty = int(qty)
        if qty < 1:
            qty = 1
    except ValueError:
        qty = 1

    product = Product.query.get(pid)
    if not product:
        flash("Produit introuvable dans la base.", "error")
        return redirect(request.referrer or url_for("main.index"))

    cart = session.get("cart", {})
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session["cart"] = cart
    flash(f"Ajouté {qty} × {product.name} au panier.", "success")
    return redirect(request.referrer or url_for("main.index"))


@main.route("/cart")
def cart():
    cart = session.get("cart", {})
    items = []
    total = 0.0

    for pid_str, qty in cart.items():
        try:
            pid = int(pid_str)
        except ValueError:
            continue
        product = Product.query.get(pid)
        if not product:
            continue
        subtotal = product.price * qty
        total += subtotal
        items.append({"product": product, "quantity": qty, "subtotal": subtotal})

    return render_template("cart.html", items=items, total=total)


@main.route("/update_cart", methods=["POST"])
def update_cart():
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")
    if not product_id:
        return redirect(url_for("main.cart"))
    try:
        pid = int(product_id)
        qty = int(quantity)
    except (ValueError, TypeError):
        return redirect(url_for("main.cart"))

    cart = session.get("cart", {})
    if qty <= 0:
        cart.pop(str(pid), None)
    else:
        cart[str(pid)] = qty
    session["cart"] = cart
    flash("Panier mis à jour.", "success")
    return redirect(url_for("main.cart"))


@main.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    flash("Produit retiré du panier.", "info")
    return redirect(url_for("main.cart"))


@main.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    flash("Panier vidé.", "info")
    return redirect(url_for("main.index"))


@main.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")
