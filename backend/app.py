# backend/app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os # <-- Make sure this is imported

# Create a Flask application instance
app = Flask(__name__)
CORS(app)

# --- Database Configuration ---
# Get the absolute path of the directory the script is in
basedir = os.path.abspath(os.path.dirname(__file__))
# Set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db = SQLAlchemy(app) # <-- Is this line present and correct?

# --- Database Model ---
class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'frequency': self.frequency,
            'category': self.category
        }

# --- API Routes ---

# A route to get all habits from the database
@app.route("/api/habits", methods=['GET'])
def get_habits():
    habits = Habit.query.all()
    return jsonify([habit.to_json() for habit in habits])

# A route to create a new habit
@app.route("/api/habits", methods=['POST'])
def create_habit():
    data = request.get_json()
    new_habit = Habit(
        name=data['name'],
        frequency=data['frequency'],
        category=data['category']
    )
    db.session.add(new_habit)
    db.session.commit()
    return jsonify(new_habit.to_json()), 201

# A simple route to test the server
@app.route("/")
def hello_world():
    return "Hello, this is the Habit Hero backend!"


# A route to delete a specific habit by its ID
@app.route("/api/habits/<int:habit_id>", methods=['DELETE'])
def delete_habit(habit_id):
    # Find the habit in the database by its ID
    habit = Habit.query.get(habit_id)

    # If the habit doesn't exist, return a 404 Not Found error
    if habit is None:
        return jsonify({'error': 'Habit not found'}), 404

    # Remove the habit from the database session
    db.session.delete(habit)
    # Commit the session to save the changes
    db.session.commit()

    # Return a success message
    return jsonify({'message': 'Habit deleted successfully'}), 200

# This line allows you to run the app directly from the command line
if __name__ == "__main__":
    app.run(debug=True)