from flask import  render_template, request

from extensions import db


# Home page
@app.route("/")
def index():
    return "Stock Management System"

# Stock items
@app.route("/stock-items")
def stock_items():
    items = StockItem.get_all()
    return render_template("stock_items.html", items=items)

#route for getting and posting stock items
@app.route("/add-stock-item", methods=["GET", "POST"])
def add_stock_item():
    if request.method == "POST":
        item_name = request.form["item_name"]
        quantity = int(request.form["quantity"])
        item = StockItem(item_name, quantity)
        item.save()
    return render_template("add_stock_item.html")

# Purchase orders
@app.route("/purchase-orders")
def purchase_orders():
    orders = PurchaseOrder.get_all()
    return render_template("purchase_orders.html", orders=orders)

@app.route("/add-purchase-order", methods=["GET", "POST"])
def add_purchase_order():
    if request.method == "POST":
        order_date = request.form["order_date"]
        supplier_name = request.form["supplier_name"]
        item_id = int(request.form["item_id"])
        quantity = int(request.form["quantity"])
        order = PurchaseOrder(order_date, supplier_name, item_id, quantity)
        order.save()
    items = StockItem.get_all()
    return render_template("add_purchase_order.html", items=items)

# Delivery notes
@app.route("/delivery-notes")
def delivery_notes():
    notes = DeliveryNote.get_all()
    return render_template("delivery_notes.html", notes=notes)

@app.route("/add-delivery-note", methods=["GET", "POST"])
def add_delivery_note():
    if request.method == "POST":
        delivery_date = request.form["delivery_date"]
        order_id = int(request.form["order_id"])
        delivered_quantity = int(request.form["delivered_quantity"])
        note = DeliveryNote(delivery_date, order_id, delivered_quantity)
        note.save()
    orders = PurchaseOrder.get_all()
    return render_template("add_delivery_note.html", orders=orders)

# Invoices
@app.route("/invoices")
def invoices():
    invoices = Invoice.get_all()
    return render_template("invoices.html", invoices=invoices)

@app.route("/add-invoice", methods=["GET", "POST"])
def add_invoice():
    if request.method == "POST":
        invoice_date = request.form["invoicedate"]
        order_id = int(request.form["order_id"])
        invoice_amount = float(request.form["invoice_amount"])
        invoice = Invoice(invoice_date, order_id, invoice_amount)
        invoice.save()
    orders = PurchaseOrder.get_all()
    return render_template("add_invoice.html", orders=orders)

#reports
@app.route('/reports')
def reports():
    items = StockItem.get_all()
