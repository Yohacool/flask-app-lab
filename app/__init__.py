from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("../config.py")
app.secret_key = "A#qwe123"

from . import routes

from .users import users_bp
from .products import products_bp

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)