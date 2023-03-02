import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import re 
#!pip3 install gspread
#!pip3 install --upgrade google-api-python-client oauth2client
#importing the required libraries

# updates dataframe based on selected index to update
# loops through each index and populates metadata using Google Places API
def update_data(travel_df,ix_to_update=None,travel_destination=None,update_all=False):
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

# Google Sheets Endpoints and Auth
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
auth = st.secrets['internal']
creds = ServiceAccountCredentials.from_json_keyfile_dict(auth, scope)

# Authorize the clientsheet and get master sheet data
client = gspread.authorize(creds)
sheet = client.open_by_url(st.secrets['public_gsheets_url']).get_worksheet(0)
source_df = pd.DataFrame(sheet.get_all_records())

# Extra preprocessing
import re
source_df = source_df.replace(r'^\s*$', np.nan, regex=True)

# If for some reason longitudinal data is blank it will check and populate this data
# Originally the usecase was to enter the location of interest so it would populate on the map
ix_to_update = [i for i in source_df[source_df['Longitude'].isnull()].index]

# If the above is the case we get the place of interest where the data is null to populate the metadata with respect to the location
try:
    place_of_interest = list(source_df[source_df['Longitude'].isnull()]['place_of_interest'])[0]
except:
    pass

# Sometimes a new index column is created, we try to drop this column if it exists each load
try:
    source_df = source_df.drop(columns='index')
except:
    pass

# Always drop duplicates
if source_df.duplicated().any():
    source_df = source_df.mask(source_df.duplicated()).replace(np.nan,'',regex=True).sort_values('username')
    sheet.update([source_df.columns.values.tolist()] + source_df.values.tolist())
    source_df = pd.DataFrame(sheet.get_all_records())

# if there are no null values in longitudinal data we pass, otherwise we update the data
if len(ix_to_update) == 0:
    pass
else:
    update_data(source_df,ix_to_update,place_of_interest,update_all=False)
    source_df = source_df.fillna(0).drop_duplicates().sort_values('username')
    sheet.update([source_df.columns.values.tolist()] + source_df.values.tolist())

