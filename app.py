from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
db = SQLAlchemy(app)

class PetProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

@app.route('/pets', methods=['GET'])
def get_all_pets():
    pets = PetProduct.query.all()
    output = []
    for pet in pets:
        pet_data = {'id': pet.id, 'name': pet.name, 'price': pet.price}
        output.append(pet_data)
    return jsonify({'pets': output})

@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    pet = PetProduct.query.get(pet_id)
    if not pet:
        return jsonify({'message': 'Pet not found'})
    pet_data = {'id': pet.id, 'name': pet.name, 'price': pet.price}
    return jsonify({'pet': pet_data})

@app.route('/pets', methods=['POST'])
def create_pet():
    data = request.get_json()
    pet = PetProduct(name=data['name'], price=data['price'])
    db.session.add(pet)
    db.session.commit()
    return jsonify({'message': 'Pet created successfully'})

@app.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    pet = PetProduct.query.get(pet_id)
    if not pet:
        return jsonify({'message': 'Pet not found'})
    data = request.get_json()
    pet.name = data['name']
    pet.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Pet updated successfully'})

@app.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    pet = PetProduct.query.get(pet_id)
    if not pet:
        return jsonify({'message': 'Pet not found'})
    db.session.delete(pet)
    db.session.commit()
    return jsonify({'message': 'Pet deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)