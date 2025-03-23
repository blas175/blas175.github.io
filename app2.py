import json

from flask import Flask, jsonify, request

app = Flask(__name__)


# Load data from JSON file
def load_data():
    with open("data.json", "r") as file:
        return json.load(file)


# Save data to JSON file
def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


# Get all users
@app.route("/api/users", methods=["GET"])
def get_users():
    data = load_data()
    names = [user["name"] for user in data]
    return jsonify(names)


# Add or replace a user by ID
@app.route("/api/users", methods=["POST"])
def add_or_replace_user():
    users = load_data()
    new_user = request.json

    # Check if the user with the given ID already exists
    existing_user = next((u for u in users if u["id"] == new_user["id"]), None)

    if existing_user:
        # Replace existing user data with new user data
        existing_user["name"] = new_user["name"]
        message = "User updated!"
    else:
        # Add new user to the list
        users.append(new_user)
        message = "User added!"

    # Save data to file
    save_data(users)
    return jsonify({"message": message, "user": new_user}), 200


if __name__ == "__main__":
    app.run(debug=True)
