#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(jsonify(body), 200)

# Task #3: View to get an earthquake by id
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    # You can use either Earthquake.query.get(id) or db.session.get(Earthquake, id)
    quake = db.session.get(Earthquake, id)
    if quake:
        return quake.to_dict(), 200
    else:
        return {"message": f"Earthquake {id} not found."}, 404

# Task #4: View to get earthquakes by minimum magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    response = {
        "count": len(quakes),
        "quakes": [q.to_dict() for q in quakes]
    }
    return response, 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
