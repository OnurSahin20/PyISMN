from DataWrapper import DataWrapper

if __name__ == '__main__':
    path = "ISMN_DataExample"
    ismn_wrapper = DataWrapper(path)
    networks = ismn_wrapper.get_networks()
    station_uscrn = ismn_wrapper.get_stations(networks[-1])
    print(station_uscrn)
    parameters = ismn_wrapper.get_station_data("USCRN", station_uscrn[0], daily_hourly="daily")
    print(parameters)
