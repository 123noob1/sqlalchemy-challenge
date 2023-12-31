# sqlalchemy-challenge
For this challenge, use Python and SQLAlchemy to do basic climate analysis and data exploration into the <code>hawaii.sqlite</code> database. After that, create an API app using Flask to retrieve data based on the queries designed during data anlysis and exploration.

### Part 1: Analyze and Explore the Climate Data
<i>Refer to the Jupyter Notebook file <code>climate_start.ipynb</code> located under the SurfsUp folder for the completed work.</i>

To perform the data anlysis and exploration, the following steps were taken:
- <b>Precipitation Analysis</b>
    1) Find the most recent date in the dataset.
    2) Using the recent date, retrieve previous 12 months of precipitation data by querying the previous 12 months of data and display the <code>date</code> and <code>prcp</code> rows.
    3) Create a bar chart using Pandas and MatplotLib.
    4) Get the statistic of the precipitation data using Pandas.
- <b>Station Analysis</b>
    1) Determine the total number of stations in the dataset.
    2) Design a query to find most-active stations in descending order and determine which station ID has the greatest number of observations.
    3) Calculate the <code>min</code>, <code>max</code>, and <code>avg</code> temperatures on the most-active station ID.
    4) Design a 12 months of temperature observation <code>tobs</code> data and plot using histogram to show the data.

### Part 2: Design the Climate App
<i>Refer to the <code>app.py</code> file located under the SurfsUp folder  and run from there for this section.</i>

1) Design Flask API based on the queries used in previous part.
2) Design a homepage and list all available routes below to retrieve and return the following data in a <code>jsonify</code> format:
    - <code>/api/v1.0/precipitation</code> to return the precipitation <code>prcp</code> by <code>date</code>
    - <code>/api/v1.0/stations</code> to return list of stations from the dataset
    - <code>/api/v1.0/tobs</code> to return <code>date</code> and temperature <code>tobs</code> observations for most-active station from previous year data
    - <code>/api/v1.0/&lt;start&gt;</code> to return <code>min</code>, <code>max</code>, and <code>avg</code> temperatures from the given <code>start</code> date
    - <code>/api/v1.0/&lt;start&gt;/&lt;end&gt;</code> to return <code>min</code>, <code>max</code>, and <code>avg</code> temperatures between the given <code>start</code> and <code>end</code> dates
        - To verify the custom date input for the <code>start</code> and <code>end</code> dates, function <code>is_date_validate</code> was created and used to validate before running the query.
        ```
        def is_date_validate(date):
            # Create validation variables
            check_pass = False

            # Do try to verify the input
            try:    
                year, month, day = date.split('-')
                dt.datetime(int(year), int(month), int(day))
                check_pass = True
            except:
                return check_pass
            
            return check_pass
        ```

#### Using the API page
You can access different route by:
- clicking on the <code>CLICK HERE</code> for predesignated query routes.
- Entering the dates into input boxes for <code>start</code> and <code>end</code> dates then hit submit for custom date ranges where your input will be calculated.
- Or manually copy and paste the path into the URL address bar, remember to replace the <code>&lt;start&gt;</code> or <code>&lt;end&gt;</code> with a date value <code>yyyy-mm-dd</code>. For any other values, the program will return an error.

![Alt text](/Resources/api_app.png)

## References
- JavaScript was used in the home page to allow interactions and the sources to help writing the script came from the following pages:
    - https://stackoverflow.com/questions/8803412/check-if-an-html-input-element-is-empty-or-has-no-value-entered-by-user
    - https://www.w3schools.com/js/js_if_else.asp
    - https://stackoverflow.com/questions/41216153/javascript-error-object-htmlinputelementobject-htmlinputelement
