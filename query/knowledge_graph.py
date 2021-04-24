from rdflib import Graph
import zipfile
from os import path

rdf_location = "./data/rdf/"

"""
Creates Singleton of knowledge graph that can be used across different queries

How to create singletons using python: https://stackabuse.com/the-singleton-design-pattern-in-python/
"""
class Knowledge_Graph:
    __instance__ = None

    def __init__(self):
        if Knowledge_Graph.__instance__ is None:
            Knowledge_Graph.__instance__ = Graph()
            print("Loading rdfs into knowledge graph...")

            if not path.exists(rdf_location + 'NYstation.rdf'): # check if rdf files have already been extracted
                print("Unzipping rdf files...")
                # How to unzip files using python: https://stackoverflow.com/questions/3451111/unzipping-files-in-python
                with zipfile.ZipFile(rdf_location + 'output_rdfs.zip', 'r') as zip_ref:
                    zip_ref.extractall(rdf_location)
                print("Done unzipping rdf files")

            try:
                # add ontologies for accident, weather station and weather type
                Knowledge_Graph.__instance__.parse(rdf_location + 'NY_accident.rdf', format='xml') # act prefix
                Knowledge_Graph.__instance__.parse(rdf_location + 'NYstation.rdf', format='xml') # STA prefix
                Knowledge_Graph.__instance__.parse(rdf_location + 'NY_weather_type.rdf', format='xml') # wea prefix
                Knowledge_Graph.__instance__.parse(rdf_location + 'NY_weather_number.rdf', format='xml') # wean prefix
                print("Done loading data into knowledge graph")

            except FileNotFoundError:
                print("Could not load data into graph. Did you unzip output_rdf.zip?")

        else:
            raise Exception("You cannot create a class of Knowledge_Graph")

    @staticmethod
    def get_graph_instance():
        if not Knowledge_Graph.__instance__:
            Knowledge_Graph()
        return Knowledge_Graph.__instance__

