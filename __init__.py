from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#local imports
from models import StockItem, PurchaseOrder, DeliveryNote, Invoice

def create_app():
    app = Flask(__name__)
    db = SQLAlchemy()

    return app