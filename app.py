from flask import Flask, jsonify
import datetime as dt
import pandas as pd
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import sqlalchemy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
style.use('fivethirtyeight')


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

app = Flask(__name__)
@app.route("/")
def Home():
    """List all available api routes."""
    return (
        "<h2>List of Paths</h2><ul><li>/api/v1.0/precipitation</li><li>/api/v1.0/stations</li><li>/api/v1.0/tobs</li><li>/api/v1.0/&lt;start&gt;</li><li>/api/v1.0/&lt;start&gt;/&lt;end&gt;</li></ul>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    shown_dict = {}
    for date, time in results:
        shown_dict[date] = time

    return jsonify(shown_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    results = session.query(Measurement.station).group_by(
        Measurement.station).all()

    session.close()
    station_ls = []
    for station in results:
        station_ls.append(station[0])
    return jsonify(station_ls)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    latest = session.query(Measurement.date).order_by(
        Measurement.date.desc()).first()
    latest = latest[0]
    latest = dt.datetime.strptime(latest, '%Y-%m-%d').date()
    """Return a list of all passenger names"""
    results = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.date >= latest-dt.timedelta(days=365)).all()

    session.close()
    tobs_ls = []
    for tobs in results:
        tobs_ls.append(tobs[1])
    return jsonify(tobs_ls)


@app.route("/api/v1.0/<start>", defaults={'end': None})
@app.route("/api/v1.0/<start>/<end>")
def dates_start(start, end):
    # Create our session (link) from Python to the DB
    if end == None:
        session = Session(engine)
        start = dt.datetime.strptime(start, "%Y-%m-%d").date()
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(
            Measurement.tobs)).filter(Measurement.date >= start).all()

        session.close()
    else:
        session = Session(engine)
        start = dt.datetime.strptime(start, "%Y-%m-%d").date()
        end = dt.datetime.strptime(end, "%Y-%m-%d").date()
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(
            Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

        session.close()
    return jsonify(results)


# @app.route("/api/v1.0/<start>/<end>")
# def dates_start_end(start, end):
#     # Create our session (link) from Python to the DB
#     session = Session(engine)
#     start = dt.datetime.strptime(start, "%Y-%m-%d").date()
#     end = dt.datetime.strptime(end, "%Y-%m-%d").date()
#     results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(
#         Measurement.tobs)).filter(Measurement.date >= start-dt.timedelta(days=365)).filter(Measurement.date <= end).all()

#     session.close()
#     return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
