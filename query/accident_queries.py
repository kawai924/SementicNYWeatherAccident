from tabulate import tabulate
from rdflib import Graph
import requests
import pandas as pd

accident_rdf_location = "./data/rdf/"
accidentNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/accident#'

"""
How-to query graph in rdflib using sparql: https://www.oreilly.com/library/view/programming-the-semantic/9780596802141/ch04.html
"""
def start(input_file):
    accident_graph = Graph()
    # add rdf accident ontology
    accident_graph.parse(accident_rdf_location + 'accidents.rdf', format='xml')

    print("First query...")
    # get all accidents in Brooklyn (without inference)
    # results = accident_graph.query("""SELECT ?accident ?borough
    #            WHERE {
    #            ?accident act:hasBorough ?borough .
    #            ?borough rdfs:label "Brooklyn" .
    #             }""", initNs={'act': accidentNamespace})

    # better human readable output
    results = accident_graph.query("""SELECT ?accident ?borough
               WHERE {
               ?accidentRes act:hasBorough ?boroughRes .
               ?accidentRes rdfs:label ?accident .
               ?boroughRes rdfs:label "Brooklyn" .
               ?boroughRes rdfs:label ?borough
                }""", initNs={'act': accidentNamespace})

    """ @todo: make function for printing the result """
    Accident = [] # use list of lists instead
    Borough = []
    for triple in results: # find nicer way to extract all columns
        Accident.append(triple[0])
        Borough.append(triple[1])
        # print(triple)

    list = zip(Accident, Borough)
    df = pd.DataFrame(list, columns=['Accident', 'Borough'])
    # displaying the DataFrame
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    print("\nSecond query...")
    # get all accidents in Brooklyn (with inference)
    results = accident_graph.query("""SELECT ?accident ?borough
               WHERE { 
               ?accident act:inZipCode ?zipcode .
               ?borough rdfs:label "Brooklyn".
               ?borough act:containsZipCode ?zipcode .
                }""", initNs={'act': accidentNamespace})

    """ @todo: make function for printing the result """
    Accident = []
    Borough = []
    for triple in results:
        Accident.append(triple[0])
        Borough.append(triple[1])

    list = zip(Accident, Borough)
    df = pd.DataFrame(list, columns=['Accident', 'Borough'])
    # displaying the DataFrame
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
