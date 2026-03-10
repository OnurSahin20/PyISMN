from DataWrapper import DataWrapper
import os 


if __name__ == '__main__':
    path = os.path.join(os.getcwd(),"ISMN_DataExample")
    ismn_wrapper = DataWrapper(path)
    networks = ismn_wrapper.get_networks()
    station_uscrn = ismn_wrapper.get_stations(networks[-1])
    parameters = ismn_wrapper.get_station_data(networks[-1], station_uscrn[0], daily_hourly="daily")
 
