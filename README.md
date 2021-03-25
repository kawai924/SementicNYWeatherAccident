# Generating semantic data using NY weather and accident data

>CECS 571 - Fundamentals of Semantic Web Technologies\
>Team 3: Dennis Lo, Andreas Saplacan, Mandar Vijay Kulkarni, Vatsal Patel

This project converts 2 datasets referencing New York weather and crash accident reports from plain `.csv` to the semantic standard in `.rdf`. It gives the datasets a shared meaning and relationships of weather and accident concepts and enables systems to infer knowledge.

## Project structure

    .
    ├── converter                       # Contains converter scripts for weather and accident
    ├── data                            # Hosts input and output data
    │   ├── csv                         # Input: datasets in .csv format
    │   └── rdf                         # Output: populated ontologies in .rdf format
    ├── ontology                        # Contains generated ontologies using Protege in .ttl format
    ├── venv                            # Dependencies needed to run the project
    ├── entrypoint.py                   # Main entry point of the program
    ├── NY_weather_data_extraction.py   # Script to pull and generate weather data into data/csv
    └── README.md
    
## How to convert `.csv` to meaningful `.rdf`

1) **Gather datasets:** Use API's to pull the dataset from a given web service or search and dowload a dataset from https://www.data.gov/.

2) **Design ontology:** Use [Protege](https://protege.stanford.edu/) to construct domain models and knowledge based concepts.
> Follow [this](http://mowl-power.cs.man.ac.uk/protegeowltutorial/resources/ProtegeOWLTutorialP4_v1_3.pdf) tutorial on how to use Protege for ontology design

3) **Populate ontology:** Add instances to the generated ontology using [Python](https://www.python.org/) and [RDFLib](https://github.com/RDFLib/rdflib).
> [Documentation](https://rdflib.readthedocs.io/en/stable/intro_to_creating_rdf.html) on how to create graphs and triplets using RDFLib


## Setting up and running the project
> **Disclaimer**: This project was developed and tested using MacOS.\

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

> The generated RDF files can be found under data/rdf/*.rdf

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



