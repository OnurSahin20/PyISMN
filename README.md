# PyISMN
Repo for easily utilizing meteorological data from the International Soil Moisture network which has compherensive meteorological insitu measurements (soil moisture and temperature, precipitation, air humidity etc.) all over the world. 
Clone the repo using;
```
git clone https://github.com/OnurSahin20/PyISMN.git
```
use RunWrapper.py to get data easily. You can see the networks and the stations from the different networks.

```
path = "ISMN_DataExample"
ismn_wrapper = DataWrapper(path)
networks = ismn_wrapper.get_networks() # see the all networks inside the given folder
station_uscrn = ismn_wrapper.get_stations(networks[-1]) # see the insitu stations inside one of the networks.
parameters = ismn_wrapper.get_station_data("USCRN", station_uscrn[0], daily_hourly="daily") # get all the parameters for one station from one network. It can be easily loop through for all networks and stations. 
```
Only dependent packages are numpy as pandas.
Meteorological data sets are stored in dictonary that key is "variable_depthTop,depthBottom" and values are pandas dataframes for corresponding key value.
Original temporal resolution of the ISMN is 1 hour. Repo can calculate daily mean for soil moisture and temperature and accumulation for precipitation using the parameter daily_hourly. 
Currently only the ISMN mask flag "G" is used for the quality consideration.
For daily conversion, if missing hours bigger than 8 hours that day is flagges as np.nan (It should be easily change if is necessary)
Some stations have multiple sensors for each depth. For example three sensor "A", "B", and "C" for soil moisture measurement at  5cm. Code probably overrates and gets the latest "C" sensor for depth = 5cm. 


