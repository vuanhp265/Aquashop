from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aquashop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Fish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    species = db.Column(db.String(120))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Accessory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    items = db.Column(db.Text)  # JSON string list of items {type:'fish'|'accessory', id, qty, price}
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_request
def create_tables():
    db.create_all()

# --- Fish endpoints ---
@app.route('/api/fish', methods=['GET'])
def list_fish():
    q = Fish.query.all()
    return jsonify([{
        'id': f.id, 'name': f.name, 'species': f.species, 'price': f.price, 'stock': f.stock
    } for f in q])

@app.route('/api/fish', methods=['POST'])
def add_fish():
    data = request.json
    f = Fish(name=data.get('name'), species=data.get('species'), price=data.get('price',0), stock=data.get('stock',0))
    db.session.add(f); db.session.commit()
    return jsonify({'message':'created','id':f.id}), 201

@app.route('/api/fish/<int:id>', methods=['PUT'])
def update_fish(id):
    f = Fish.query.get_or_404(id)
    data = request.json
    f.name = data.get('name', f.name)
    f.species = data.get('species', f.species)
    f.price = data.get('price', f.price)
    f.stock = data.get('stock', f.stock)
    db.session.commit()
    return jsonify({'message':'updated'})

@app.route('/api/fish/<int:id>', methods=['DELETE'])
def delete_fish(id):
    f = Fish.query.get_or_404(id)
    db.session.delete(f); db.session.commit()
    return jsonify({'message':'deleted'})

# --- Accessory endpoints ---
@app.route('/api/accessories', methods=['GET'])
def list_accessories():
    q = Accessory.query.all()
    return jsonify([{
        'id': a.id, 'name': a.name, 'category': a.category, 'price': a.price, 'stock': a.stock
    } for a in q])

@app.route('/api/accessories', methods=['POST'])
def add_accessory():
    data = request.json
    a = Accessory(name=data.get('name'), category=data.get('category'), price=data.get('price',0), stock=data.get('stock',0))
    db.session.add(a); db.session.commit()
    return jsonify({'message':'created','id':a.id}), 201

@app.route('/api/accessories/<int:id>', methods=['PUT'])
def update_accessory(id):
    a = Accessory.query.get_or_404(id)
    data = request.json
    a.name = data.get('name', a.name)
    a.category = data.get('category', a.category)
    a.price = data.get('price', a.price)
    a.stock = data.get('stock', a.stock)
    db.session.commit()
    return jsonify({'message':'updated'})

@app.route('/api/accessories/<int:id>', methods=['DELETE'])
def delete_accessory(id):
    a = Accessory.query.get_or_404(id)
    db.session.delete(a); db.session.commit()
    return jsonify({'message':'deleted'})

# --- Orders ---
import json as _json

@app.route('/api/orders', methods=['GET'])
def list_orders():
    orders = Order.query.order_by(Order.created_at.desc()).limit(200).all()
    return jsonify([{
        'id': o.id, 'customer_name': o.customer_name, 'items': _json.loads(o.items), 'total': o.total, 'status': o.status, 'created_at': o.created_at.isoformat()
    } for o in orders])

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    items = data.get('items', [])
    total = float(data.get('total', 0))
    o = Order(customer_name=data.get('customer_name',''), items=_json.dumps(items), total=total)
    db.session.add(o); db.session.commit()
    return jsonify({'message':'created','id':o.id}), 201

@app.route('/api/orders/<int:id>', methods=['PUT'])
def update_order(id):
    o = Order.query.get_or_404(id)
    data = request.json
    o.status = data.get('status', o.status)
    db.session.commit()
    return jsonify({'message':'updated'})

# --- Stats ---
@app.route('/api/stats/summary', methods=['GET'])
def stats_summary():
    total_fish = Fish.query.count()
    total_accessories = Accessory.query.count()
    total_orders = Order.query.count()
    revenue = 0.0
    for o in Order.query.all():
        revenue += o.total or 0.0
    return jsonify({
        'total_fish': total_fish,
        'total_accessories': total_accessories,
        'total_orders': total_orders,
        'total_revenue': revenue
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
