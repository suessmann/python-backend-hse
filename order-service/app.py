from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)
product_service_url = 'localhost:8081'


# Class for Order Entity
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order_products = db.relationship('OrderProduct', backref='order', lazy=True)


class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)


# Create an order
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(status=data['status'], total_price=data['total_price'])
    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'})


# Get all orders
@app.route('/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    result = []
    for order in orders:

        # Request product information from another microservice
        product_response = requests.get(f'http://{product_service_url}/products/{order.order_products}')
        if product_response.status_code != 200:
            return jsonify({'message': 'Failed to retrieve product information'})

        order_data = {
            'id': order.id,
            'status': order.status,
            'total_price': order.total_price,
            'product': product_response.json()
        }
        result.append(order_data)
    return jsonify(result)


# Get an order by ID
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'})

    # Request product information from another microservice
    product_response = requests.get(f'http://{product_service_url}/products/{order.order_products}')
    if product_response.status_code != 200:
        return jsonify({'message': 'Failed to retrieve product information'})

    order_data = {
        'id': order.id,
        'status': order.status,
        'total_price': order.total_price,
        'product': product_response.json()
    }
    return jsonify(order_data)


# Update an order
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'})
    data = request.get_json()
    order.status = data['status']
    order.total_price = data['total_price']
    db.session.commit()
    return jsonify({'message': 'Order updated successfully'})


# Delete an order
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'})
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'})


# Create an order product
@app.route('/order_products', methods=['POST'])
def create_order_product():
    data = request.get_json()
    order_product = OrderProduct(order_id=data['order_id'], product_id=data['product_id'])
    db.session.add(order_product)
    db.session.commit()
    return jsonify({'message': 'Order product created successfully'})


# Get all order products for an order
@app.route('/order_products/<int:order_id>', methods=['GET'])
def get_order_products(order_id):
    order_products = OrderProduct.query.filter_by(order_id=order_id).all()
    result = []
    for order_product in order_products:
        order_product_data = {
            'id': order_product.id,
            'product_id': order_product.product_id,
            'order_id': order_product.order_id
        }
        result.append(order_product_data)
    return jsonify(result)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
