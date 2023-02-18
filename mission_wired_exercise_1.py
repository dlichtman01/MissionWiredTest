#MissionWired skills test task 1
#David Lichtman
#02/17/23

import pandas as pd

path=r'C:\Users\dlich\Documents\MissionWired Skills Test\\'

# Step 1: read in csvs
cons=pd.read_csv(path+'cons.csv')
cons_email=pd.read_csv(path+'cons_email.csv')
cons_email_chapter_subscription=pd.read_csv(path+'cons_email_chapter_subscription.csv')

df_list=[cons,cons_email,cons_email_chapter_subscription]

#basic EDA
#for df in df_list:
    #print(df.info())

#Step 2: select from dataframes to only join on needed fields

cons_select=cons[['cons_id','firstname','lastname','source','create_dt','modified_dt']]

cons_email_select=cons_email[['cons_id','cons_email_id','email','is_primary','create_dt','modified_dt']]
#filter to primary emails only
cons_email_select=cons_email_select.query('is_primary==1')

cons_email_chapter_subscription_select=cons_email_chapter_subscription[['cons_email_id','cons_email_chapter_subscription_id','chapter_id','isunsub','unsub_dt','modified_dt']]

#instructions:

#We only care about subscription statuses where chapter_id is 1.
#If an email is not present in this table
#, it is assumed to still be subscribed where chapter_id is 1.

#filter to chapter_id=1 only
cons_email_chapter_subscription_select=cons_email_chapter_subscription_select.query('chapter_id==1')
print(cons_email_chapter_subscription_select)

#Step 3: merge dataframes

cons_and_emails=cons_select.merge(cons_email_select,how='left',on='cons_id')

cons_and_emails_and_email_chapter_subscriptions=cons_and_emails.merge(cons_email_chapter_subscription_select,how='left',on='cons_email_id')
#print(cons_and_emails_and_email_chapter_subscriptions.head())

#how to know which columns to use for created_dt and updated_dt?
#each df has a create_dt and modified_dt field but they don't agree
#will use values from cons table since that is more specific to 'Person'

#Step 4: create is_unsub boolean
people=cons_and_emails_and_email_chapter_subscriptions
people['is_unsub']=people['isunsub'].apply(lambda x: True if x==1.0 else False)

#Step 5: create created_dt and updated_dt fields as datetime types

#strip day of week from datetime fields so to_datetime doesn't get confused
pattern='.*,(.*)'  #regex to return only part of field after the first comma
people['create_dt_x']=people['create_dt_x'].str.extract(pattern)
people['modified_dt_x']=people['modified_dt_x'].str.extract(pattern)

#update date fields to datetime
people['created_dt']=pd.to_datetime(people['create_dt_x'])
people['updated_dt']=pd.to_datetime(people['modified_dt_x'])

#Step 6: select columns of interest for final product
people=people[['email','source','is_unsub','created_dt','updated_dt']]
#print(people.head())
#print(people.info())

#Step 7: write to csv in working directory
people.to_csv('people.csv', index=False)
