from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

# Class for Product Entity
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price


# Endpoint for getting list of products
@app.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {'id': product.id, 'name': product.name, 'price': product.price}
        output.append(product_data)
    return jsonify({'products': output})


# Endpoint for getting product by id
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'})
    product_data = {'id': product.id, 'name': product.name, 'price': product.price}
    return jsonify({'product': product_data})


# Endpoint for creating product
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(name=data['name'], price=data['price'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'})


# Endpoint for updating product
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'product not found'})
    data = request.get_json()
    product.name = data['name']
    product.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})


# Endpoint for deleting product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'})
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
