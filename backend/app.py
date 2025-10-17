from flask import Flask, jsonify
from flask_cors import CORS

# Create a Flask application instance
app = Flask(__name__)
CORS(app) # This will enable Cross-Origin Resource Sharing

# A simple route to test the server
@app.route("/")
def hello_world():
    return "Hello, this is the Habit Hero backend!"

# A route to get some sample habits
@app.route("/api/habits", methods=['GET'])
def get_habits():
    sample_habits = [
        {"id": 1, "name": "Drink Water", "frequency": "daily", "category": "Health"},
        {"id": 2, "name": "Read a Book", "frequency": "daily", "category": "Learning"}
    ]
    return jsonify(sample_habits)

# This line allows you to run the app directly from the command line
if __name__ == "__main__":
    app.run(debug=True)