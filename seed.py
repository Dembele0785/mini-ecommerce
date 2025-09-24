from app import create_app, db
from app.models import Product

app = create_app()

with app.app_context():
    db.create_all()  # recrée les tables

    # Créer quelques produits avec image
    p1 = Product(name="Produit 1", price=10, image="images/produit1.jpg")
    p2 = Product(name="Produit 2", price=20, image="images/produit2.jpg")
    p3 = Product(name="Produit 3", price=30, image="images/produit3.jpg")

    db.session.add_all([p1, p2, p3])
    db.session.commit()

    print("✅ Produits insérés avec images !")
