import csv
from iribaker import to_iri
from rdflib import URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD, Graph

filename = "./data/csv/example.csv"
output = "./data/rdf/"
vocabulary = "./vocabulary/"

# Example taken from: https://github.com/KRontheWeb/csv2rdf-tutorial
# and: https://rdflib.readthedocs.io/en/stable/gettingstarted.html
def start():
    with open(filename, 'r') as csvfile: # change this to use pandas
        csv_contents = [{k: v for k, v in row.items()}
                        for row in csv.DictReader(csvfile, skipinitialspace=True, quotechar='"', delimiter=';')]

    # A namespace for our resources
    data = 'http://data.krw.d2s.labs.vu.nl/group20/resource/'
    DATA = Namespace(data)
    # A namespace for our vocabulary items (schema information, RDFS, OWL classes and properties etc.)
    vocab = 'http://data.krw.d2s.labs.vu.nl/group20/vocab/'
    VOCAB = Namespace('http://data.krw.d2s.labs.vu.nl/group20/vocab/')

    # The URI for our graph
    graph_uri = URIRef('http://data.krw.d2s.labs.vu.nl/group20/resource/examplegraph')

    graph = Graph()

    # Load the externally defined schema into the default graph (context) of the dataset/graph
    graph.parse(vocabulary + 'example_vocab.ttl', format='turtle')

    graph.bind('g20data', DATA)
    graph.bind('g20vocab', VOCAB)

    # Let's iterate over the dictionary, and create some triples
    # Let's pretend we know exactly what the 'schema' of our CSV file is
    for row in csv_contents:
        # `Name` is the primary key and we use it as our primary resource, but we'd also like to use it as a label
        person = URIRef(to_iri(data + row['Name']))
        name = Literal(row['Name'], datatype=XSD['string'])
        # `Country` is a resource
        country = URIRef(to_iri(data + row['Country']))
        # But we'd also like to use the name as a label (with a language tag!)
        country_name = Literal(row['Country'], lang='en')
        # `Age` is a literal (an integer)
        age = Literal(int(row['Age']), datatype=XSD['int'])
        # `Favourite Colour` is a resource
        colour = URIRef(to_iri(data + row['Favourite Colour']))
        colour_name = Literal(row['Favourite Colour'], lang='en')
        # `Place` is a resource, but we are now going to prepend the country to avoid ambiguity
        place = URIRef(to_iri(data + row['Country'] + '/' + row['Place']))
        place_name = Literal(row['Place'], lang='en')
        # `Address` is a literal (a string)
        address = Literal(row['Address'], datatype=XSD['string'])
        # `Hobby` is a resource
        hobby = URIRef(to_iri(data + row['Hobby']))
        hobby_name = Literal(row['Hobby'], lang='en')

        # All set... we are now going to add the triples to our graph
        graph.add((person, RDFS.label, name))
        graph.add((person, VOCAB['age'], age))
        graph.add((person, VOCAB['address'], address))

        # Add the place, its label and its type.
        graph.add((person, VOCAB['place'], place))
        graph.add((place, RDFS.label, place_name))

        # Add the country and its label
        graph.add((person, VOCAB['country'], country))
        graph.add((country, RDFS.label, country_name))

        # Add the favourite colour and its label
        graph.add((person, VOCAB['favourite_colour'], colour))
        graph.add((colour, RDFS.label, colour_name))

        # Add the hobby and its label
        graph.add((person, VOCAB['hobby'], hobby))
        graph.add((hobby, RDFS.label, hobby_name))

    with open(output + 'example-simple.rdf', 'wb') as f:
        graph.serialize(f, format='pretty-xml')

