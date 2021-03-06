import converter.accident_converter as accident
import converter.weather_converter as weather
import converter.weather_type_converter as weather_type
import converter.station_converter as station
import query.accident_queries as accident_thunder_query
import query.monthly_summary_ as monthly_summary_query
import query.simple_station_ as simple_station_query
import query.borough_accident as borough_accident_query
import query.vehicle_type as vehicle_type_query
import query.input_query as input_query
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import webbrowser


def create_rdf():
    print('Parsing weather station data...')
    # not going to include the data file as those are too big
    # weatherStation.NYdata()
    station.convert_to_rdf('data/csv/NY_station.csv', 'data/rdf/NYstation.rdf')
    print('Done with parsing weather station data!\n')

    print('Converting accident csv into rdf...')
    accident.convert_to_rdf('data/csv/accident-NY-2020.csv', 'data/rdf/NY_accident.rdf')
    print('Done with accident data!\n')

    print('Converting weather number csv into rdf...')
    weather.convert_to_rdf('data/csv/NY_weather_number_pivot.csv', 'data/rdf/NY_weather_number.rdf')
    print('Done with weather number data!\n')

    print('Converting weather type csv into rdf...')
    weather_type.convert_to_rdf('data/csv/NY_weather_type_pivot.csv', 'data/rdf/NY_weather_type.rdf')
    print('Done with weather type data!\n')


def execute_queries():
    print('This will run example simple and complex queries automatically')

    print('Executing query #1...')
    accident_thunder_query.start()  # complex query
    print('Done with query #1!\n\n')
    
    print('Executing query #2...')
    monthly_summary_query.start()  # complex query
    print('Done with query #2!\n\n')
    
    print('Executing query #3...')
    simple_station_query.start()  # simple query
    print('Done with query #3!\n\n')
    
    print('Executing query #4...')
    borough_accident_query.start()  # complex query
    print('Done with query #4!\n\n')
    
    print('Executing query #5...')
    vehicle_type_query.start()  # complex query
    print('Done with query #5!\n\n')

    print('Done with executing all the queries! You can find the output files under ./query/output/*.html \n')


def execute_manual_query():
    print('This will allow you to input your own query in the terminal and execute it')
    input_query.start()
    print('Done with executing input query. You can find the output files under ./query/output/input_results.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # comment out specific line if only project 2 or 3 should run
    # create_rdf()  # Project 2
    execute_queries()  # Project 3 for all automated queries
    # execute_manual_query()  # Project 3 for executing manual queries aka search engine

    ########################################################
    # web server part
    ########################################################
    # cd to the output folder
    os.chdir('./query/output')

    # call browser
    webbrowser.open('localhost:8888')

    # start web server, until process terminated
    httpd = HTTPServer(('localhost', 8888), SimpleHTTPRequestHandler)
    httpd.serve_forever()
