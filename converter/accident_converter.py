import pandas as pd
from iribaker import to_iri
from rdflib import URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD, Graph, BNode

resource = 'http://github.com/kawai924/SementicNYWeatherAccident/resource/'
vocabulary = 'http://github.com/kawai924/SementicNYWeatherAccident/vocabulary/'
geocoord = 'http://www.w3.org/2003/01/geo/wgs84_pos#'
accidentVocab = 'http://github.com/kawai924/SementicNYWeatherAccident/accident#'
voc_location = "./vocabulary/"

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
    ACC = Namespace(accidentVocab)
    return RESOURCES, VOCABULARY, GEO, ACC


def __setup_graph__(res, vocab):
    graph = Graph()
    graph.bind('data', res)
    graph.bind('vocab', vocab)
    graph.bind('geo', geocoord)
    graph.bind('acc', accidentVocab)
    return graph


def __save__(graph, file_path):
    f = open(file_path, "wb")
    f.write(graph.serialize(format='xml'))
    f.close()


def convert_to_rdf(input_file, output_file):
    rows = 0

    data = __load__(input_file)
    RES, VOCAB, GEO, ACC = __setup_namespace__()
    graph = __setup_graph__(RES, VOCAB)
    graph.parse(voc_location + 'accident.ttl', format='turtle')

    filter2020 = data.loc[data['CRASH DATE'].str.split('/', expand=True)[2] == '2018']
                          # or data['CRASH DATE'].str.split('/', expand=True)[2] == '2019'
                          # or data['CRASH DATE'].str.split('/', expand=True)[2] == '2018']

    for index, accident_data in filter2020.iterrows():

        # Collision_id is primary key
        accident = URIRef(to_iri(resource + str(accident_data['COLLISION_ID'])))
        collision_id = Literal(accident_data['COLLISION_ID'], datatype=XSD['integer'])

        # change this to already existing namespace?
        crash_date = Literal(accident_data['CRASH DATE'], datatype=XSD['string'])    # change this to xsd:date

        # create new resource called Address:
        vehicleAccident = URIRef(to_iri(accidentVocab + 'VehicleAccident'))
        borough = URIRef(to_iri(accidentVocab + str(accident_data['BOROUGH']).capitalize()))

        if (pd.isnull(accident_data['ZIP CODE']) == False):
            zip = Literal(int(accident_data['ZIP CODE']), datatype=XSD['integer'])
            graph.add((accident, ACC['hasZipcode'], zip))
        # include location

        geo = URIRef(to_iri(geocoord + str(accident_data['COLLISION_ID'])))
        lat = Literal(accident_data['LATITUDE'], datatype=XSD['double'])
        lon = Literal(accident_data['LONGITUDE'], datatype=XSD['double'])

        if (pd.isnull(accident_data['ON STREET NAME']) == False):
            street = Literal(accident_data['ON STREET NAME'].rstrip(), datatype=XSD['string'])
            graph.add((accident, VOCAB['street'], street))

        persons_injured = Literal(accident_data['NUMBER OF PERSONS INJURED'], datatype=XSD['integer'])
        persons_killed = Literal(accident_data['NUMBER OF PERSONS KILLED'], datatype=XSD['integer'])
        pedestrians_injured = Literal(accident_data['NUMBER OF PEDESTRIANS INJURED'], datatype=XSD['integer'])
        pedestrians_killed = Literal(accident_data['NUMBER OF PEDESTRIANS KILLED'], datatype=XSD['integer'])

        vehicleTypeString = accident_data['VEHICLE TYPE CODE 1']
        if(len(accident_data['VEHICLE TYPE CODE 1'].split('/')) > 1):
            vehicleTypeString = accident_data['VEHICLE TYPE CODE 1'].split('/')[0].replace(" ", "")

        vehicleType = URIRef(to_iri(accidentVocab + vehicleTypeString))
        vehicle_type_1 = Literal(vehicleTypeString, datatype=ACC + vehicleTypeString)
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

        # graph.add((accident, GEO['Point'], geo))
        graph.add((accident, RDF.type, vehicleAccident))
        graph.add((accident, GEO['lat'], lat))
        graph.add((accident, GEO['long'], lon))

        graph.add((accident, ACC['hasCrashDate'], crash_date))
        graph.add((borough, RDF.type, borough))
        graph.add((accident, ACC['hasBorough'], borough))

        graph.add((vehicleType, RDF.type, vehicleType))
        graph.add((accident, ACC['hasVehicleType'], vehicleType))
        graph.add((accident, VOCAB['contributing_factor_1'], contributing_factor_1))

        graph.add((accident, ACC['hasPersonsInjured'], persons_injured))
        graph.add((accident, ACC['hasPersonsKilled'], persons_killed))
        graph.add((accident, ACC['hasPedestriansInjured'], pedestrians_injured))
        graph.add((accident, ACC['hasPedestriansKilled'], pedestrians_killed))

        # just for debugging purposes
        if((index % 10000) == 0):
            print("done with " + str(rows) + "0,000 rows")
            rows += 1

    __save__(graph, output_file)
