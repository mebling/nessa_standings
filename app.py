import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_cors import CORS
from flask import jsonify
import datetime
from flask_migrate import Migrate
from models import db, School
from ratings import chart_data, rating_for, matchups_for
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
    return render_template("index.html", schools=schools)


@app.route("/matchups/<school_id>", methods=["GET"])
def matchups(school_id):
    return render_template("matchups.html", matchups=matchups_for(int(school_id)))


@app.route("/schools/<school_id>", methods=["GET"])
def schools(school_id):
    data = chart_data(int(school_id))
    school_name = db.session.query(School).filter_by(id=school_id).first().name
    return render_template("chart.html", highchart_json=data, school_name=school_name)
