import pandas as pd
from iribaker import to_iri
from rdflib import URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD, Graph, BNode

resource = 'http://github.com/kawai924/SementicNYWeatherAccident/resource/'
vocabulary = 'http://github.com/kawai924/SementicNYWeatherAccident/vocabulary/'
geocoord = 'http://www.w3.org/2003/01/geo/wgs84_pos#'
accidentVocab = 'http://github.com/kawai924/SementicNYWeatherAccident/accident#'
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

    filter2020 = data.loc[data['CRASH DATE'].str.split('/', expand=True)[2] == '2020']
                          # or data['CRASH DATE'].str.split('/', expand=True)[2] == '2019'
                          # or data['CRASH DATE'].str.split('/', expand=True)[2] == '2018']

    for index, accident_data in filter2020.iterrows():

        # Collision_id is primary key
        accident = URIRef(to_iri(resource + str(accident_data['COLLISION_ID'])))
        vehicleAccident = URIRef(to_iri(accidentVocab + 'VehicleAccident'))
        collision_id = Literal(accident_data['COLLISION_ID'], datatype=XSD['integer'])

        graph.add((accident, RDFS.label, collision_id))
        graph.add((accident, RDF.type, vehicleAccident))

        # change this to already existing namespace?
        crash_date_raw = accident_data['CRASH DATE'].split('/')
        crash_date_formatted = crash_date_raw[2] + "-" + crash_date_raw[0] + "-" + crash_date_raw[1]
        crash_date = Literal(crash_date_formatted, datatype=XSD['date'])
        graph.add((accident, ACC['hasCrashDate'], crash_date))

        # create new resource called Address:
        borough_raw = str(accident_data['BOROUGH']).split(" ")
        borough_data = [b.capitalize() for b in borough_raw]

        # borough_data = str(accident_data['BOROUGH']).capitalize()
        borough = URIRef(to_iri(accidentVocab + ''.join(borough_data)))
        graph.add((borough, RDF.type, borough))
        graph.add((accident, ACC['hasBorough'], borough))

        if (pd.isnull(accident_data['ZIP CODE']) == False):
            zip = URIRef(to_iri(accidentVocab + str(int(accident_data['ZIP CODE']))))
            graph.add((borough, ACC['hasZipcode'], zip))

        lat = Literal(accident_data['LATITUDE'] if pd.isnull(accident_data['LATITUDE']) == False else 0, datatype=XSD['double'])
        lon = Literal(accident_data['LONGITUDE'] if pd.isnull(accident_data['LONGITUDE']) == False else 0, datatype=XSD['double'])
        graph.add((accident, GEO['lat'], lat))
        graph.add((accident, GEO['long'], lon))

        location_data = '%.4f'%(accident_data['LATITUDE']) + ',' + '%.4f'%accident_data['LONGITUDE']
        if(borough != 'Nan' and location_data != "nan,nan"):
            location = URIRef(to_iri(accidentVocab + location_data))
            graph.add((borough, ACC['hasLocation'], location))

        if (pd.isnull(accident_data['ON STREET NAME']) == False):
            streets = accident_data['ON STREET NAME'].rstrip().split(" ")
            street = [s.capitalize() for s in streets]
            street_data = URIRef(to_iri(accidentVocab + ''.join(street)))
            # graph.add((street_data, RDF.type, XSD['string']))
            graph.add((accident, ACC['hasStreetName'], street_data))

        persons_injured = Literal(int(accident_data['NUMBER OF PERSONS INJURED']), datatype=XSD['integer'])
        graph.add((accident, ACC['hasPersonsInjured'], persons_injured))

        persons_killed = Literal(int(accident_data['NUMBER OF PERSONS KILLED']), datatype=XSD['integer'])
        graph.add((accident, ACC['hasPersonsKilled'], persons_killed))

        pedestrians_injured = Literal(int(accident_data['NUMBER OF PEDESTRIANS INJURED']), datatype=XSD['integer'])
        graph.add((accident, ACC['hasPedestriansInjured'], pedestrians_injured))

        pedestrians_killed = Literal(int(accident_data['NUMBER OF PEDESTRIANS KILLED']), datatype=XSD['integer'])
        graph.add((accident, ACC['hasPedestriansKilled'], pedestrians_killed))

        vehicleType1_data = str(accident_data['VEHICLE TYPE CODE 1']).replace(" ", "")
        if(len(vehicleType1_data.split('/')) > 1):
            vehicleType1_data = accident_data['VEHICLE TYPE CODE 1'].split('/')[0].replace(" ", "")

        vehicleType1 = URIRef(to_iri(accidentVocab + vehicleType1_data))
        graph.add((vehicleType1, RDF.type, vehicleType1))
        graph.add((accident, ACC['hasVehicleType'], vehicleType1))

        # vehicle_type_1 = Literal(vehicleType1_data, datatype=ACC + vehicleType1_data)
        if (pd.isnull(accident_data['VEHICLE TYPE CODE 2']) == False):
            vehicleType2_data = str(accident_data['VEHICLE TYPE CODE 2']).replace(" ", "")
            if(len(vehicleType2_data.split('/')) > 1):
                vehicleType2_data = accident_data['VEHICLE TYPE CODE 2'].split('/')[0].replace(" ", "")

            vehicleType2 = URIRef(to_iri(accidentVocab + vehicleType2_data))
            graph.add((vehicleType2, RDF.type, vehicleType2))
            graph.add((accident, ACC['hasVehicleType'], vehicleType2))

        if (pd.isnull(accident_data['VEHICLE TYPE CODE 3']) == False):
            vehicleType3_data = str(accident_data['VEHICLE TYPE CODE 3']).replace(" ", "")
            if(len(vehicleType3_data.split('/')) > 1):
                vehicleType3_data = accident_data['VEHICLE TYPE CODE 3'].split('/')[0].replace(" ", "")

            vehicleType3 = URIRef(to_iri(accidentVocab + vehicleType3_data))
            graph.add((vehicleType3, RDF.type, vehicleType3))
            graph.add((accident, ACC['hasVehicleType'], vehicleType3))

        if(accident_data['CONTRIBUTING FACTOR VEHICLE 1'] != 'Unspecified'):
            contributing_factor_1 = URIRef(to_iri(accidentVocab + str(accident_data['CONTRIBUTING FACTOR VEHICLE 1'])))
            graph.add((accident, ACC['hasContributingFactor'], contributing_factor_1))

        if(pd.isnull(accident_data['CONTRIBUTING FACTOR VEHICLE 2']) == False and accident_data['CONTRIBUTING FACTOR VEHICLE 2'] != 'Unspecified'):
            contributing_factor_2 = URIRef(to_iri(accidentVocab + str(accident_data['CONTRIBUTING FACTOR VEHICLE 2'])))
            graph.add((accident, ACC['hasContributingFactor'], contributing_factor_2))

        if(pd.isnull(accident_data['CONTRIBUTING FACTOR VEHICLE 3']) == False and accident_data['CONTRIBUTING FACTOR VEHICLE 3'] != 'Unspecified'):
            contributing_factor_3 = URIRef(to_iri(accidentVocab + str(accident_data['CONTRIBUTING FACTOR VEHICLE 3'])))
            graph.add((accident, ACC['hasContributingFactor'], contributing_factor_3))

        # just for debugging purposes
        if((index % 10000) == 0):
            print("done with " + str(rows) + "0,000 rows")
            rows += 1

    __save__(graph, output_file)
