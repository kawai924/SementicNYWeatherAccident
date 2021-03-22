import NY_weather_data_extraction as weatherStation
import converter.accident_converter as accident

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Parsing weather station data...')
    weatherStation.NYdata()
    print('Done with parsing weather station data!\n')
    print('Converting accident csv into rdf...')
    accident.convert_to_rdf('data/csv/accident-NY-2020.csv', 'data/rdf/accident.rdf')
    print('Done with accident data!\n')
