from tabulate import tabulate
import pandas as pd
import time
from query.knowledge_graph import Knowledge_Graph, Namespaces, replace_prefix

output_location = "./query/output/"

"""
Query : Which accident happened due to view obstruction in heavy fog?
Developers : Gayathri Venna and Aditi Tomar
"""


def start():
    start_time = time.time()
    accident_graph = Knowledge_Graph.get_graph_instance()

    print(
        "\nExecuting query `Which accident happened due to view obstruction in heavy fog?`...")
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
                """, initNs={'act': Namespaces.accident, 'STA': Namespaces.station, 'wea': Namespaces.weatherType})


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

    print('exporting to html')
    f = open(output_location + 'heavy_fog_accident.html', 'w')
    f.write('Which accident happened due to view obstruction in heavy fog? ' )
    f.write(df.to_html())
    f.close()

    print("Execution took: %.2f seconds" % (time.time() - start_time))

