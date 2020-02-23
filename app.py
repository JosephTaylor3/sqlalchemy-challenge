import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
 
    )


@app.route("/api/v1.0/precipitation")   #check if working#
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and precipitation values"""
    # Query all dates and prcp values 
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

     # Create a dictionary from the row data and append to a list
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)



@app.route("/api/v1.0/stations")   #check to see if works#
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")   #check to see if working#
def lastyearrain():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations from the latest year"""
    # Query
    tobs_last12 = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').all()

    session.close()

     # Create a dictionary from the row data and append to a list
    tobs = []
    for date, prcp in tobs_last12:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs.append(tobs_dict)

    return jsonify(tobs)



# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")   #UNFINISHED#
def calc_temps(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()

    session.close()

     # Convert list of tuples into normal list
    temperature_set = list(np.ravel(results))

    return jsonify(temperature_set)



@app.route("/api/v1.0/<start>/<end>")   #UNFINISHED#
def calc_temps(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

     # Convert list of tuples into normal list
    temperature_set = list(np.ravel(results))

    return jsonify(temperature_set)




if __name__ == '__main__':
    app.run(debug=True)
