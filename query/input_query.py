
import pandas as pd
import time
from query.knowledge_graph import Knowledge_Graph


accident_rdf_location = "./data/rdf/"
output_location = "./query/output/"
accidentNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/accident#'
stationsNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/station#'
weatherTypeNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/weather#'
weatherNumberNamespace = 'http://github.com/kawai924/SementicNYWeather/stationID#'
geoNamespace = 'http://www.w3.org/2003/01/geo/wgs84_pos#'

"""
Query : Since, it is taking time to load the RDFs , built this query to load the RDFs once, and ask for input , 
we can paste the python query in terminal and it will execute successfully giving the result if there is 
no error OR it will throw an error if something is wrong.In either cases, it will again ask user to input query to run.
Developers : Aditi Tomar and Gayathri Venna
"""


"""
How-to query graph in rdflib using sparql: https://www.oreilly.com/library/view/programming-the-semantic/9780596802141/ch04.html
"""
def start():
    
    accident_graph = Knowledge_Graph.get_graph_instance()

    while True:
        execute(accident_graph)


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


def executeQuery(query, accident_graph):
    start_time = time.time()
    results = accident_graph.query(query, initNs={'act': accidentNamespace, 'STA': stationsNamespace,
                                                  'wea': weatherTypeNamespace, 'wean': weatherNumberNamespace, 'geo': geoNamespace})

    with open(output_location + 'query.txt', 'w') as f:
        f.write(query)
        f.close()
    f = open(output_location + 'query.txt', "r")
    with open(output_location + "input_results.html", "w") as e:
        for lines in f.readlines():
            e.write("<pre>" + lines + "</pre>")
        df = pd.DataFrame(results)
        e.write(df.to_html())
        e.close()

    print("Execution took: %.2f seconds" % (time.time() - start_time))
    print("Done with this query!\n You can try another one if you like\n\n")


def execute(accident_graph):
    print("Enter/Paste your query. Once done enter new line and write ;;")
    contents = ""
    while True:
        line = input()
        if line == ";;":
            break
        else:
            contents = contents + "\n" + line
    query = contents
    # print("\n Executing query " + query)  # for debugging purposes
    executeQuery(query, accident_graph)
