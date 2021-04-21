

from tabulate import tabulate
from rdflib import Graph
import pandas as pd
import time

accident_rdf_location = "./data/rdf/"
output_location = "./query/output/"
accidentNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/accident#'
stationsNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/station#'
weatherTypeNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/weather#'

"""
Query : Which borough in NY had the greatest number of accidents due to view obstruction in heavy fog?
Developers : Gayathri Venna and Aditi Tomar
"""


def start():
    start_time = time.time()

    accident_graph = Graph()
    # add ontologies for accident, weather station and weather type
    accident_graph.parse(accident_rdf_location + 'NY_accident.rdf', format='xml')
    accident_graph.parse(accident_rdf_location + 'NYstation.rdf', format='xml')
    accident_graph.parse(accident_rdf_location + 'NY_weather_type.rdf', format='xml')

    print(
        "\nExecuting query ` Which borough in NY had the greatest number of accidents due to view obstruction in heavy fog?`...")
    results = accident_graph.query("""
               PREFIX act: <http://github.com/kawai924/SementicNYWeatherAccident/accident#>
               PREFIX STA: <http://github.com/kawai924/SementicNYWeatherAccident/station#>
               PREFIX wea: <http://github.com/kawai924/SementicNYWeatherAccident/weather#>
               SELECT DISTINCT ?accident ?borough ?location ?zipcode ?date ?station ?weather ?station_type
               WHERE {
                       ?accident a act:VehicleAccident;
                                 rdfs:label ?id;
                                 act:hasDate ?date;
                                 act:inLocation ?location;
                                 act:hasContributingFactor ?factor.

                       FILTER(REGEX(?factor, "View Obstructed")).
                       {?location act:inBorough ?borough} UNION {?accident act:hasBorough ?borough}. 
                        
                       OPTIONAL {?accident act:inZipCode ?zipcode}

                       ?station STA:county "QUEENS"^^xsd:string.
                       ?station_type STA:station_id ?station;
                                     wea:onDate ?date;
                                     wea:hasWeatherType ?weather.
                       FILTER(?weather = "Heavy Fog"^^xsd:string)
               }
               GROUP BY ?accident
               ORDER BY MONTH(?date)
                """, initNs={'act': accidentNamespace, 'STA': stationsNamespace, 'wea': weatherTypeNamespace})


    Accident = []
    Borough = []
    Location = []
    Zip = []
    Date = []
    Station_id = []
    Weather = []
    Station_type = []
    for triple in results:
        Accident.append(replace_prefix(triple[0]))
        Borough.append(replace_prefix(triple[1]))
        Location.append(replace_prefix(triple[2]))
        Zip.append(replace_prefix(triple[3]))
        Date.append(replace_prefix(triple[4]))
        Station_id.append(replace_prefix(triple[5]))
        Weather.append(replace_prefix(triple[6]))
        Station_type.append(replace_prefix(triple[7]))

    list = zip(Accident, Borough, Location, Zip, Date, Station_id, Weather, Station_type)
    df = pd.DataFrame(list, columns=['Accident', 'Borough', 'Location', 'Zipcode', 'Date', 'Station ID', 'Weather',
                                     'Station Type'])
    # displaying the DataFrame
    # print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    with open(output_location + 'borough-accident.txt', 'w') as f:
        f.write(
            ' Which borough in NY had the greatest number of accidents due to view obstruction in heavy fog? ---- Answer: ' +
            str(df['Borough'].value_counts().idxmax()) + '\n\n')
        f.write(tabulate(df, headers='keys', tablefmt='psql', showindex=False))


    print('Answer to the query:' + str(df['Borough'].value_counts().idxmax()))
    print("Execution took: %.2f seconds" % (time.time() - start_time))





def replace_prefix(data):
    if not data:
        return
    elif accidentNamespace in data:
        return data.replace(accidentNamespace, "act:")
    elif stationsNamespace in data:
        return data.replace(stationsNamespace, "sta:")
    elif weatherTypeNamespace in data:
        return data.replace(weatherTypeNamespace, "wea:")
    else:
        return data
