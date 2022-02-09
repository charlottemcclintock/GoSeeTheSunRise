
import requests
import pandas as pd
import datetime 
import time 
# define api url, lat, long
api_url = 'https://api.sunrise-sunset.org/json?lat={}&lng={}&date={}'
lat = 38.9072 # 38.9072
long = -77.0369 # -77.0369


# set times to iterate over 
start_date = datetime.date(2022, 2, 9)
end_date = datetime.date(2022, 12, 31)
delta = datetime.timedelta(days=1)

times = []

# loop to hit API for lots of dates
while start_date <= end_date:

    response = requests.get(api_url.format(lat, long, start_date))
    data = response.json()
    times.append([start_date, [data['results'].get(key) for key in ['sunrise', 'sunset']]])
    start_date += delta

# results to dataframe
df = pd.DataFrame(times, columns = ['date', 'risesetpair'])

# unlist 
df[['sunrise','sunset']] = pd.DataFrame(df['risesetpair'].tolist(), index= df.index)

# drop pair
df.drop(columns =["risesetpair"], inplace = True)

df.to_csv("sun-patterns-febdec-dc.csv")


sun = pd.read_csv('sun-patterns-febdec-dc.csv') # read from csv to avoid rehitting API

# add date to times
sun['sunrise'] =  sun['date'] + ' ' + sun['sunrise']
sun['sunset'] =  sun['date'] + ' ' + sun['sunset']

# to datetime
sun['sunrise'] =  pd.to_datetime(sun['sunrise'])
sun['sunset'] =  pd.to_datetime(sun['sunset'])

# convert to EST
sun['sunrise'] = sun['sunrise'].apply(lambda x: x.tz_localize('UTC').tz_convert('US/Eastern')) # US/Eastern
sun['sunset'] = sun['sunset'].apply(lambda x: x.tz_localize('UTC').tz_convert('US/Eastern')) # US/Eastern

# write back to csv
sun.to_csv("sun-patterns-febdec-dc.csv")

