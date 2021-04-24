import pandas as pd
import time
from query.knowledge_graph import Knowledge_Graph

output_location = "./query/output/"
accidentNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/accident#'
stationsNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/station#'
weatherTypeNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/weather#'

"""
Query: What are the top 5 vehicle types that were involved in the most accidents in Manhattan due to ice?
Developer: Andreas Saplacan
"""
def start():
    start_time = time.time()  # time execution

    graph = Knowledge_Graph.get_graph_instance()

    print(
        "Executing query `What are the top 5 vehicle types that were involved in the most accidents in Manhattan due to ice?`...")
    results = graph.query("""
               PREFIX act: <http://github.com/kawai924/SementicNYWeatherAccident/accident#>
               PREFIX STA: <http://github.com/kawai924/SementicNYWeatherAccident/station#>
               PREFIX wea: <http://github.com/kawai924/SementicNYWeatherAccident/weather#>
               SELECT DISTINCT ?vehicle_type (COUNT(?vehicle_type) AS ?num)
               WHERE {
                       ?accident a act:VehicleAccident;
                                 rdfs:label ?id;
                                 act:hasDate ?date;
                                 act:inLocation ?location;
                                 act:hasVehicleType ?vehicle_type.

                       {?location act:inBorough ?borough} UNION {?accident act:hasBorough ?borough}. 
                       ?borough rdf:type act:Manhattan.

                       ?station STA:county "NEW YORK"^^xsd:string.
                       ?station_type STA:station_id ?station.
                       ?station_type wea:onDate ?date.
                       ?station_type wea:hasWeatherType ?weather.
                                     
                       FILTER(REGEX(?weather, "glaze", "i") || REGEX(?weather, "ice", "i"))
               }
               GROUP BY ?vehicle_type
               ORDER BY DESC (?num)
               LIMIT 5
                """, initNs={'act': accidentNamespace, 'STA': stationsNamespace, 'wea': weatherTypeNamespace})

    Vehicle_type, numofAcc = [], []
    for triple in results:
        Vehicle_type.append(replace_prefix(triple[0]))
        numofAcc.append(triple[1])

    list = zip(Vehicle_type, numofAcc)
    df = pd.DataFrame(list, columns=['Vehicle Type', 'Number of Accidents'])
    # displaying the DataFrame
    # print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    print('exporting to html')
    f = open(output_location + 'vehicle_type_ice.html', 'w')
    f.write('<h3><b>'
            'What are the top 5 vehicle types that were involved in the most accidents in Manhattan due to ice?'
            '</b></h3>')
    f.write(get_text_prefix())
    f.write(df.to_html(index=False))
    f.close()

    print('Answer to the query: ' + str(Vehicle_type))
    print("Execution took: %.2f seconds" % (time.time() - start_time))


""" Replaces namespace in resource with prefix for shorter display in output data """
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


def get_text_prefix():
    return "Namespaces and used prefixes:<br>" \
           "act: http://github.com/kawai924/SementicNYWeatherAccident/accident#<br>" \
           "sta: http://github.com/kawai924/SementicNYWeatherAccident/station#<br>" \
           "wea: http://github.com/kawai924/SementicNYWeatherAccident/weather#<br><br>"
