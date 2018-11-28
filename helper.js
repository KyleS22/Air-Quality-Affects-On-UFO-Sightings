function getPollutants(data, city, year, month)
{
    toRet = {"CO": 0, "NO2": 0, "O3": 0, "SO2": 0, "count": 0}
    if(year == "any")
    {
        for (i = 2000; i < 2009; i++)
        {
            year_data = getPollutants(data, city, i, month)
            toRet["CO"] += year_data["CO"] * year_data["count"]
            toRet["NO2"] += year_data["NO2"] * year_data["count"]
            toRet["O3"] += year_data["O3"] * year_data["count"]
            toRet["SO2"] += year_data["SO2"] * year_data["count"]
            toRet["count"] += year_data["count"]
        }
        toRet["CO"] = toRet["CO"] / toRet["count"]
        toRet["NO2"] = toRet["NO2"] / toRet["count"]
        toRet["O3"] = toRet["O3"] / toRet["count"]
        toRet["SO2"] = toRet["SO2"] / toRet["count"]
        return toRet
    }
    else if(month == "any"){
        toRet["count"] = 0
        for (i = 1; i < 13; i++)
        {
            if (year + "_" + i in Object.keys(data))
            {
                
                for (p in data[year + "_" + i]["map_data"][city]["pollutants"])
                {
                    toRet["CO"] += p["CO"]
                    toRet["NO2"] += p["NO2"]
                    toRet["O3"] += p["O3"]
                    toRet["SO2"] += p["SO2"]
                    toRet["count"] += 1
                }
            }
        }
        toRet["CO"] = toRet["CO"] / toRet["count"]
        toRet["NO2"] = toRet["NO2"] / toRet["count"]
        toRet["O3"] = toRet["O3"] / toRet["count"]
        toRet["SO2"] = toRet["SO2"] / toRet["count"]
        return toRet
    }
    else{
        for (p in data[year + "_" + month]["map_data"][city]["pollutants"])
        {
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