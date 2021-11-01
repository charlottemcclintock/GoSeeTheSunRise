
from ics import Calendar, Event, DisplayAlarm
import pandas as pd
from datetime import datetime, timedelta 
import numpy as np


# read in sunrise/sunset data
sunnov = pd.read_csv('sun-patterns-nov1jun1.csv')
sunjun = pd.read_csv('sun-patterns-jun2dec31.csv')

# append together
sun = sunnov.append(sunjun)

# wide to long
sun = pd.melt(sun, id_vars='date', value_vars=['sunrise', 'sunset'])

# capitalize sunrise/sunset
sun['variable'] = sun['variable'].str.title()

# slice time string to get a pretty time for event titles
sun['shorttime'] = sun['value'].str.slice(11,16)

emojis = np.where(sun['variable'] == 'Sunset', '\U0001F307', '\U0001F304')
sun['emoji'] = emojis.tolist()

# reformat to 12 hour clock
sun['shorttime'] = sun['shorttime'].map(lambda a: datetime.strptime(a, "%H:%M"))
sun['shorttime'] = sun['shorttime'].map(lambda a: datetime.strftime(a, "%I:%M %p"))

# create event title from various strings
sun['title'] = sun['emoji'] + " " + sun['shorttime'] + " " + sun['variable']


sun = sun.sort_values(by='value')

# ..............................................................................

# add here 
sunrise_phrases = []
sunset_phrases = []

# ..............................................................................

# init calendar class
c = Calendar()

# loop over dates and create calendar events, add to calendar
for i, row in sun.head(4).iterrows():
    e = Event()
    e.name = row['title']
    e.begin = row['value']
    e.alarm = [DisplayAlarm(trigger=timedelta(minutes=-5))]
    # e.description = row['desc'] # TO DO 
    c.events.add(e)

# write out as ics file
with open('sun.ics', 'w') as my_file:
    my_file.writelines(c)

