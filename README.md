# Air-Quality-Impact-On-UFO-Sightings
A visualization of air quality data combined with UFO sightings in the United States.  Based on the datasets here https://www.kaggle.com/infof422henni/ufo-air-quality 

## Interactive Webpage
The current published version of the project can be accessed at https://kyles22.github.io/Air-Quality-Impact-On-UFO-Sightings/

## Devloper Information

The project is developed using the d3.js libraries for creating interactive svg data visualizations.

To run a development server, use python:

```
python -m http.server 8888

```

The open your favourite browser and go to `http://localhost:8888/air_quality_ufo_dash.html`


### Data Preprocessing
The project has a few python scripts that are used to combine the required CSV data into one JSON file to reduce the load on the client browser when
loading data.  These scripts DO NOT NEED TO BE RUN to use the visualization.  They are simply there for aggregating new data into an easy to access format.  The project can be accessed as is through a browser using the `air_quality_ufo_dash.html` file.


