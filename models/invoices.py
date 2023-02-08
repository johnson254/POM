# stock_management/blueprints/invoices.py
from flask import Blueprint, render_template, request
from models import Invoice, db

bp = Blueprint('invoices', __name__)

@bp.route('/invoices')
def index():
    invoices = Invoice.query.all()
    return render_template('invoices/index.html', invoices=invoices)

@bp.route('/invoices/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        invoice = Invoice(request.form['delivery_note_id'], request.form['total'])
        db.session.add(invoice)
        db.session.commit()
        return redirect(url_for('invoices.index'))
    return render_template('invoices/create.html')

@bp.route('/invoices/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    invoice = Invoice.query.get(id)
    if request.method == 'POST':
        invoice.delivery_note_id = request.form['delivery_note_id']
        invoice.total = request.form['total']
        db.session.commit()
        return redirect(url_for('invoices.index'))
    return render_template('invoices/edit.html', invoice=invoice)

@bp.route('/invoices/<int:id>/delete')
def delete(id):
    invoice = Invoice.query.get(id)
    db.session.delete(invoice)
    db.session.commit()
    return redirect(url_for('invoices.index'))
