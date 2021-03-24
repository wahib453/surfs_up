#%%
# import datetime, numpy, and pandas dependencies
import datetime as dt
import numpy as np
import pandas as pd

#%%
# import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#%%
# import flask depency
from flask import Flask, jsonify

#%%
# set up the database
engine = create_engine("sqlite:///hawaii.sqlite")

#%%
# reflect database into classes
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#%%
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#%%
# Create our session (link) from Python to the DB
session = Session(engine)

#%%
# create a new flask app instance
app = Flask(__name__)

#%%
#create flask routes
@app.route('/')
def welcome():
    return(
        '''
        welcome to the climate analysis API!
        Available Routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/v1.0/temp/start/end
        '''
    )
#%%
# create precipation route
@app.route("/api/v1.0/precipitation")    
def precipitation():
    # Get the date and precipitation for the previous year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year ).all()
    # create a dictionary with date as the key and precipitaion as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
#%%
# create stations route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
#%%
# create temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
#%%
# create a summary report of statistics
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
    