import rdflib
import pandas as pd

print("start getting the graphs")
gMer = rdflib.Graph()


print(__file__)
gMer.parse('./../data/rdf/NY_accident.rdf')
gMer.parse('./../data/rdf/NY_weather_number.rdf')

#Upasana

print("start query")
qres = gMer.query("""
        SELECT ?mon ?pKill ?pInjur ?pedKill ?pedInjur ?tKill ?tInjur ?accCount ?avgWind ?avgTemp  
        WHERE {
            {
            select ?mon (sum(?personKill) as ?pKill) (sum(?personInjur) as ?pInjur) 
                   (sum(?pedesKill) as ?pedKill) (sum(?pedesInjur) as ?pedInjur)
                   (sum(?totalKill) as ?tKill) (sum(?totalInjur) as ?tInjur) 
                   (count(?mon) as ?accCount) 
          where {
          ?accident act:hasDate ?aDate;
                    act:hasPersonsKilled ?personKill;
                    act:hasPersonsInjured ?personInjur;
                    act:hasPedestriansKilled ?pedesKill;
                    act:hasPedestriansInjured ?pedesInjur.
             BIND(?personKill + ?pedesKill as ?totalKill)
             BIND(?personInjur + ?pedesInjur as ?totalInjur)
            }
            GROUP BY (substr(xsd:string(?aDate),6,2) as ?mon)
            }
            {
            select ?mon ?sDate ((sum(?averageWS)/count(?mon)) as ?avgWind) 
                   ((sum(?avgT)/count(?mon)) as ?avgTemp)
                   where{
            OPTIONAL {
                    ?stationID wea:hasAWND ?averageWindSpeed;
                               wea:hasTAVG ?averageTemp.
                    }
                    ?stationID rdfs:label ?sDate.
            BIND(xsd:double(?averageWindSpeed) as ?averageWS)
            BIND(?averageTemp/10 as ?avgT)
            }
            GROUP BY (substr(xsd:string(?sDate),6,2) as ?mon)
            }
        }
        GROUP BY (substr(xsd:string(?aDate),6,2) as ?mon)
        ORDER BY ?mon
    """)

month, pKill,pInjur,pedKill,pedInjur,tKill,tInjur,accCount,avgWind,avgTemp = [], [],[],[],[],[],[],[],[],[]

for row in qres:
    month.append(row.asdict()['mon'].toPython())
    pKill.append(row.asdict()['pKill'].toPython())
    pInjur.append(row.asdict()['pInjur'].toPython())
    tKill.append(row.asdict()['tKill'].toPython())
    pedKill.append(row.asdict()['pedKill'].toPython())
    pedInjur.append(row.asdict()['pedInjur'].toPython())
    tInjur.append(row.asdict()['tInjur'].toPython())
    accCount.append(row.asdict()['accCount'].toPython())
    avgWind.append(row.asdict()['avgWind'].toPython())
    avgTemp.append(row.asdict()['avgTemp'].toPython())


df = pd.DataFrame({"Month":month, "No. of accidents":accCount, "Person Killed":pKill, "Person Injured":pInjur
                            , "Pedestrians Killed":pedKill, "Pedestrians Injured":pedInjur
                            , "Total Killed ":tKill, "Total Injured ":tInjur
                          , "Average Wind ":avgWind, "Average Temperature(C) ":avgTemp})
# print(df)

print("start output")
f=open('output/Monthly_summary.html', 'w')

# f.write("Monthly Summary for the accidents happened including average wind speed, average temperature, person killed or injured and pedestrians killed or injured-----")
f.write(df.to_html())
f.close()
