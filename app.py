# Import dependencies needed for the analysis

# Analytics dependencies
import datetime as dt
import numpy as np
import pandas as pd

# SQLite dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask dependencies
from flask import Flask, jsonify

# Magical values
version_num = "v1.0"

# Set up the Database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Rename tables/classes
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link
session =Session(engine)

# Set up Flask
app = Flask(__name__)

# Welcome Route
@app.route("/")

def welcome():
    return(
    f'''
    Welcome to the Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/{version_num}/precipitation<br/>
    /api/{version_num}/stations<br/>
    /api/{version_num}/tobs<br/>
    /api/{version_num}/temp/start/end<br/>
    ''')

@app.route(f"/api/{version_num}/precipitation")

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route(f"/api/{version_num}/stations")

def stations():
  results = session.query(Station.station).all()
  stations = list(np.ravel(results))
  return jsonify(stations=stations)

@app.route(f"/api/{version_num}/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route(f"/api/{version_num}/temp/<start>")
@app.route(f"/api/{version_num}/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# Added after lecture, not in module
if __name__ == "__main__":
    app.run(debug=True)