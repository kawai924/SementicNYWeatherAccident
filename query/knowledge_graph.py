from enum import Enum
from rdflib import Graph, RDF
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
                print("\tUnzipping rdf files...")
                # How to unzip files using python: https://stackoverflow.com/questions/3451111/unzipping-files-in-python
                with zipfile.ZipFile(rdf_location + 'output_rdfs.zip', 'r') as zip_ref:
                    zip_ref.extractall(rdf_location)
                print("\tDone unzipping rdf files")

            try:
                # add ontologies for accident, weather station and weather type
                Knowledge_Graph.__instance__.parse(rdf_location + 'NY_accident.rdf', format='xml') # act prefix
                Knowledge_Graph.__instance__.parse(rdf_location + 'NYstation.rdf', format='xml') # STA prefix
                Knowledge_Graph.__instance__.parse(rdf_location + 'NY_weather_type.rdf', format='xml') # wea prefix
                Knowledge_Graph.__instance__.parse(rdf_location + 'NY_weather_number.rdf', format='xml') # wean prefix
                print("Done loading data into knowledge graph")

            except FileNotFoundError:
                print("Could not load data into graph. Do the names of the rdf files match the unzipped filenames?")

        else:
            raise Exception("You cannot create a class of Knowledge_Graph")

    @staticmethod
    def get_graph_instance():
        if not Knowledge_Graph.__instance__:
            Knowledge_Graph()
        return Knowledge_Graph.__instance__


"""
Represents all namespaces used in the knowledge graph
"""
class Namespaces(Enum):
    def __str__(self):
        return '%s' % self.value

    accident = 'http://github.com/kawai924/SementicNYWeatherAccident/accident#'
    station = 'http://github.com/kawai924/SementicNYWeatherAccident/station#',
    weatherType = 'http://github.com/kawai924/SementicNYWeatherAccident/weather#',
    weatherNumber = 'http://github.com/kawai924/SementicNYWeather/stationID#',
    geo = 'http://www.w3.org/2003/01/geo/wgs84_pos#'


""" 
Replaces namespace in resource with prefix for shorter display in output data 
"""
def replace_prefix(data):
    if not data:
        return
    elif str(Namespaces.accident) in data:
        return data.replace(str(Namespaces.accident), "act:")
    elif str(Namespaces.station) in data:
        return data.replace(str(Namespaces.station), "sta:")
    elif str(Namespaces.weatherType) in data:
        return data.replace(str(Namespaces.weatherType), "wea:")
    elif str(Namespaces.weatherNumber) in data:
        return data.replace(str(Namespaces.weatherNumber), "wean:")
    else:
        return data


"""
Returns all namespaces and prefixes used in the graph in html format
"""
def get_text_prefix():
    return "Namespaces and used prefixes:<br>" \
            "act: " + str(Namespaces.accident) + "<br>" \
            "sta: " + str(Namespaces.station) + "<br>" \
            "wea: " + str(Namespaces.weatherType) + "<br>" \
            "wean: " + str(Namespaces.weatherNumber) + "<br><br>"
