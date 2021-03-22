import pandas as pd
from iribaker import to_iri
from rdflib import URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD, Graph, BNode
from converter.accident_columns import isValidVehicle

resource = 'http://github.com/kawai924/SementicNYWeatherAccident/resource/'
vocabulary = 'http://github.com/kawai924/SementicNYWeatherAccident/vocabulary/'
geocoord = 'http://www.w3.org/2003/01/geo/wgs84_pos#'
accidentVocab = 'http://github.com/kawai924/SementicNYWeatherAccident/accident#'
ontology_location = "./ontology/"

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
    print('----> Finished parsing csv, saving graph to rdf...')
    f = open(file_path, "wb")
    f.write(graph.serialize(format='xml'))
    f.close()


def convert_to_rdf(input_file, output_file):
    rows = 0

    data = __load__(input_file)
    RES, VOCAB, GEO, ACC = __setup_namespace__()
    graph = __setup_graph__(RES, VOCAB)
    # add accident ontology created via protege
    graph.parse(ontology_location + 'accident.ttl', format='turtle')

    # filter for a specific year
    filter2020 = data.loc[data['CRASH DATE'].str.split('/', expand=True)[2] == '2020']

    for index, accident_data in filter2020.iterrows():

        # Collision_id is primary key
        accident = URIRef(to_iri(resource + str(accident_data['COLLISION_ID'])))
        vehicleAccident = URIRef(to_iri(accidentVocab + 'VehicleAccident'))
        collision_id = Literal(accident_data['COLLISION_ID'], datatype=XSD['integer'])

        # add accident to graph
        graph.add((accident, RDFS.label, collision_id))
        graph.add((accident, RDF.type, vehicleAccident))

        # setup and add crash date to graph as resource
        crash_date_raw = accident_data['CRASH DATE'].split('/')
        crash_date_formatted = crash_date_raw[2] + "-" + crash_date_raw[0] + "-" + crash_date_raw[1]
        crash_date = Literal(crash_date_formatted, datatype=XSD['date'])
        graph.add((accident, ACC['hasCrashDate'], crash_date))

        borough_raw = str(accident_data['BOROUGH']).split(" ")
        borough_data = [b.capitalize() for b in borough_raw]

        # setup and add borough data as resource, only if its defined in current instance
        # borough_data = str(accident_data['BOROUGH']).capitalize()
        if (''.join(borough_data) != 'Nan'):
            borough = URIRef(to_iri(accidentVocab + ''.join(borough_data)))
            graph.add((borough, RDF.type, borough))
            graph.add((borough, RDFS.label, Literal(''.join(borough_data))))
            graph.add((accident, ACC['hasBorough'], borough))

        # setup and add zipcode data as resource, only if its defined in current instance
        if (pd.isnull(accident_data['ZIP CODE']) == False):
            zip = URIRef(to_iri(accidentVocab + str(int(accident_data['ZIP CODE']))))
            graph.add((zip, RDFS.label, Literal(int(accident_data['ZIP CODE']))))
            graph.add((accident, ACC['inZipcode'], zip))
            if (''.join(borough_data) != 'Nan'):
                graph.add((borough, ACC['hasZipcode'], zip))

        # setup and add geo coordinates to graph as literals
        lat = Literal(accident_data['LATITUDE'] if pd.isnull(accident_data['LATITUDE']) == False else 0, datatype=XSD['double'])
        lon = Literal(accident_data['LONGITUDE'] if pd.isnull(accident_data['LONGITUDE']) == False else 0, datatype=XSD['double'])
        graph.add((accident, GEO['lat'], lat))
        graph.add((accident, GEO['long'], lon))

        # setup and add location to graph as resource (used to map to borough if only location is available)
        # 3 decimal values will ensure a precision of 111m
        # location_data = '%.3f'%(accident_data['LATITUDE']) + ',' + '%.3f'%(accident_data['LONGITUDE'])
        # if(location_data != "nan,nan" and location_data != '0.000,0.000'):
        #     location = URIRef(to_iri(accidentVocab + location_data))
        #     if ''.join(borough_data) != 'Nan':
        #         graph.add((borough, ACC['hasLocation'], location))
        #     graph.add((accident, ACC['inLocation'], location))

        # setup and add street name to graph as resource
        if (pd.isnull(accident_data['ON STREET NAME']) == False):
            streets = accident_data['ON STREET NAME'].rstrip().split(" ")
            street = [s.capitalize() for s in streets]
            street_data = Literal(''.join(street), datatype=XSD['string'])
            # street_data = URIRef(to_iri(accidentVocab + ''.join(street)))
            graph.add((accident, ACC['hasStreetName'], street_data))

        # setup and add person and pedestrian data to graph as literals
        persons_injured = Literal(int(accident_data['NUMBER OF PERSONS INJURED']), datatype=XSD['integer'])
        graph.add((accident, ACC['hasPersonsInjured'], persons_injured))

        persons_killed = Literal(int(accident_data['NUMBER OF PERSONS KILLED']), datatype=XSD['integer'])
        graph.add((accident, ACC['hasPersonsKilled'], persons_killed))

        pedestrians_injured = Literal(int(accident_data['NUMBER OF PEDESTRIANS INJURED']), datatype=XSD['integer'])
        graph.add((accident, ACC['hasPedestriansInjured'], pedestrians_injured))

        pedestrians_killed = Literal(int(accident_data['NUMBER OF PEDESTRIANS KILLED']), datatype=XSD['integer'])
        graph.add((accident, ACC['hasPedestriansKilled'], pedestrians_killed))

        # setup and add vehicle types involved in the accident to graph as resource
        vehicleType1_split = str(accident_data['VEHICLE TYPE CODE 1']).split(' ')
        vehicleType1_data = ''.join([v.capitalize() for v in vehicleType1_split])
        if(len(vehicleType1_data.split('/')) > 1):
            vehicleType1_data = vehicleType1_data.split('/')[0]

        if(vehicleType1_data != 'Nan' and isValidVehicle(vehicleType1_data)):
            vehicleType1 = URIRef(to_iri(accidentVocab + vehicleType1_data))
            graph.add((vehicleType1, RDF.type, vehicleType1))
            graph.add((accident, ACC['hasVehicleType'], vehicleType1))

        if (pd.isnull(accident_data['VEHICLE TYPE CODE 2']) == False):
            vehicleType2_split = str(accident_data['VEHICLE TYPE CODE 2']).split(' ')
            vehicleType2_data = ''.join([v.capitalize() for v in vehicleType2_split])
            if(len(vehicleType2_data.split('/')) > 1):
                vehicleType2_data = vehicleType2_data.split('/')[0]

            if (vehicleType2_data != 'Nan' and isValidVehicle(vehicleType2_data)):
                vehicleType2 = URIRef(to_iri(accidentVocab + vehicleType2_data))
                graph.add((vehicleType2, RDF.type, vehicleType2))
                graph.add((accident, ACC['hasVehicleType'], vehicleType2))

        if (pd.isnull(accident_data['VEHICLE TYPE CODE 3']) == False):
            vehicleType3_split = str(accident_data['VEHICLE TYPE CODE 3']).split(' ')
            vehicleType3_data = ''.join([v.capitalize() for v in vehicleType3_split])
            if(len(vehicleType3_data.split('/')) > 1):
                vehicleType3_data = vehicleType3_data.split('/')[0].replace(" ", "").capitalize()

            if (vehicleType3_data != 'Nan' and isValidVehicle(vehicleType3_data)):
                vehicleType3 = URIRef(to_iri(accidentVocab + vehicleType3_data))
                graph.add((vehicleType3, RDF.type, vehicleType3))
                graph.add((accident, ACC['hasVehicleType'], vehicleType3))

        # setup and add contributing factors to graph as resource
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
            print("------> Done with " + str(rows) + "0,000 rows...")
            rows += 1

        # only processing 50,000 rows so it can be loaded into protege within reasonable time
        if(rows == 5):
            break

    __save__(graph, output_file)
