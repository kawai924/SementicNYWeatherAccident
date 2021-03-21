import pandas as pd
from iribaker import to_iri
from rdflib import URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD, Graph, BNode

resource = 'http://github.com/kawai924/SementicNYWeatherAccident/resource/'
vocabulary = 'http://github.com/kawai924/SementicNYWeatherAccident/vocabulary/'
geocoord = 'http://www.w3.org/2003/01/geo/wgs84_pos#'
stationVocab = 'http://github.com/kawai924/SementicNYWeatherAccident/station#'
voc_location = "./ontology/"

RESOURCES = Namespace(resource)
VOCABULARY = Namespace(vocabulary)
GEO = Namespace(geocoord)
graph = []

def __load__(file_path):
    data = pd.read_csv(file_path, sep=",", quotechar='"', low_memory=False)
    return data


def __setup_namespace__():
    RESOURCES = Namespace(resource)
    VOCABULARY = Namespace(vocabulary)
    GEO = Namespace(geocoord)
    STA = Namespace(stationVocab)
    return RESOURCES, VOCABULARY, GEO, STA


def __setup_graph__(res, vocab):
    graph = Graph()
    graph.bind('data', res)
    graph.bind('vocab', vocab)
    graph.bind('geo', geocoord)
    graph.bind('STA', stationVocab)
    return graph


def __save__(graph, file_path):
    f = open(file_path, "wb")
    f.write(graph.serialize(format='xml'))
    f.close()


def convert_to_rdf(input_file, output_file):
    rows = 0

    data = __load__(input_file)
    RES, VOCAB, GEO, STA = __setup_namespace__()
    graph = __setup_graph__(RES, VOCAB)
    graph.parse(voc_location + 'NY_station_2.ttl', format='turtle')

    filter2020 = data

    # print(filter2020)

    for index, data in filter2020.iterrows():

        # station ID is primary key
        station = URIRef(to_iri(stationVocab + str(data['GHCND'])))
        station_id = Literal(data['GHCND'], datatype=XSD['string'])
        graph.add((station, STA['station_id'], station_id))
        # graph.add((station, RDF.lable, station))


        # print(graph)

        lat = Literal(data['LAT_DEC'] if pd.isnull(data['LAT_DEC']) == False else 0, datatype=XSD['double'])
        lon = Literal(data['LON_DEC'] if pd.isnull(data['LON_DEC']) == False else 0, datatype=XSD['double'])
        graph.add((station, GEO['lat'], lat))
        graph.add((station, GEO['long'], lon))

        name = Literal(data['STATION_NAME'], datatype=XSD['string'])
        graph.add((station, RDFS.label, name))

        # countrytag = URIRef(to_iri(stationVocab + '/' + str(data['CC'])))
        country = Literal(data['CC'], datatype=XSD['string'])
        # graph.add((countrytag, RDF.type, countrytag))
        graph.add((station, STA['country'], country))

        # statetag = URIRef(to_iri(stationVocab + '/' +  str(data['ST'])))
        state = Literal(data['ST'], datatype=XSD['string'])
        graph.add((station, STA['state'], state))
        # graph.add((statetag, RDF.type, statetag))

        # countytag = URIRef(to_iri(stationVocab + '/' +  str(data['COUNTY'])))
        county = Literal(data['COUNTY'], datatype=XSD['string'])
        graph.add((station, STA['county'], county))
        # graph.add((countytag, RDF.type, countytag))

    __save__(graph, output_file)