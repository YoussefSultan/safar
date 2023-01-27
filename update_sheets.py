import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import re 
#!pip3 install gspread
#!pip3 install --upgrade google-api-python-client oauth2client
#importing the required libraries
place_of_interest = 'Philadelphia PA'
def update_data(travel_df,ix_to_update=None,travel_destination=place_of_interest,update_all=False):
   #for i in range(len(travel_df.loc_of_interest))
    if update_all:
        to_update = range(len(travel_df.loc_of_interest))
    else:
        to_update = ix_to_update
    for i in to_update:
        location_to_search = travel_df.iloc[i]['loc_of_interest']
        search_results = get_details(location_to_search,travel_destination)
        travel_df.loc[i, 'Latitude'] = search_results[3]
        travel_df.loc[i, 'Longitude'] = search_results[2]
        travel_df.loc[i, 'city'] = search_results[1].split(',')[1].split()[0]
        travel_df.loc[i, 'full_address'] = search_results[1]
        travel_df.loc[i, 'formatted_name'] = search_results[4]
        travel_df.loc[i, 'rating'] = search_results[5]
        print("Updated",search_results[4])

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

auth = st.secrets['internal']
creds = ServiceAccountCredentials.from_json_keyfile_dict(auth, scope)

# authorize the clientsheet 
client = gspread.authorize(creds)
sheet = client.open_by_url(st.secrets['public_gsheets_url']).get_worksheet(0)
source_df = pd.DataFrame(sheet.get_all_records())
import re
source_df = source_df.replace(r'^\s*$', np.nan, regex=True)
ix_to_update = [i for i in source_df[source_df['Longitude'].isnull()].index]

try:
    source_df = source_df.drop(columns='index')
except:
    pass

if len(ix_to_update) == 0:
    pass
else:
    update_data(source_df,ix_to_update,update_all=False)
    source_df = source_df.fillna(0)
    sheet.update([source_df.columns.values.tolist()] + source_df.values.tolist())

