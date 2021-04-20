from query.knowledge_graph import Knowledge_Graph
import pandas as pd

output_location = "./query/output/"
accidentNamespace = 'http://github.com/kawai924/SementicNYWeatherAccident/accident#'
weatherNumberNamespace = 'http://github.com/kawai924/SementicNYWeather/stationID#'

"""
Query: What is the monthly summary of accidents including injuries and weather data?
Developer: Upasana Garg
"""
def start():
    print("start getting the graphs")
    gMer = Knowledge_Graph.get_graph_instance()

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
                        ?stationID wean:hasAWND ?averageWindSpeed;
                                   wean:hasTAVG ?averageTemp.
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
        """, initNs={'act': accidentNamespace, 'wean': weatherNumberNamespace})

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
    f=open(output_location + 'Monthly_summary.html', 'w')

    # f.write("Monthly Summary for the accidents happened including average wind speed, average temperature, person killed or injured and pedestrians killed or injured-----")
    f.write(df.to_html())
    f.close()
