# Import Essential Libraries
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
            f'/api/v1.0/start/<font color="red">yyyymmdd</font><br/>'
            f'-- returns min, max, and average temps from the given date to end of dataset.<br/>'
            f"<br/>"
            f'/api/v1.0/startend/<font color="red">yyyymmdd</font>/<font color="blue">yyyymmdd</font><br/>'
            f'-- returns min, max, and average temps between start and end date.<br/>')
            
@app.route('/api/v1.0/precipitation')
def rain():
    lastyearsrain = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= dt.date(2017,8,23), Measurement.date >= dt.date(2017,8,23)-dt.timedelta(days=365)).all()
    session.close()
    return dict(lastyearsrain)

@app.route('/api/v1.0/stations')
def stations():
    station_count = session.query(Station.station).all()
    session.close()
    return dict(enumerate(station_count))

@app.route('/api/v1.0/tobs')
def tobs():
    temp_obs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date <= "2017-08-18", Measurement.date >= "2016-08-18").all()
    session.close()
    return dict(temp_obs)

@app.route('/api/v1.0/start/<start_date>')
def onedate(start_date):

    #yyyymmdd to 'yyyy-mm-dd'
    begin = str(start_date)
    broken= [b for b in begin]
    broken.insert(4,'-')
    broken.insert(7,'-')
    glue = ""
    start_date = glue.join(broken)

    temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    test = zip(['Min', 'Avg', "Max"], *temp)
    return dict([i for i in test])

@app.route('/api/v1.0/startend/<s_date>/<e_date>')
def twodates(s_date, e_date):

    #yyyymmdd to 'yyyy-mm-dd'
    twobegin = [str(s_date), str(e_date)]
    twobroken= [b for b in twobegin]
    s = [x for x in twobroken[0]]
    s.insert(4,'-')
    s.insert(7,'-')
    e = [y for y in twobroken[1]]
    e.insert(4,'-')
    e.insert(7,'-')
    glue = ""
    ss_date = glue.join(s)
    ee_date = glue.join(e)
    
    twotemp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= ss_date, Measurement.date <= ee_date, ).all()
    session.close()

    twotest = zip(['Min', 'Avg', "Max"], *twotemp)
    return dict([j for j in twotest])

# Run App
if __name__ == "__main__":
    app.run(debug=True)