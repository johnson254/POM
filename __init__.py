from flask import Flask 
#local imports
#from models import StockItem, PurchaseOrder, DeliveryNote, Invoice
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///db.sqlite3'
    app.config[SQLALCHEMY_TRACK_MODIFICATIONS] = False

    db.init_app(app)

    return app