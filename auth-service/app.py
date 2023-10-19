from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

users = []


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if the username is already taken
    if any(user['username'] == username for user in users):
        return jsonify({'message': 'Username already exists'})

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user
    user = {'username': username, 'password': hashed_password}
    users.append(user)

    return jsonify({'message': 'User created successfully'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Find the user by username
    user = next((user for user in users if user['username'] == username), None)
    if not user:
        return jsonify({'message': 'Invalid username'})

    # Check the password
    if not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid password'})

    # Generate a JWT token
    access_token = create_access_token(identity=username)

    return jsonify({'access_token': access_token})


if __name__ == '__main__':
    app.run()
