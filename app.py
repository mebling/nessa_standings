import os
from flask import Flask
from flask_cors import CORS
from flask import jsonify
import datetime
from flask_migrate import Migrate
from models import db, School
from ratings import rating_for, matchups_for
import os


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/nessa"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
migrate = Migrate(app, db)
db.init_app(app)


@app.route('/', methods=['GET'])
def index():
    schools = db.session.query(School).order_by(School.name).all()
    schools = [{'name': school.name, 'id': school.id, 'rating': rating_for(school)} for school in schools]
    schools = sorted(schools, key=lambda k: k['rating'], reverse=True)
    return jsonify({'schools': schools})


@app.route("/schools/<school_id>/matchups", methods=["GET"])
def matchups(school_id):
    return jsonify({'matchups': matchups_for(int(school_id))})
