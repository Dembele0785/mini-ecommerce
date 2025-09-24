from app import create_app, db
from app.models import Product

app = create_app()

with app.app_context():
    db.create_all()  # crée les tables si elles n'existent pas déjà

    # Créer quelques produits
    p1 = Product(name="Produit 1", price=10)
    p2 = Product(name="Produit 2", price=20)
    p3 = Product(name="Produit 3", price=30)

    db.session.add_all([p1, p2, p3])
    db.session.commit()

    print("✅ Produits insérés avec succès !")
