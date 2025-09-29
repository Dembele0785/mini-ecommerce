from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from .models import Product, User
from . import db
import functools

main = Blueprint('main', __name__)

@main.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('main.login'))
        return view(**kwargs)
    return wrapped_view

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
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Connexion réussie !', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Identifiant ou mot de passe incorrect.', 'error')

    return render_template("login.html")


@main.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return redirect(url_for('main.register'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Ce nom d\'utilisateur existe déjà.', 'error')
            return redirect(url_for('main.register'))

        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('main.login'))

    return render_template("register.html")

@main.route("/logout")
def logout():
    session.clear()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.index'))

@main.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_profile':
            g.user.first_name = request.form.get('first_name')
            g.user.last_name = request.form.get('last_name')
            g.user.username = request.form.get('username')
            db.session.commit()
            flash('Profil mis à jour.', 'success')
        elif action == 'change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_new_password = request.form.get('confirm_new_password')

            if not g.user.check_password(current_password):
                flash('Mot de passe actuel incorrect.', 'error')
            elif new_password != confirm_new_password:
                flash('Les nouveaux mots de passe ne correspondent pas.', 'error')
            else:
                g.user.set_password(new_password)
                db.session.commit()
                flash('Mot de passe mis à jour.', 'success')
        return redirect(url_for('main.profile'))
    return render_template("profile.html")