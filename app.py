from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#Hellot statu
# Setup SQLite database URI
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///users.db"  # SQLite file in the current directory
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # To disable modification tracking

# Initialize the database
db = SQLAlchemy(app)


# Define the User model (table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


# Create the database and table (run only once to initialize the database)
with app.app_context():
    db.create_all()


# Route to get all users
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()  # Query all users from the database
    return jsonify([{"id": u.id, "name": u.name} for u in users])


# Route to add or replace a user
@app.route("/api/users", methods=["POST"])
def add_or_replace_user():
    data = request.json
    existing_user = User.query.filter_by(id=data["id"]).first()

    if existing_user:
        # Update the user
        existing_user.name = data["name"]
        db.session.commit()
        message = "User updated!"
    else:
        # Add new user
        new_user = User(id=data["id"], name=data["name"])
        db.session.add(new_user)
        db.session.commit()
        message = "User added!"

    return (
        jsonify({"message": message, "user": {"id": data["id"], "name": data["name"]}}),
        200,
    )


# Route to delete a user by ID
@app.route("/api/users", methods=["DELETE"])
def delete_user():
    data = request.json
    user_id = data.get("id")

    if not user_id:
        return jsonify({"message": "User ID is required!"}), 400

    user_to_delete = User.query.filter_by(id=user_id).first()

    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return (
            jsonify({"message": f"User with ID {user_id} deleted successfully!"}),
            200,
        )
    else:
        return jsonify({"message": f"User with ID {user_id} not found!"}), 404


if __name__ == "__main__":
    app.run(debug=True)
