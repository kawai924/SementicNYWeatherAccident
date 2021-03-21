import pandas as pd
from iribaker import to_iri
from rdflib import URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD, Graph, BNode

resource = 'http://github.com/kawai924/SementicNYWeatherAccident/resource/'
vocabulary = 'http://github.com/kawai924/SementicNYWeatherAccident/vocabulary/'
weatherVocab = 'http://github.com/kawai924/SementicNYWeatherAccident/weather#'
voc_location = "./"

RESOURCES = Namespace(resource)
VOCABULARY = Namespace(vocabulary)
graph = []

def __load__(file_path):
    data = pd.read_csv(file_path, sep=",", quotechar='"', low_memory=False)
    return data

def __setup_namespace__():
    RESOURCES = Namespace(resource)
    VOCABULARY = Namespace(vocabulary)
    WEA = Namespace(weatherVocab)
    return RESOURCES, VOCABULARY, WEA


def __setup_graph__(res, vocab):
    graph = Graph()
    graph.bind('data', res)
    graph.bind('vocab', vocab)
    graph.bind('wea', weatherVocab)
    return graph


def __save__(graph, file_path):
    f = open(file_path, "wb")
    f.write(graph.serialize(format='xml'))
    f.close()


def convert_to_rdf(input_file, output_file):

    data = __load__(input_file)
    RES, VOCAB, WEA = __setup_namespace__()
    graph = __setup_graph__(RES, VOCAB)
    # graph.parse(voc_location + 'weather.ttl', format='turtle')

    filter2020 = data

    for index, data in data.iterrows():
        
        date = URIRef(to_iri(resource + str(data['DATE'])))
        DATE = Literal(data['DATE'], datatype=XSD['string'])
        graph.add((date, VOCAB['Date'], DATE))

        STATION_ID = Literal(data['STATION_ID'], datatype=XSD['string'])
        WEATHER_TYPE = Literal(data['WEATHER_TYPE'], datatype=XSD['string'])
        WEATHER_ID = Literal((data['WEATHER_ID']), datatype=XSD['string'])

        graph.add((date, VOCAB['weatherStation'], STATION_ID))  
        graph.add((date, VOCAB['hasWeatherType'], WEATHER_TYPE)) 
        graph.add((date, VOCAB['hasWeatherId'], WEATHER_ID)) 

    __save__(graph, output_file)


input_file = './NY_weather_type_2020.csv'
output_file = './NY_weather_type.rdf'
convert_to_rdf(input_file,output_file)