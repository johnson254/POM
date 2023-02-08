from .extensions import db

# StockItem model
class StockItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    quantity = db.Column(db.Integer)
    
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def deduct_quantity(self, quantity):
        self.quantity -= quantity
        db.session.commit()
        
    @staticmethod
    def get_all():
        return StockItem.query.all()
        
    def __repr__(self):
        return "<StockItem {}>".format(self.name)
