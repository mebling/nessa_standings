import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_cors import CORS
from flask import jsonify
import datetime
from flask_migrate import Migrate
from models import db
from ratings import chart_data
import os


# DATABASE_URL = "postgresql://localhost/nessa"

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
migrate = Migrate(app, db)
db.init_app(app)


@app.route('/', methods=['GET'])
def index():
    data, tooltip_data = chart_data()
    return render_template("chart.html", highchart_json=data, tooltip_json=tooltip_data)


@app.route("/schools/<school_id>", methods=["GET"])
def schools(school_id):
    school = School.filter_by(id=school_id).first()
    data, tooltip_data = chart_data()
    data = [d for d in data if d['name'] == school.name]
    return render_template("chart.html", highchart_json=data, tooltip_json=tooltip_data)
