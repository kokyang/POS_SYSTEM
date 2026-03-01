from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Database
from models import Category, Item, Sale
from datetime import datetime

app = Flask(__name__)
Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pos')
def pos():
    items = Item.get_all()
    categories = Category.get_all()
    return render_template('pos.html', items=items, categories=categories)

@app.route('/inventory')
def inventory():
    items = Item.get_all()
    categories = Category.get_all()
    return render_template('inventory.html', items=items, categories=categories)

@app.route('/reports')
def reports():
    return render_template('reports.html')

# API endpoints
@app.route('/api/categories', methods=['GET', 'POST', 'DELETE'])
def api_categories():
    if request.method == 'GET':
        categories = Category.get_all()
        return jsonify([{'id': c[0], 'name': c[1]} for c in categories])
    
    elif request.method == 'POST':
        data = request.json
        Category.add(data['name'])
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        data = request.json
        Category.delete(data['id'])
        return jsonify({'success': True})

@app.route('/api/items', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_items():
    if request.method == 'GET':
        items = Item.get_all()
        return jsonify([{
            'id': i[0], 'name': i[1], 'category': i[2],
            'price': i[3], 'stock': i[4], 'barcode': i[6] if len(i) > 6 else None
        } for i in items])

    elif request.method == 'POST':
        data = request.json
        Item.add(data['name'], data['category_id'], data['price'], data['stock'],
                 barcode=data.get('barcode'))
        return jsonify({'success': True})

    elif request.method == 'PUT':
        data = request.json
        Item.update(data['id'], data['name'], data['category_id'], data['price'], data['stock'],
                    barcode=data.get('barcode'))
        return jsonify({'success': True})

    elif request.method == 'DELETE':
        data = request.json
        Item.delete(data['id'])
        return jsonify({'success': True})

@app.route('/api/lookup-barcode/<path:query>')
def api_lookup_barcode(query):
    # Try exact barcode match first
    item = Item.get_by_barcode(query)
    if item:
        return jsonify({
            'found': True,
            'item': {'id': item[0], 'name': item[1], 'price': item[3], 'stock': item[4], 'barcode': item[6]}
        })
    # Fallback: search by name
    results = Item.search_by_name(query)
    if len(results) == 1:
        i = results[0]
        return jsonify({
            'found': True,
            'item': {'id': i[0], 'name': i[1], 'price': i[3], 'stock': i[4], 'barcode': i[6]}
        })
    return jsonify({'found': False, 'matches': len(results)})

@app.route('/api/restock', methods=['POST'])
def api_restock():
    data = request.json
    Item.update_stock(data['id'], data['quantity'])
    return jsonify({'success': True})

@app.route('/api/checkout', methods=['POST'])
def api_checkout():
    data = request.json
    sale_id = Sale.create_sale(data['items'], data['total'])
    return jsonify({'success': True, 'sale_id': sale_id})

@app.route('/api/revenue/<int:year>/<int:month>')
def api_revenue(year, month):
    revenue = Sale.get_monthly_revenue(year, month)
    return jsonify({'revenue': revenue})

@app.route('/api/sales')
def api_sales():
    sales = Sale.get_all_sales()
    return jsonify([{
        'id': s[0], 'date': s[1], 'total': s[2]
    } for s in sales])

@app.route('/api/sales/<int:sale_id>')
def api_sale_details(sale_id):
    details = Sale.get_sale_details(sale_id)
    return jsonify([{
        'name': d[0], 'quantity': d[1], 'price': d[2], 'subtotal': d[3]
    } for d in details])

@app.route('/api/today-sales')
def api_today_sales():
    data = Sale.get_today_sales()
    return jsonify(data)

@app.route('/api/top-selling')
def api_top_selling():
    items = Sale.get_top_selling_items()
    return jsonify([{
        'name': i[0], 'quantity': i[1], 'revenue': i[2]
    } for i in items])

@app.route('/api/sales-range/<start_date>/<end_date>')
def api_sales_range(start_date, end_date):
    sales = Sale.get_sales_by_date_range(start_date, end_date)
    return jsonify([{
        'date': s[0], 'count': s[1], 'total': s[2]
    } for s in sales])

@app.route('/api/daily-reconciliation')
def api_daily_reconciliation():
    data = Sale.get_daily_reconciliation()
    return jsonify(data)

@app.route('/api/best-selling-analysis')
def api_best_selling_analysis():
    data = Sale.get_best_selling_analysis()
    return jsonify(data)

@app.route('/api/transactions-by-date/<start_date>/<end_date>')
def api_transactions_by_date(start_date, end_date):
    transactions = Sale.get_transactions_by_date(start_date, end_date)
    return jsonify([{
        'id': t[0], 'date': t[1], 'total': t[2]
    } for t in transactions])

@app.route('/api/monthly-report/<int:year>/<int:month>')
def api_monthly_report(year, month):
    data = Sale.get_monthly_report(year, month)
    return jsonify(data)

@app.route('/api/sales-summary/<start_date>/<end_date>')
def api_sales_summary(start_date, end_date):
    data = Sale.get_sales_summary(start_date, end_date)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
