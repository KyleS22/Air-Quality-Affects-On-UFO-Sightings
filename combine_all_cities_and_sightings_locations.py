import csv

US_CITIES_FILE = "all_us_cities.csv"
cached_city_locations = {}

print("Processing City Locations:")
    with open(US_CITIES_FILE) as cities_csv:

        city_reader = csv.reader(cities_csv)
        city_lines = [line for line in cities_csv]
        city_lines = city_lines[1:]

        for city in tqdm(csv.reader(city_lines), total=len(city_lines)):
            city_name = city[1]
            lat = float(city[5])
            longitude = float(city[6])
            state = city[3]

            new_key = city_name.lower() + "_" + state.lower()

            cached_city_locations[new_key] = {}
            cached_city_locations[new_key]["longitude"] = longitude
            cached_city_locations[new_key]["latitude"] = lat


print("Processing City Locations:")
    with open(SIGHTINGS_FILE) as cities_csv:

        city_reader = csv.reader(cities_csv)
        city_lines = [line for line in cities_csv]
        city_lines = city_lines[1:]

        for city in tqdm(csv.reader(city_lines), total=len(city_lines)):
            city_name = city[1]
            lat = float(city[9])
            longitude = float(city[10])
            state = city[2]

            new_key = city_name.lower() + "_" + state.lower()

            if not new_key in cached_city_locations:
                with open('document.csv','a') as fd:
                    fd.write("us",city_name,city_name,state,0,lat,longitude)