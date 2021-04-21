import converter.accident_converter as accident
import converter.weather_converter as weather
import converter.weather_type_converter as weather_type
import converter.station_converter as station
import query.accident_queries as accident_thunder_query
import query.monthly_summary_ as monthly_summary_query
import query.simple_station_ as simple_station_query
import query.accident_queries as accident_query
# import query.borough_accident as borough_accident_query
# from query import accident_queries_optimize


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
    print('Executing query #1...')
    accident_thunder_query.start() # complex query
    print('Done with query #1!\n\n')

    print('Executing query #2...')
    monthly_summary_query.start() # complex query
    print('Done with query #2!\n\n')

    print('Executing query #3...')
    simple_station_query.start() # simple query
    print('Done with query #3!\n')
    print('Querying accident data...')
    accident_query.start()
    # print('Querying optimized accident data...')
    # accident_queries_optimize.start()
    # print('Querying borough data with View Obstruction...')
    # borough_accident_query.start()
    print('Done with querying accident data!\n')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # comment out specific line if only project 2 or 3 should run
    # create_rdf() # Project 2
    execute_queries() # Project 3
