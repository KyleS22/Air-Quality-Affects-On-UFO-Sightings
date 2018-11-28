import csv
import json
import numpy as np
from tqdm import tqdm

# Input file names
UFO_DATA_FILE = "UFOPOLLUTANTS.csv"
US_CITIES_FILE = "all_us_cities.csv"

# CSV column indices to give them all meaning
CITY_COL = 1
STATE_COL = 2
DAY_COL = 3 
MONTH_COL = 4 
YEAR_COL = 5
NO2_AQI_COL = 10
O3_AQI_COL = 14
SO2_AQI_COL = 18
CO_AQI_COL = 22
ET_COL = 23

OUTFILE = "processed_UFO_data.json"

# The output data
out_data = {}

# A place to store city locations to speed up matching cities with their coordinates
cached_city_locations = {}

def main():
    # Cache the city locations
    print("Processing City Locations:")
    with open(US_CITIES_FILE) as cities_csv:

        city_reader = csv.reader(cities_csv)
        city_lines = [line for line in cities_csv]
        city_lines = city_lines[1:]

        for city in tqdm(csv.reader(city_lines), total=len(city_lines)):
            city_name = city[1]
            lat = float(city[5])
            longitude = float(city[6])

            cached_city_locations[city_name.lower()] = {}
            cached_city_locations[city_name.lower()]["longitude"] = longitude
            cached_city_locations[city_name.lower()]["latitude"] = lat

    # Process Pollutant data
    print("\nProcessing Pollutant Data")

    with open(UFO_DATA_FILE) as ufo_csv:
        lines = [line for line in ufo_csv]
        ufo_reader = csv.reader(ufo_csv)
        lines = lines[1:]

        for row in tqdm(csv.reader(lines), total=len(lines)):
            ufo_city_name = row[CITY_COL]
            state = row[STATE_COL]
            try:
                day = int(row[DAY_COL])
                month = int(row[MONTH_COL])
                year = int(row[YEAR_COL])
                NO2 = float(row[NO2_AQI_COL])
                O3 = float(row[O3_AQI_COL])
                SO2 = float(row[SO2_AQI_COL])
                CO = float(row[CO_AQI_COL])
                ET = int(row[ET_COL])
            except:
                # If there is a problem with the data, ignore it
                continue

            # If we have the location for the city, get it, otherwise ignore it
            if ufo_city_name.lower() in cached_city_locations.keys():
                city = cached_city_locations[ufo_city_name.lower()]
                lat = city["latitude"]
                longitude = city["longitude"]
                add_city(ufo_city_name, state, day, month, year, NO2, O3, SO2, CO, ET, longitude, lat)
    
    # Get pollutant breakdowns for each city
    calculate_pollutant_breakdowns()
    calculate_sightings_by_state()
    calculcate_sightings_by_month()

    # Crap out a JSON
    with open(OUTFILE, 'w') as fp:
        json.dump(out_data, fp, sort_keys=True, indent=4)       
                        

def add_city(city, state, day, month, year, NO2, O3, SO2, CO, ET, longitude, lat):
    """
    Add a new city to the output JSON
    """
    year_month_key = str(year) + "_" + str(month)
    year_all_key = str(year) + "_all"

    if year_month_key not in out_data.keys():
        out_data[year_month_key] = {}
        out_data[year_month_key]["map_data"] = {}

    update_out_map_data(year_month_key, city, state, day, month, year, NO2, O3, SO2, CO, ET, longitude, lat)

    if year_all_key not in out_data.keys():
        out_data[year_all_key] = {}
        out_data[year_all_key]["map_data"] = {}

    if "all_all" not in out_data.keys():
        out_data["all_all"] = {}
        out_data["all_all"]["map_data"] = {}

    update_out_map_data(year_all_key, city, state, day, month, year, NO2, O3, SO2, CO, ET, longitude, lat)
    update_out_map_data("all_all", city, state, day, month, year, NO2, O3, SO2, CO, ET, longitude, lat)


def update_out_map_data(key, city, state, day, month, year, NO2, O3, SO2, CO, ET, longitude, lat):
    """
    Update the data in the output dictionary with the given data
    """
    
    map_data = out_data[key]["map_data"]

    pollutants = {}
    pollutants["day"] = day
    pollutants["month"] = month
    pollutants["year"] = year
    pollutants["NO2"] = NO2
    pollutants["O3"] = O3
    pollutants["SO2"] = SO2
    pollutants["CO"] = CO
    pollutants["ET"] = ET

    if city in map_data.keys():
        out_data[key]["map_data"][city]["num_sightings"] += ET

        out_data[key]["map_data"][city]["pollutants"].append(pollutants)
        
    else:
        out_data[key]["map_data"][city] = {}
        out_data[key]["map_data"][city]["state"] = state
        out_data[key]["map_data"][city]["num_sightings"] = ET
        out_data[key]["map_data"][city]["longitude"] = longitude
        out_data[key]["map_data"][city]["latitude"] = lat
        out_data[key]["map_data"][city]["pollutants"] = [pollutants]




def calculate_pollutant_breakdowns():
    """
    Calculate the data for a pie chart of the pollutants for each city
    """
    print("\nCalculating Pollutant Breakdowns")

    for year_month in tqdm(out_data.keys()):
        for city in out_data[year_month]["map_data"].keys():
            pollutants = out_data[year_month]["map_data"][city]["pollutants"]

            NO2_vals = []
            SO2_vals = []
            O3_vals = []
            CO_vals = []

            for pollutant_data in pollutants:
                NO2_vals.append(pollutant_data["NO2"])
                SO2_vals.append(pollutant_data["SO2"])
                O3_vals.append(pollutant_data["O3"])
                CO_vals.append(pollutant_data["CO"])

            pie_chart = {}
            pie_chart["NO2"] = np.mean(NO2_vals)
            pie_chart["SO2"] = np.mean(SO2_vals)
            pie_chart["O3"] = np.mean(O3_vals)
            pie_chart["CO"] = np.mean(CO_vals)

            out_data[year_month]["map_data"][city]["pollutant_pie"] = pie_chart

def calculate_sightings_by_state():
    print("\nCalculating Sightings By State")

    for year_month in tqdm(out_data.keys()):
        sightings_by_state = {}

        for city in out_data[year_month]["map_data"].keys():
            num_sightings = out_data[year_month]["map_data"][city]["num_sightings"]
            state = out_data[year_month]["map_data"][city]["state"]

            if state in sightings_by_state.keys():
                sightings_by_state[state] += num_sightings
            else:
                sightings_by_state[state] = num_sightings

        out_data[year_month]["sightings_by_state"] = sightings_by_state

def calculcate_sightings_by_month():
    print("\nCalculating Sightings By Month")

    for year_month in tqdm(out_data.keys()):
        if "_all" in year_month:
            sightings_by_month = {}

            for city in out_data[year_month]["map_data"].keys():
                pollutant_data = out_data[year_month]["map_data"][city]["pollutants"]

                for pollutant in pollutant_data:
                    sighting = pollutant["ET"]
                    month = pollutant["month"]

                    if month in sightings_by_month:
                        sightings_by_month[month] += sighting
                    else:
                        sightings_by_month[month] = sighting


            current_year = year_month.split("_")[0]

            for another_year_month in out_data.keys():
                if another_year_month.split("_")[0] == current_year:
                    out_data[another_year_month]["sightings_by_month"] = sightings_by_month
            

if __name__ == "__main__":
    main()
