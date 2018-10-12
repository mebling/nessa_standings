import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_cors import CORS
from flask import jsonify
import datetime
from flask_migrate import Migrate
from models import db
#from ratings import chart_data


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/nessa"
db.init_app(app)
migrate = Migrate(app, db)



@app.route('/', methods=['GET'])
def index():
    data, tooltip_data = chart_data()
    return render_template("chart.html", highchart_json=data, tooltip_json=tooltip_data)


@app.route("/schools/<school_id>", methods=["GET"])
def schools(school_id):
    school = School.get(id=school_id)
    data, tooltip_data = chart_data()
    data = [d for d in data if d['name'] == school.name]
    return render_template("chart.html", highchart_json=data, tooltip_json=tooltip_data)
