import os
from DataHandler import DataHandler
import numpy as np


class DataWrapper:
    def __init__(self, full_path: str):
        self.full_path = full_path
        # full path to ISMN folder

    def get_networks(self) -> list:
        # It gets list of networks in the ISMN folder
        return os.listdir(self.full_path)

    def get_stations(self, network: str) -> list:
        # list of station in the given network
        return os.listdir(os.path.join(self.full_path, network))

    def get_parameters(self, network: str, station: str) -> dict[str:list]:  # variable and corresponding depths:
        # list of parameters for given network and station
        files = os.listdir(os.path.join(self.full_path, network, station))
        csv_filtered = list(filter(lambda x: "csv" not in x, files))
        variables = {}
        for file in csv_filtered:
            splits = file.split("_")
            depths = "_".join([splits[4], splits[5]])
            if splits[3] not in variables.keys():
                variables[splits[3]] = [depths]
            else:
                variables[splits[3]].append(depths)
        return variables

    def get_station_data(self, network: str, station: str, daily_hourly: str = "hourly") -> dict[str:np.ndarray]:
        handler = DataHandler(self.full_path, network, station)
        return handler.get_data(daily_hourly)

    def get_coordinates(self, network: str, station: str) -> dict[str:float, str:float]:
        handler = DataHandler(self.full_path, network, station)
        return handler.get_coordinates()
