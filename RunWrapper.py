from DataWrapper import DataWrapper

if __name__ == '__main__':
    path = "ISMN_DataExample"
    ismn_wrapper = DataWrapper(path)
    scan_stations = ismn_wrapper.get_stations("SCAN")
    parameters = ismn_wrapper.get_station_data("SCAN", scan_stations[0], daily_hourly="daily")
    print(ismn_wrapper.get_coordinates("SCAN", scan_stations[0]))
