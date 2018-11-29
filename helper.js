function getPollutants(data, city, year="any", month="any")
{
    /**
     * Search the data for the average AQI for each pollutant type
     * over the specified time interval.
     */
    toRet = {"CO": 0, "NO2": 0, "O3": 0, "SO2": 0, "count": 0}
    if(year == "any")
    {
        toRetY = {"CO": 0, "NO2": 0, "O3": 0, "SO2": 0, "count": 0}
        for (j = 2000; j < 2009; j++)
        {
            year_data = getPollutants(data, city, j, month)
            toRetY["CO"] += year_data["CO"] * year_data["count"]
            toRetY["NO2"] += year_data["NO2"] * year_data["count"]
            toRetY["O3"] += year_data["O3"] * year_data["count"]
            toRetY["SO2"] += year_data["SO2"] * year_data["count"]
            toRetY["count"] += year_data["count"]
        }
        if (toRetY["count"] != 0)
        {
            toRetY["CO"] = toRetY["CO"] / toRetY["count"]
            toRetY["NO2"] = toRetY["NO2"] / toRetY["count"]
            toRetY["O3"] = toRetY["O3"] / toRetY["count"]
            toRetY["SO2"] = toRetY["SO2"] / toRetY["count"]
        }
        return toRetY
    }
    else if(month == "any"){
        toRet["count"] = 0
        for (i = 1; i < 13; i++)
        {
            if (data[year + "_" + i] != undefined && data[year + "_" + i]["map_data"][city] != undefined)
            {
                for (x in data[year + "_" + i]["map_data"][city]["pollutants"])
                {
                    p = data[year + "_" + i]["map_data"][city]["pollutants"][x]
                    toRet["CO"] += p["CO"]
                    toRet["NO2"] += p["NO2"]
                    toRet["O3"] += p["O3"]
                    toRet["SO2"] += p["SO2"]
                    toRet["count"] += 1
                }
            }
        }
        if (toRet["count"] != 0)
        {
            toRet["CO"] = toRet["CO"] / toRet["count"]
            toRet["NO2"] = toRet["NO2"] / toRet["count"]
            toRet["O3"] = toRet["O3"] / toRet["count"]
            toRet["SO2"] = toRet["SO2"] / toRet["count"]
        }
        return toRet
    }
    else{
        if (data[year + "_" + month] == undefined || data[year + "_" + month]["map_data"][city] == undefined)
        {
            return toRet
        }
        for (x in data[year + "_" + month]["map_data"][city]["pollutants"])
        {
            p = data[year + "_" + month]["map_data"][city]["pollutants"][x]
            toRet["CO"] += p["CO"]
            toRet["NO2"] += p["NO2"]
            toRet["O3"] += p["O3"]
            toRet["SO2"] += p["SO2"]
            toRet["count"] += 1
        }
        toRet["CO"] = toRet["CO"] / toRet["count"]
        toRet["NO2"] = toRet["NO2"] / toRet["count"]
        toRet["O3"] = toRet["O3"] / toRet["count"]
        toRet["SO2"] = toRet["SO2"] / toRet["count"]
        
        return toRet
    }
}

function getUFO(data, city, year="any", month="any")
{
    /**
     * Find each UFO sighting for the specified city over the
     * specified time interval
     */
    toRet = []
    if(year == "any")
    {
        toRetY = []
        for (j = 2000; j < 2009; j++)
        {
            toRetY.concat(getUFO(data, city, j, month))
        }
        return toRetY
    }
    else if(month == "any"){
        for (i = 1; i < 13; i++)
        {
            if (data[year + "_" + i] != undefined && data[year + "_" + i]["map_data"][city] != undefined)
            {
                for (x in data[year + "_" + i]["map_data"][city]["pollutants"])
                {
                    p = data[year + "_" + i]["map_data"][city]["pollutants"][x]
                    if(p.ET == 1)
                    {
                        toRet.push({"year": p.year, "month": p.month, "day": p.day})
                    }
                }
            }
        }
        return toRet
    }
    else{
        if (data[year + "_" + month] == undefined || data[year + "_" + month]["map_data"][city] == undefined)
        {
            return toRet
        }
        for (x in data[year + "_" + month]["map_data"][city]["pollutants"])
        {
            p = data[year + "_" + month]["map_data"][city]["pollutants"][x]
            if(p.ET == 1)
            {
                toRet.push({"year": p.year, "month": p.month, "day": p.day})
            }
        }
        return toRet
    }
}