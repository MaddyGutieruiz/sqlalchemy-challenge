import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from Flask import Flask, jsonify


## Setting up Database

engine = create_engine('sqlite:///hawaii.sqlite', connect_args={'check_same_thread': False})

# pulling database from existing one
database = automap_base()

database.prepare(engine, reflect=True)

# Save references to the tables
measurement = database.classes.measurement
station = database.classes.station


# Create session from Python
session = Session(engine)


## Flask and landing page for app
app = Flask(__name__)

# last 12 months variable
twelve_months = '2016-08-23'

#Start at the homepage. List all the available routes.
@app.route("/")
def welcome():
    return (
        f"<p>Welcome to the Hawaii weather API!</p>"
        f"<p>Usage:</p>"
        f"/api/v1.0/precipitation<br/>Returns a JSON list of percipitation data for the dates between 8/23/16 and 8/23/17<br/><br/>"
        f"/api/v1.0/stations<br/>Returns a JSON list of the weather stations<br/><br/>"
        f"/api/v1.0/tobs<br/>Returns a JSON list of the Temperature Observations (tobs) for each station for the dates between 8/23/16 and 8/23/17<br/><br/>"
        f"/api/v1.0/date<br/>Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for the dates between the given start date and 8/23/17<br/><br/>."
        f"/api/v1.0/start_date/end_date<br/>Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for the dates between the given start date and end date<br/><br/>."
    )

# Precipitation
#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Date 12 months ago
    precip_year = session.query(measurement.date, func.avg(measurement.prcp)).filter(measurement.date >= twelve_months).group_by(measurement.date).all()
    return jsonify(precip_year)


# Stations
#Return the JSON representation of your dictionary
@app.route("/api/v1.0/stations")
def stations():
    active_station_query = session.query(station.station, station.name).all()
    return jsonify(active_station_query)


# tobs
# Return a JSON list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    temp_query = session.query(measurement.date, measurement.station, measurement.tobs).filter(measurement.date >= twelve_months).all()
    return jsonify(temp_query)


# Start and End
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    day_temp_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= date).all()
    return jsonify(day_temp_results)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    multi_day_temp_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    return jsonify(multi_day_temp_results)

if __name__ == "__main__":
    app.run(debug=True)
