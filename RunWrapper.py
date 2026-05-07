from DataWrapper import DataWrapper
import os 
import pandas as pd 

if __name__ == '__main__':
    path = '/arf/scratch/onsahin/nisar_paper/data/ismn'
    ismn_wrapper = DataWrapper(path)
    df = pd.DataFrame(index=['network','station','latitude','longitude'])
    networks = ['SCAN', 'USCRN']
    print(networks)
    c = 0 
    for network in networks:
        stations = ismn_wrapper.get_stations(network)
        for station in stations:
            print(station)
            lat,lon = (ismn_wrapper.get_coordinates(network,station)).values()
            df.loc[:,c] = [network,station,lat,lon]
            parameters = ismn_wrapper.get_station_data(network, station, daily_hourly="daily")
            print(parameters['sm_0.050800-0.050800'])
            raise ValueError
            c +=1
    df.T.to_csv('/arf/scratch/onsahin/nisar_paper/data/ismn/ismn_texas.csv')
    

