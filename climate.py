# Import Essential Libraries
from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc, asc


# Base & Engine Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


# Store Session Queries
lastyearsrain = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= dt.date(2017,8,23), Measurement.date >= dt.date(2017,8,23)-dt.timedelta(days=365)).all()
station_count = session.query(Station.station).all()
tobs_plot = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date <= "2017-08-18", Measurement.date >= "2016-08-18").all()

# Begin Flask Climate App

from flask import Flask, jsonify
app = Flask(__name__)


#Define routes

@app.route('/')
def home():
    return (f"Welcome to Gerard's Climate Site.<br/>"
            f"Here are your available routes:<br/>"
            f"<br/>"
            f'/api/v1.0/precipitation<br/>'
            f'--returns a list of precipitation values in the last 12 month period<br/>'
            f"<br/>"
            f'/api/v1.0/stations<br/>'
            f'-- returns a list of all stations collecting climate data<br/>'
            f"<br/>"
            f'/api/v1.0/tobs<br/>'
            f'-- returns a list of temperature observations in the last 12 months<br/>'
            f"<br/>"
            f'/api/v1.0/start<br/>'
            f'-- returns min, max, and average temps from the given date to end of dataset<br/>'
            f"<br/>"
            f'/api/v1.0/start/end<br/>'
            f'-- returns min, max, and average temps between start and end date. enter date as %Y-%m-%d<br/>')
            
@app.route('/api/v1.0/precipitation')
def rain():
    return dict(lastyearsrain)

@app.route('/api/v1.0/stations')
def stations():
    return dict(enumerate(station_count))

@app.route('/api/v1.0/tobs')
def tobs():
    return dict(tobs_plot)

@app.route('/api/v1.0/<start>')
def calc_tempsa(start):
  
    begin = str(start)
    broken= [b for b in begin]
    broken.insert(4,'-')
    broken.insert(7,'-')
    glue = ""
    start_date = glue.join(broken)
    
    temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    test = zip(['Min', 'Avg', "Max"], *temp)
    
    return dict([i for i in test])

if __name__ == "__main__":
    app.run(debug=True)
