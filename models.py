# Import the necessary libraries
import sqlite3

# Connect to the database
conn = sqlite3.connect("stock_management.db")

# Create the stock item table
conn.execute("""
CREATE TABLE IF NOT EXISTS stock_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    item_description TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL
)
""")

# Create the purchase order table
conn.execute("""
CREATE TABLE IF NOT EXISTS purchase_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date DATE NOT NULL,
    supplier_name TEXT NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (item_id) REFERENCES stock_items(id)
)
""")

# Create the delivery note table
conn.execute("""
CREATE TABLE IF NOT EXISTS delivery_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_date DATE NOT NULL,
    order_id INTEGER NOT NULL,
    delivered_quantity INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES purchase_orders(id)
)
""")

# Create the invoice table
conn.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_date DATE NOT NULL,
    order_id INTEGER NOT NULL,
    invoice_amount REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES purchase_orders(id)
)
""")

# Commit the changes to the database
conn.commit()

# Create a class for stock items
class StockItem:
    def __init__(self, item_name, item_description, quantity, unit_price):
        self.item_name = item_name
        self.item_description = item_description
        self.quantity = quantity
        self.unit_price = unit_price

    def save(self):
        conn.execute("""
        INSERT INTO stock_items (item_name, item_description, quantity, unit_price)
        VALUES (?, ?, ?, ?)
        """, (self.item_name, self.item_description, self.quantity, self.unit_price))
        conn.commit()

    @staticmethod
    def get_all():
        cursor = conn.execute("""
        SELECT * FROM stock_items
        """)
        return [StockItem(*row) for row in cursor.fetchall()]

# Create a class for purchase orders
class PurchaseOrder:
    def __init__(self, order_date, supplier_name, item_id, quantity):
        self.order_date = order_date
        self.supplier_name = supplier_name
        self.item_id = item_id
        self.quantity = quantity

    def save(self):
        conn.execute("""
        INSERT INTO purchase_orders (order_date, supplier_name, item_id, quantity)
        VALUES (?, ?, ?, ?)
        """, (self.order_date, self.supplier_name, self.item_id, self.quantity))
        conn.commit()

    @staticmethod
    def get_all():
        cursor = conn.execute("""
        SELECT * FROM purchase_orders
        """)
        return [PurchaseOrder(*row) for row in cursor.fetchall()]

# Create a class for delivery notes
class DeliveryNote:
    def __init__(self, delivery_date, order_id, delivered_quantity):
        self.delivery_date = delivery_date
        self.order_id = order_id
        self.delivered_quantity = delivered_quantity

    def save(self):
        conn.execute("""
        INSERT INTO delivery_notes (delivery_date, order_id, delivered_quantity)
        VALUES (?, ?, ?)
        """, (self.delivery_date, self.order_id, self.delivered_quantity))
        conn.commit()

        # Deduct the delivered items from the stock levels
        conn.execute("""
        UPDATE stock_items
        SET quantity = quantity - (SELECT delivered_quantity FROM delivery_notes WHERE id = ?)
        WHERE id = (SELECT item_id FROM purchase_orders WHERE id = ?)
        """, (self.id, self.order_id))
        conn.commit()

    @staticmethod
    def get_all():
        cursor = conn.execute("""
        SELECT * FROM delivery_notes
        """)
        return [DeliveryNote(*row) for row in cursor.fetchall()]

# Create a class for invoices
class Invoice:
    def __init__(self, invoice_date, order_id, invoice_amount):
        self.invoice_date = invoice_date
        self.order_id = order_id
        self.invoice_amount = invoice_amount

    def save(self):
        conn.execute("""
        INSERT INTO invoices (invoice_date, order_id, invoice_amount)
        VALUES (?, ?, ?)
        """, (self.invoice_date, self.order_id, self.invoice_amount))
        conn.commit()

    @staticmethod
    def get_all():
        cursor = conn.execute("""
        SELECT * FROM invoices
        """)
        return [Invoice(*row) for row in cursor.fetchall()]

