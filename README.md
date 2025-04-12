# PyISMN
Repo for getting easily the meteorological data from the International Soil Moisture network which has compherensive meteorological insitu measurements all over the world. 
Clone the repo using;
```
git clone https://github.com/OnurSahin20/PyISMN.git
```
use RunWrapper.py to get data easily. You can see the networks and the stations from the different networks.

```
path = "ISMN_DataExample"
ismn_wrapper = DataWrapper(path)
networks = ismn_wrapper.get_networks() # see the all networks inside the given folder
station_uscrn = ismn_wrapper.get_stations(networks[-1]) # see the insitu stations inside one of the network inside networks.
parameters = ismn_wrapper.get_station_data("USCRN", station_uscrn[0], daily_hourly="daily") # get all the parameters for one station from one network. It can be easily loop through for all networks and stations. 
```
