# SementicNYWeatherAccident

Project is for CECS 571\
by Dennis Lo, Andreas Saplacan,\
Mandar Vijay Kulkarni, Vatsal Patel

---
###Running the project
1) Clone the repository:
```
git clone https://github.com/kawai924/SementicNYWeatherAccident.git
```


2) Open the project in the file browser and unzip the ```venv.zip``` file

3) Open the project in PyCharm 
4) Pick your python interpreter `Python 3` in configuration
   
5) press `Run`
---
###Software requirement (used):
Python 3 (3.9)\
pandas\
rdflib\
iribaker\
enum

---

###Data Source:
https://www.ncei.noaa.gov/data/gsom/archive/ (actual weather data)\
https://www.ncdc.noaa.gov/cdo-web/datatools (Weather station info)\
https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95 (NY accident report)
###Documentation:
https://www1.ncdc.noaa.gov/pub/data/cdo/documentation/gsom-gsoy_documentation.pdf (weather data set)

---
###Instruction
put formatted file under /data/csv\
Ontology is under /ontology\
run entrypoint.py\
output RDF in /data/rdf
