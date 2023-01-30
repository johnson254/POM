from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

# PurchaseOrder model
class PurchaseOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date)
    supplier = db.Column(db.String(30))
    items = db.Column(db.String(100))  # comma-separated string of item ids
    
    def __init__(self, order_date, supplier, items):
        self.order_date = order_date
        self.supplier = supplier
        self.items = ",".join(str(item_id) for item_id in items)
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def get_all():
        return PurchaseOrder.query.all()
        
    def __repr__(self):
        return "<PurchaseOrder {}>".format(self.id)

# DeliveryNote model
class DeliveryNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_date = db.Column(db.Date)
    order_id = db.Column(db.Integer, db.ForeignKey("purchase_order.id"))
    order = db.relationship("PurchaseOrder", back_populates="delivery_notes")
    
    def __init__(self, delivery_date, order_id):
        self.delivery_date = delivery_date
        self.order_id = order_id
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
        # Deduct item quantities from stock
        order = PurchaseOrder.query.get(self.order_id)
        item_ids = [int(item_id) for item_id in order.items.split(",")]
        for item_id in item_ids:
            item = StockItem.query.get(item_id)
            item.deduct_quantity(1)
        
    @staticmethod
    def get_all():
        return DeliveryNote.query.all()
        
    def __repr__(self):
        return "<DeliveryNote {}>".format(self.id)

# Invoice model
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_date = db.Column(db.Date)
    delivery_note_id = db.Column(db.Integer, db.ForeignKey("delivery_note.id"))
    delivery_note = db.relationship("DeliveryNote", back_populates="invoices")
    
    def __init__(self, invoice_date, delivery_note_id):
        self.invoice_date = invoice_date
        self.delivery_note_id = delivery_note_id
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def get_all():
        return Invoice.query.all()
        
    def __repr__(self):
        return "<Invoice {}>".format(self.id)

