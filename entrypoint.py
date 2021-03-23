# import NY_weather_data_extraction as weatherStation
import converter.accident_converter as accident
import converter.weather_converter as weather
import converter.weather_type_converter as weather_type
import converter.station_converter as station

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
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