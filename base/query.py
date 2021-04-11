
import rdflib
import pandas as pd
g = rdflib.Graph()

# ... add some triples to g somehow ...
g.parse('../data/rdf/NYstation.rdf')
# g.serialize(format='JSON')
#
# qres = g.query(
#     """
#     SELECT ?a ?station_id ?county ?lat ?long
#     where {
#         ?a STA:county ?county.
#         ?a STA:station_id ?station_id.
#         ?a geo:lat ?lat.
#         ?a geo:long ?long.
#         filter (?county = 'ONTARIO')
#     }
#     """)

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
f=open('webpage.html','w')
f.write(df.to_html())
f.close()


# call  python3 -m http.server 8000
# to host the folder and open result.html
