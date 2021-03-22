import pandas as pd
from iribaker import to_iri
from rdflib import URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD, Graph, BNode

resource = 'http://github.com/kawai924/SementicNYWeatherAccident/resource/'
station = 'http://github.com/kawai924/SementicNYWeatherAccident/station#'
weatherVocab = 'http://github.com/kawai924/SementicNYWeatherAccident/weather#'
ontology = "./ontology/"

RESOURCES = Namespace(resource)

graph = []

def __load__(file_path):
    data = pd.read_csv(file_path, sep=",", quotechar='"', low_memory=False)
    return data

def __setup_namespace__():
    RESOURCES = Namespace(resource)
    WEA = Namespace(weatherVocab)
    return RESOURCES, WEA


def __setup_graph__(res):
    graph = Graph()
    graph.bind('data', res)
    graph.bind('wea', weatherVocab)
    return graph


def __save__(graph, file_path):
    f = open(file_path, "wb")
    f.write(graph.serialize(format='xml'))
    f.close()


def convert_to_rdf(input_file, output_file):

    rows = 0
    data = __load__(input_file)
    RES, WEA = __setup_namespace__()
    graph = __setup_graph__(RES)
    graph.parse(ontology + 'weather_type.ttl', format='turtle')

    filter2020 = data

    for index, data in filter2020.iterrows():
        
        
        station_id =  URIRef(to_iri(station + str(data['STATION_ID'])))
        date = URIRef(to_iri(resource + str(data['DATE'])))
        STATION_ID = Literal(data['STATION_ID'], datatype=XSD['string'])
        DATE = Literal(str(data['DATE']), datatype=XSD['unsignedlong'])

        instance = URIRef(to_iri(weatherVocab + ''.join(STATION_ID) + '/' + ''.join(str(data['DATE']))))

        graph.add((instance, RDF.type, instance))
        graph.add((instance, RDFS.label, STATION_ID))  
        graph.add((instance, RDFS.label, DATE)) 

        graph.add((instance, WEA['hasWeatherID'], Literal(data['WEATHER_ID'], datatype=XSD['string'])))
        graph.add((instance, WEA['hasWeatherType'], Literal(data['WEATHER_TYPE'], datatype=XSD['string'])))
        graph.add((instance, WEA['onDate'], Literal(data['DATE'], datatype=XSD['unsignedlong'])))
        #
        # if index % 10000 == 0:
        #    print("done with " + str(rows) + "0,000 rows")
        #    rows += 1
 
    __save__(graph, output_file)
#
# input_file = '../data/csv/NY_weather_type_pivot.csv'
# output_file = '../data/rdf/NY_weather_type.rdf'
# convert_to_rdf(input_file,output_file)