# from converter.weather_columns import Weather
import pandas as pd
from iribaker import to_iri
from rdflib import URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD, Graph, BNode

resource = 'http://github.com/kawai924/SementicNYWeatherAccident/weather/'
station = 'http://github.com/kawai924/SementicNYWeatherAccident/station#'

weatherVocab = 'http://github.com/kawai924/SementicNYWeather/stationID#'

voc_location = "./ontology/"

RESOURCES = Namespace(resource)
graph = []


def __load__(file_path):
    data = pd.read_csv(file_path, sep=",", quotechar='"', low_memory=False)
    return data


def __setup_namespace__():
    RESOURCES = Namespace(resource)
    WEAN = Namespace(weatherVocab)
    STA = Namespace(station)
    return RESOURCES, WEAN, STA


def __setup_graph__(res):
    graph = Graph()
    graph.bind('data', res)
    graph.bind('wean', weatherVocab)
    return graph


def __save__(graph, file_path):
    f = open(file_path, "wb")
    f.write(graph.serialize(format='xml'))
    f.close()


def convert_to_rdf(input_file, output_file):
    rows = 0

    data = __load__(input_file)
    RES, WEA, STA = __setup_namespace__()
    graph = __setup_graph__(RES)
    graph.parse(voc_location + 'weather.ttl', format='turtle')

    filter2020 = data

    for index, weather_data in filter2020.iterrows():

        # Collision_id is primary key
        stationId = URIRef(to_iri(station + str(weather_data['station_id'])))

        Date = URIRef(to_iri(resource + str(weather_data['date'])))

        # graph.add((stationId,WEA['isOn'],Date))
        # data property
        station_id = Literal(weather_data['station_id'], datatype=XSD['string'])
        date = Literal(str(weather_data['date']), datatype=XSD['date'])

        # borough_data = str(accident_data['BOROUGH']).capitalize()
        instance = URIRef(to_iri(weatherVocab + ''.join(station_id) + '/' + ''.join(str(weather_data['date']))))
        graph.add((instance, RDF.type, instance))
        # graph.add((instance, STA['station_id'], stationId))
        graph.add((instance, WEA['stationID'], stationId))
        graph.add((instance, RDFS.label, station_id))
        graph.add((instance, RDFS.label, date))
        # graph.add((Weather, WEA['isinstance'], instance))

        if (pd.isnull(weather_data['AWND']) == False):
            graph.add((instance, WEA['hasAWND'], Literal(weather_data['AWND'], datatype=XSD['int'])))

        if (pd.isnull(weather_data['TMAX']) == False):
            graph.add((instance, WEA['hasTMAX'], Literal(weather_data['TMAX'], datatype=XSD['int'])))

        if (pd.isnull(weather_data['TMIN']) == False):
            graph.add((instance, WEA['hasTMIN'], Literal(weather_data['TMIN'], datatype=XSD['int'])))

        if (pd.isnull(weather_data['TAVG']) == False):
            graph.add((instance, WEA['hasTAVG'], Literal(weather_data['TAVG'], datatype=XSD['int'])))

        if (pd.isnull(weather_data['WESF']) == False):
            graph.add((instance, WEA['hasWESF'], Literal(weather_data['WESF'], datatype=XSD['int'])))

        # just for debugging purposes
        if ((index % 10000) == 0):
            print("done with " + str(rows) + "0,000 rows")
            rows += 1

    __save__(graph, output_file)