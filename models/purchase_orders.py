# stock_management/blueprints/purchase_orders.py
from flask import Blueprint, render_template, request
from models import PurchaseOrder, db

bp = Blueprint('purchase_orders', __name__)

@bp.route('/purchase_orders')
def index():
    purchase_orders = PurchaseOrder.query.all()
    return render_template('purchase_orders/index.html', purchase_orders=purchase_orders)

@bp.route('/purchase_orders/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        purchase_order = PurchaseOrder(request.form['supplier_id'], request.form['order_date'])
        db.session.add(purchase_order)
        db.session.commit()
        return redirect(url_for('purchase_orders.index'))
    return render_template('purchase_orders/create.html')

@bp.route('/purchase_orders/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    purchase_order = PurchaseOrder.query.get(id)
    if request.method == 'POST':
        purchase_order.supplier_id = request.form['supplier_id']
        purchase_order.order_date = request.form['order_date']
        db.session.commit()
        return redirect(url_for('purchase_orders.index'))
    return render_template('purchase_orders/edit.html', purchase_order=purchase_order)

@bp.route('/purchase_orders/<int:id>/delete')
def delete(id):
    purchase_order = PurchaseOrder.query.get(id)
    db.session.delete(purchase_order)
    db.session.commit()
    return redirect(url_for('purchase_orders.index'))
