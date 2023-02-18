#MissionWired skills test task 2
#David Lichtman
#02/18/23

import pandas as pd

path=r'C:\Users\dlich\Documents\MissionWired Skills Test\\'

#Step 1: read in csv
people=pd.read_csv(path+'people.csv', parse_dates=True)

#Step 2: update date fields to datetime
people['created_dt']=pd.to_datetime(people['created_dt'])
people['updated_dt']=pd.to_datetime(people['created_dt'])

print(people.info())

#Step 3: extract date from created datetime
people['acquisition_date']=people['created_dt'].dt.date

#Step 4: aggregate stats
acquisition_facts=people.groupby(by=['acquisition_date']).count().reset_index()
acquisition_facts['acquisitions']=acquisition_facts['email']

#Step 5: select for output csv
acquisition_facts=acquisition_facts[['acquisition_date','acquisitions']]

print(acquisition_facts)
print(acquisition_facts.info())

#Step 6: write to csv
acquisition_facts.to_csv('acquisition_facts.csv', index=False)
