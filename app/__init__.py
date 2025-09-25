from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# On initialise SQLAlchemy en dehors de create_app
db = SQLAlchemy()

def create_app():
    print("--- Inside create_app ---")
    app = Flask(__name__)

    # Config DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mini_ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev' # A changer pour la production

    # Initialiser la DB avec l'app
    db.init_app(app)

    # Importer et enregistrer les Blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
