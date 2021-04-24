import pandas as pd
import time
from query.knowledge_graph import Knowledge_Graph

output_location = "./query/output/"
accidentNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/accident#'
stationsNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/station#'
weatherTypeNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/weather#'


"""
Query: How many accidents in Queens could have been caused by Distraction due to Thunder in 2020?
Developer: Andreas Saplacan
"""
def start():
    start_time = time.time()  # time execution

    accident_graph = Knowledge_Graph.get_graph_instance()

    print("Executing query `How many accidents in Queens could have been caused by Distraction due to Thunder in 2020?`...")
    results = accident_graph.query("""
               PREFIX act: <http://github.com/kawai924/SementicNYWeatherAccident/accident#>
               PREFIX STA: <http://github.com/kawai924/SementicNYWeatherAccident/station#>
               PREFIX wea: <http://github.com/kawai924/SementicNYWeatherAccident/weather#>
               SELECT DISTINCT ?accident ?borough ?location ?zipcode ?date ?station ?weather ?station_type 
                               (COUNT(DISTINCT ?accident) AS ?numOfAcc) # count num of accidents
               WHERE {
                       ?accident a act:VehicleAccident;
                                 rdfs:label ?id;
                                 act:hasDate ?date;
                                 act:inLocation ?location;
                                 act:hasContributingFactor ?factor.
                       
                       FILTER(REGEX(?factor, "Distraction")).
                       {?location act:inBorough ?borough} UNION {?accident act:hasBorough ?borough}. 
                       ?borough rdf:type act:Queens.
                       OPTIONAL {?accident act:inZipCode ?zipcode}
                       
                       ?station STA:county "QUEENS"^^xsd:string.
                       ?station_type STA:station_id ?station;
                                     wea:onDate ?date;
                                     wea:hasWeatherType ?weather.
                       FILTER(?weather = "Thunder"^^xsd:string)
               }
               GROUP BY ?accident # remove/add comment to display all found instances
               ORDER BY MONTH(?date) # remove/add comment to display all found instances
                """, initNs={'act': accidentNamespace, 'STA': stationsNamespace, 'wea': weatherTypeNamespace})

    Accident, Borough, Location, Zip, Date, Station_id, Weather, Station_type = [], [], [], [], [], [], [], []
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

    print('exporting to html')
    f = open(output_location + 'accidents-queens-thunder.html', 'w')
    f.write('<h3><b>'
            'How many accidents in Queens could have been caused by Distraction due to Thunder in 2020?<br> '
            'Answer: ' + str(len(results)) +
            '</b></h3>')
    f.write(get_text_prefix())
    f.write(df.to_html(index=False))
    f.close()

    print('Answer to the query: ' + str(len(results)))
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
