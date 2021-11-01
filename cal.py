
from ics import Calendar, Event
import pandas as pd
from datetime import datetime
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

sun['emoji'] = np.where(sun['variable'] == 'Sunset', '\U0001F307', '\U0001F304'))

# reformat to 12 hour clock
sun['shorttime'] = sun['shorttime'].map(lambda a: datetime.strptime(a, "%H:%M"))
sun['shorttime'] = sun['shorttime'].map(lambda a: datetime.strftime(a, "%I:%M %p"))

sun['title'] = sun['emoji'] + " " + sun['shorttime'] + " " + sun['variable']

c = Calendar()

for i, row in sun.head(5).iterrows():
    e = Event()
    e.name = row['title']
    e.begin = row['value']
    c.events.add(e)

c.events

with open('sun.ics', 'w') as my_file:
    my_file.writelines(c)

