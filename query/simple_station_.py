from query.knowledge_graph import Knowledge_Graph
import pandas as pd

output_location = "./query/output/"

"""
Query: Which weather station is located in the county of Ontario?
Developer: Dennis Lo
"""
def start():
    g = Knowledge_Graph.get_graph_instance()


    qres = g.query(
        """
        SELECT ?name ?station ?county ?station_id ?lat ?long
        where {
            ?station STA:county ?county;
                    STA:station_id ?station_id;
                    geo:lat ?lat;
                    geo:long ?long;
                    rdfs:label ?name.
            filter (?county = 'ONTARIO')
        }
        """)

    name, station, county, lat, long, station_id = [], [], [], [], [], []

    for row in qres:
        # print(row)
        name.append(row.asdict()['name'].toPython())
        station_id.append(row.asdict()['station_id'].toPython())
        county.append(row.asdict()['county'].toPython())
        lat.append(row.asdict()['lat'].toPython())
        long.append(row.asdict()['long'].toPython())
        station.append(row.asdict()['station'].toPython())

    df = pd.DataFrame({"Name":name, "Station_id":station_id, "County":county, "Lat":lat, "Long":long, "Station_URI":station})



    # now create the html page and write the data...
    f=open(output_location + 'simple_station.html', 'w')
    f.write(df.to_html())
    f.close()
