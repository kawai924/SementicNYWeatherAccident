# Generating and querying semantic data using NY weather and accident data

>CECS 571 - Fundamentals of Semantic Web Technologies
>>**Project 2 - Generate semantic data**\
>>Team 3: Dennis Lo, Andreas Saplacan, Mandar Vijay Kulkarni, Vatsal Patel\
>>\
>>**Project 3 - Querying semantic data**\
>>Team 2: Dennis Lo, Andreas Saplacan, Upasana Garg, Aditi Tomar, Gayathri Venna

This project converts 2 datasets referencing New York weather and crash accident reports from plain `.csv` to the semantic standard in `.rdf`. It gives the datasets a shared meaning and relationships of weather and accident concepts and enables systems to infer knowledge.
The project also includes queries demonstrating the ability to answer complex questions using SPARQL as query language.

## Project structure

    .
    ├── converter                       # Contains converter scripts for weather and accident  (project 2)
    ├── data                            # Hosts input and output data  (project 2)
    │   ├── csv                         # Input: datasets in .csv format
    │   └── rdf                         # Output: populated ontologies in .rdf format (in zip file)
    ├── ontology                        # Contains generated ontologies using Protege in .ttl format  (project 2)
    ├── query                           # Contains query and graph scripts for executing SPARQL queries  (project 3)
    │   └── output                      # Output: result of SPARQL queries in HTML format  (project 3)
    ├── venv                            # Dependencies needed to run the project
    ├── entrypoint.py                   # Main entry point of the program to execute converter and queries
    ├── NY_weather_data_extraction.py   # Script to pull and generate weather data into data/csv
    └── README.md
    
## How to convert `.csv` to meaningful `.rdf`

1) **Gather datasets:** Use API's to pull the dataset from a given web service or search and download a dataset from https://www.data.gov/.

2) **Design ontology:** Use [Protege](https://protege.stanford.edu/) to construct domain models and knowledge based concepts.
> Follow [this](http://mowl-power.cs.man.ac.uk/protegeowltutorial/resources/ProtegeOWLTutorialP4_v1_3.pdf) tutorial on how to use Protege for ontology design

3) **Populate ontology:** Add instances to the generated ontology using [Python](https://www.python.org/) and [RDFLib](https://github.com/RDFLib/rdflib).
> [Documentation](https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html) on how to create graphs and triplets using RDFLib

## How to query an ontology using SPARQL and RDFLib

Use [RDFLib](https://github.com/RDFLib/rdflib) to query graph using [SPARQL](https://www.w3.org/TR/rdf-sparql-query/) syntax.
> Follow [this](https://www.oreilly.com/library/view/programming-the-semantic/9780596802141/ch04.html) tutorial on how to create simple queries


## Setting up and running the project
> **Disclaimer**: This project was developed and tested using MacOS.

> Python has to be installed on the machine (comes by default with XCode on MacOS)\
> The project comes with all dependencies needed  in the `venv.zip` 


1) Open the terminal and clone the project repository 
```
git clone https://github.com/kawai924/SementicNYWeatherAccident.git
```

2) Open the project root folder in the file browser and unzip the shipped dependency file `venv.zip`

> There are **2 ways** to run this project: Using (a) [PyCharm IDE](https://www.jetbrains.com/pycharm/) or using (b) the Terminal.

### (a) Using PyCharm:

3) Open the project in PyCharm

4) Pick your python interpreter `Python 3` in the configuration at the top right corner\
![](https://cdn.discordapp.com/attachments/807016072074887192/823710750593777694/Screen_Shot_2021-03-22_at_5.12.14_PM.png)
   
5) Press `Run` at the top right corner to start the program

### (b) Using MacOS Terminal:

3) Navigate into the root folder of the project
```
cd SementicNYWeatherAccident
```

4) Activate the Python virtual environment 
```
source venv/bin/activate
```

5) Execute the entrypoint script
```
python entrypoint.py
```

6) After the script finished, exit the virtual environment
```
deactivate
```

> The generated RDF files can be found under data/rdf/\*.rdf\
> The generated HTML files can be found under query/output/\*.html

## Queries and their developers

Following are the queries that were tested on the generated ontologies for accidents and weather in NY city and their respective developers.

Query  | Developer
------------- | -------------
What is the monthly summary of accidents including injuries and weather data? | Upasana Garg
How many accidents in Queens could have been caused by Distraction due to Thunder in 2020? | Andreas Saplacan
What are the top 5 vehicle types that were involved in the most accidents in Manhattan due to ice? | Andreas Saplacan
Which weather station is located in the county of Ontario? | Dennis Lo
Which borough in NY had the greatest number of accidents due to view obstruction in heavy fog? | Gayathri Venna /Aditi Tomar
Input query via terminal | Aditi Tomar/Gayathri Venna


## Running your own query

Input query can be used to manually query our graph by inputting a query via the terminal, similar to a search engine

Steps to run input query are as follows: 

1. Uncomment line 63 `execute_manual_query()` in entrypoint.py and comment line 61 and line 62 to run only the manual input query
2. Run entrypoint.py
3. Once the query loads all RDF and the console asks you for input, just type your query in the terminal. Once you are done, press enter one time and type ";;"
4. Press enter and query will start running
5. Keep observing the console output for runtime information
6. The results can be found in `./query/output/input_results.html`


**Prefixes for namespaces:**

Prefix | Namespace | Description 
------------- | ------------- | -------------
act | http://github.com/kawai924/SementicNYWeatherAccident/accident# | Accident data
STA | http://github.com/kawai924/SementicNYWeatherAccident/station# | Weather station ID
wea | http://github.com/kawai924/SementicNYWeatherAccident/weather# | Weather type by station and date
wean | http://github.com/kawai924/SementicNYWeather/stationID# | Weather number by station and date

## Software dependencies:
> All dependencies are included in `venv.zip`, which has to be unzipped before running the project

[Python 3](https://www.python.org/downloads/) - Python interpreter\
[Pandas](https://pandas.pydata.org/) - Tool for efficient data analysis and manipulation\
[RDFLib](https://github.com/RDFLib/rdflib) - API for creating and manipulating with RDF \
[Iribaker](https://pypi.org/project/iribaker/) - API for creating URI's easily


## Data Source:
> All datasets were found via https://www.data.gov

- https://www.ncei.noaa.gov/data/gsom/archive/ - actual weather data 
- https://www.ncdc.noaa.gov/cdo-web/datatools - Weather station info 
- https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95 - NY accident report

## Documentation:
- https://www1.ncdc.noaa.gov/pub/data/cdo/documentation/gsom-gsoy_documentation.pdf - how to read weather data set
- https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html - how to create a graph and use triples in RDFLib
- http://mowl-power.cs.man.ac.uk/protegeowltutorial/resources/ProtegeOWLTutorialP4_v1_3.pd - how to create an ontology using Protege
- https://www.oreilly.com/library/view/programming-the-semantic/9780596802141/ch04.html - how to query rdf using SPARQL and RDFLib


