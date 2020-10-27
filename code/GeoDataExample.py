# this file is an example to how we extracted the school's locations

import pandas as pd
from geopy.geocoders import Nominatim

data2 = [
        {'Id':'01', 'Address': "אידר 23, חיפה, ישראל", 'Latitude': None, 'Longitude' :None},
        {'Id':'02', 'Address': "מקיף י',אשדוד, ישראל", 'Latitude': None, 'Longitude' :None}]

# ====================================================================================
# ------------------------- getting institutions coord -------------------------------
# ====================================================================================
geolocator = Nominatim(user_agent="http")
df = pd.DataFrame(data2)

# merge city and institution name into one col name 'Address' in this format: instName, city, israel
# MISSING
# create col 'AddessAsUni' - convert each address to unicode:
df['AddressAsUni']  = df['Address'].apply(lambda x: x.encode(encoding='UTF-8',errors='strict'))
# find coordinates
df['city_coord']  = df['AddressAsUni'].apply(geolocator.geocode)
# sort to lati/long
df['Latitude'] = df['city_coord'].apply(lambda x: (x.latitude))
df['Longitude'] = df['city_coord'].apply(lambda x: (x.longitude))
print(df[['Address' , 'Latitude','Longitude']])

