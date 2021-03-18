import pandas as pd
from iribaker import to_iri
from rdflib import URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD, Graph, BNode

resource = 'http://github.com/kawai924/SementicNYWeatherAccident/resource/'
vocabulary = 'http://github.com/kawai924/SementicNYWeatherAccident/vocabulary/'
geocoord = 'http://www.w3.org/2003/01/geo/wgs84_pos#'

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
    return RESOURCES, VOCABULARY, GEO


def __setup_graph__(res, vocab):
    graph = Graph()
    graph.bind('data', res)
    graph.bind('vocab', vocab)
    graph.bind('geo', geocoord)
    return graph


def __save__(graph, file_path):
    f = open(file_path, "wb")
    f.write(graph.serialize(format='pretty-xml'))
    f.close()


def convert_to_rdf(input_file, output_file):
    rows = 0

    data = __load__(input_file)
    RES, VOCAB, GEO = __setup_namespace__()
    graph = __setup_graph__(RES, VOCAB)
    filter2020 = data.loc[data['CRASH DATE'].str.split('/', expand=True)[2] == '2020']
                          # or data['CRASH DATE'].str.split('/', expand=True)[2] == '2019'
                          # or data['CRASH DATE'].str.split('/', expand=True)[2] == '2018']

    for index, accident_data in filter2020.iterrows():

        # Collision_id is primary key
        accident = URIRef(to_iri(resource + str(accident_data['COLLISION_ID'])))
        collision_id = Literal(accident_data['COLLISION_ID'], datatype=XSD['int'])

        # change this to already existing namespace?
        crash_date = Literal(accident_data['CRASH DATE'], datatype=XSD['string'])    # change this to xsd:date

        # create new resource called Address:
        borough = Literal(accident_data['BOROUGH'], datatype=XSD['string'])
        zip = Literal(accident_data['ZIP CODE'], datatype=XSD['int'])
        # include location

        geo = URIRef(to_iri(geocoord + str(accident_data['COLLISION_ID'])))
        lat = Literal(accident_data['LATITUDE'], datatype=XSD['double'])
        lon = Literal(accident_data['LONGITUDE'], datatype=XSD['double'])

        if (pd.isnull(accident_data['ON STREET NAME']) == False):
            street = Literal(accident_data['ON STREET NAME'].rstrip(), datatype=XSD['string'])
            graph.add((accident, VOCAB['street'], street))

        persons_injured = Literal(accident_data['NUMBER OF PERSONS INJURED'], datatype=XSD['int'])
        persons_killed = Literal(accident_data['NUMBER OF PERSONS KILLED'], datatype=XSD['int'])
        pedestrians_injured = Literal(accident_data['NUMBER OF PEDESTRIANS INJURED'], datatype=XSD['int'])
        pedestrians_killed = Literal(accident_data['NUMBER OF PEDESTRIANS KILLED'], datatype=XSD['int'])

        vehicle_type_1 = Literal(accident_data['VEHICLE TYPE CODE 1'], datatype=XSD['string'])
        if(pd.isnull(accident_data['VEHICLE TYPE CODE 2']) == False):
            vehicle_type_2 = Literal(accident_data['VEHICLE TYPE CODE 2'], datatype=XSD['string'])
            graph.add((accident, VOCAB['vehicle_type_2'], vehicle_type_2))

        if(pd.isnull(accident_data['VEHICLE TYPE CODE 3']) == False):
            vehicle_type_3 = Literal(accident_data['VEHICLE TYPE CODE 3'], datatype=XSD['string'])
            graph.add((accident, VOCAB['vehicle_type_3'], vehicle_type_3))

        contributing_factor_1 = Literal(accident_data['CONTRIBUTING FACTOR VEHICLE 1'], datatype=XSD['string'])
        if(pd.isnull(accident_data['CONTRIBUTING FACTOR VEHICLE 2']) == False):
            vehicle_type_2 = Literal(accident_data['CONTRIBUTING FACTOR VEHICLE 2'], datatype=XSD['string'])
            graph.add((accident, VOCAB['contributing_factor_2'], vehicle_type_2))

        if(pd.isnull(accident_data['CONTRIBUTING FACTOR VEHICLE 3']) == False):
            vehicle_type_3 = Literal(accident_data['CONTRIBUTING FACTOR VEHICLE 3'], datatype=XSD['string'])
            graph.add((accident, VOCAB['contributing_factor_3'], vehicle_type_3))

        graph.add((accident, RDFS.label, collision_id))

        graph.add((accident, GEO['Point'], geo))
        graph.add((geo, GEO['lat'], lat))
        graph.add((geo, GEO['long'], lon))

        graph.add((accident, VOCAB['date'], crash_date))
        graph.add((accident, VOCAB['borough'], borough))
        graph.add((accident, VOCAB['zip'], zip))
        # graph.add((accident, VOCAB['street'], street))
        graph.add((accident, VOCAB['vehicle_type_1'], vehicle_type_1))
        graph.add((accident, VOCAB['contributing_factor_1'], contributing_factor_1))

        graph.add((accident, VOCAB['persons_injured'], persons_injured))
        graph.add((accident, VOCAB['persons_killed'], persons_killed))
        graph.add((accident, VOCAB['pedestrians_injured'], pedestrians_injured))
        graph.add((accident, VOCAB['pedestrians_killed'], pedestrians_killed))

        # just for debugging purposes
        if((index % 10000) == 0):
            print("done with " + str(rows) + "0,000 rows")
            rows += 1

    __save__(graph, output_file)
