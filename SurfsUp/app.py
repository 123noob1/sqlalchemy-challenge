# Import the dependencies.
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///../Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Starting route and list all available routes
@app.route('/')
def home():
    print('Server received request for "Home" page...')
    return '''
        <head>
            <title>Homepage</title>
            <style>
                .code-mark {
                    background-color: #DCDCDC;
                    border-radius: 5px;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to the Simple API Hawaiin Weather Stations</h1><hr/>
            <h3>Available Routes</h3>
            <h5>You can manually copy and paste into the URL box or by clicking the link or the button.</h5>
            <ul>
                <li><mark class='code-mark'>/api/v1.0/precipitation</mark> for the precipitation analysis (<a href='../api/v1.0/precipitation'>CLICK HERE</a>)</li>
                <li><mark class='code-mark'>/api/v1.0/stations</mark> for a list of stations (<a href='../api/v1.0/stations'>CLICK HERE</a>)</li>
                <li><mark class='code-mark'>/api/v1.0/tobs</mark> for a list of temperatures from the most-active station in the last 12 years (<a href='../api/v1.0/tobs'>CLICK HERE</a>)</li>
                <li>
                    <mark class='code-mark'>/api/v1.0/&lt;start&gt;</mark> or <mark class='code-mark'>/api/v1.0/&lt;start&gt;/&lt;end&gt;</mark> 
                    to get the temperature stats from a given date range by replacing <mark class='code-mark'>&lt;start/end&gt;</mark> with the date<br/><br/>                  
                    <b>Use the following input boxes to query by dates</b><br/>
                    <b>Note:</b> The format date is <mark class='code-mark'>yyyy-mm-dd</mark><br/>
                    <form>
                        <label>Start Date</label>&ensp;<input type='text' id='start'><br/>
                        <label>End Date</label>&ensp;&nbsp;<input type='text' id='end'><br/>
                        <input type='button' value='Submit' onclick="goto(document.getElementById('start'), document.getElementById('end'))">
                    </form>
                </li>
            </ul>

            <script>
                function goto(start, end) {
                    if ((start && start.value) && (end && end.value)) {
                        window.location.href='../api/v1.0/' + start.value + '/' + end.value;
                    } else if ((start && start.value) && !(end && end.value)) {
                        window.location.href='../api/v1.0/' + start.value;
                    } else {
                        window.location.href='../api/v1.0/error';
                    }
                }
            </script>
        </body>
        '''

#  Create a route for precipitation that:
#    - Returns JSON with the date as the key and the value as precipitation
#    - Only returns the jsonified precipitation data for the last year in the database
@app.route('/api/v1.0/precipitation')
def get_precipitation():
    # Get the most recent date in the database
    recent_date = session.query(func.max(measurement.date)).first()

    # Calculate the starting date for the last year
    start_date = (dt.datetime.strptime(recent_date[0], '%Y-%m-%d') - dt.timedelta(days = 365)).date()
    
    # Query to retrieve dates and precipitation
    query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= start_date).all()

    # Close session
    session.close()

    # Assign the query into a dictionary with dates being the keys and prcps being the values
    precipitation_ = [dict(query)]

    return jsonify(precipitation_)

#  Create a route for stations that:
#    - Returns jsonified data of all the stations in the databases
@app.route('/api/v1.0/stations')
def get_stations():
    # Query to retrieve all the stations then return as a dictionary in jsonify format
    stations_ = session.query(station).all()

    # Close session
    session.close()

    # Set up empty dictionary
    all_stations = []

    # Using For loop to assign into a dictionary where station ID is the key and the rest will stored in a nested dictionary
    for station_ in stations_:
        # Set up the dictionary
        station_dict = {}
        station_dict[station_.station] = {
                                'name': station_.name,
                                'lat': station_.latitude,
                                'lng': station_.longitude,
                                'elevation': station_.elevation
                            }
        all_stations.append(station_dict)

    return jsonify(all_stations)

# Create a route for tobs to find:
#   -temperature observations of most-active station (USC00519281) for the previous year of data
@app.route('/api/v1.0/tobs')
def temperatures():
    # Get the most recent date in the database
    recent_date = session.query(func.max(measurement.date)).filter(measurement.station == 'USC00519281').first()

    # Calculate the starting date for the last year
    start_date = (dt.datetime.strptime(recent_date[0], '%Y-%m-%d') - dt.timedelta(days = 365)).date()

    # Query for all dates and tobs for the station from the past 12 months
    station_query = session.query(station.station, measurement.date, measurement.tobs).filter(measurement.station == station.station, \
                                                                                      measurement.date >= start_date, \
                                                                                      station.station == 'USC00519281'
                                                                                    ).all()
    
    # Close session
    session.close()

    station_result = []
    station_result.append({station_query[0][0] : {dt:val for _, dt, val in station_query}})

    return jsonify(station_result)

# Set up api path with start and end to return the JSON list of minimum, average,
# and the maximum temperature for a specified start or start-end range
@app.route('/api/v1.0/<start>')
def get_temp_start(start):
    # Validate the date entered before proceeding
    start_is_date = is_date_validate(start)

    if start_is_date:
        # Set query
        query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).all()
        
        # Close session
        session.close()

        # Check to see if the query yielded none in case the date entered does not exist in the table
        if not query[0][0] is None:
            result = []
            result.append({
                'min': query[0][0],
                'max': query[0][1],
                'avg': query[0][2]
                })            
            return jsonify(result)
        
        return jsonify({"error": f"Date entered {start} yielded no result."}), 404
    
    return jsonify({"error": f"Date entered {start} is not in proper format (yyyy-mm-dd) or is not a date"}), 404

@app.route('/api/v1.0/<start>/<end>')
def get_temp_start_end(start, end):
    # Validate the start and end dates before proceeding
    start_is_date = is_date_validate(start)
    end_is_date = is_date_validate(end)

    if start_is_date and end_is_date:

        if not start.replace('-','') > end.replace('-',''):
            # Set query
            query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)). \
                            filter(measurement.date >= start, measurement.date <= end).all()
            
            # Close session
            session.close()

            # Check to see if the query yielded none in case the date entered does not exist in the table
            if not query[0][0] is None:
                result = []
                result.append({
                    'min': query[0][0],
                    'max': query[0][1],
                    'avg': query[0][2]
                    })            
                return jsonify(result)
            
            return jsonify({"error": f"Start date '{start}' and End date '{end}' yielded no result."}), 404
        
        return jsonify({"error": f"Start date '{start}' cannot be greater than the end date '{end}'"}), 404
    
    return jsonify({"error": f"Date not in proper format (yyyy-mm-dd) or is not a date <Start date '{start}' = {start_is_date} | End date '{end}' = {end_is_date}>"}), 404

##############################################
# Set up function for reuse in validating date
##############################################
def is_date_validate(date):
    # Create validation variables
    check_pass = False

    # Do try to verify the input and return false regardless of exception
    try:    
        year, month, day = date.split('-')
        dt.datetime(int(year), int(month), int(day))
        check_pass = True
    except:
        return check_pass
    
    return check_pass

if __name__ == '__main__':
    app.run(debug = True)