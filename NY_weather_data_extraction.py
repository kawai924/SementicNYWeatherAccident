import pandas as pd


def NYdata():
    # with open('data/NY_stations_id.txt', 'r') as f:
    #     data = f.read()
    df = pd.read_csv('data/csv/NY_stations_id.txt')
    # print(df)
    listdf = list(df.GHCND)

    data2017 = pd.read_csv('/Users/dennislo/Downloads/2017.csv', header=None)
    data2017[8] = data2017[0]
    data2017 = data2017.set_index([0])
    filter2017 =data2017.loc[data2017.index.isin(listdf)]

    data2018 = pd.read_csv('/Users/dennislo/Downloads/2018.csv', header=None)
    data2018[8] = data2018[0]
    data2018 = data2018.set_index([0])
    filter2018 = data2018.loc[data2018.index.isin(listdf)]

    data2019 = pd.read_csv('/Users/dennislo/Downloads/2019.csv', header=None)
    data2019[8] = data2019[0]
    data2019 = data2019.set_index([0])
    filter2019 = data2019.loc[data2019.index.isin(listdf)]

    data2020 = pd.read_csv('/Users/dennislo/Downloads/2020.csv', header=None)
    data2020[8] = data2020[0]
    data2020 = data2020.set_index([0])
    filter2020 = data2020.loc[data2020.index.isin(listdf)]

    NYalldata = pd.concat([filter2017, filter2018, filter2019, filter2020], ignore_index=True)

    NYalldata.columns = ["date", "datatype", "value", "4", "5","6","7","station_id"]

    # print(NYalldata)
    # filter out the certain type
    targetlist = ['TAVG','TMIN','TMAX','AWND', 'WESF']
    final = NYalldata[NYalldata["datatype"].isin(targetlist)]

    WTlist = ['WT01','WT02','WT03','WT04','WT05','WT06','WT07','WT08','WT09','WT10','WT11','WT12','WT13','WT14','WT15',
              'WT16', 'WT17', 'WT18', 'WT19', 'WT21', 'WT22'  ]
    WTdata = NYalldata[NYalldata["datatype"].isin(WTlist)]
    # print(NYalldata[NYalldata[2].isin(targetlist)])

    final.to_csv('data/NY_data.csv', index = False)
    WTdata.to_csv('data/NY_weather_type.csv', index = False)