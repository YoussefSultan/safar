 # Initialize base_df which fits master data model
initialize_df = {
                'formatted_name': 0,
                'Longitude': 0,
                'Latitude': 0,
                'city': 0,
                'rating': 0,
                'notes': 0,
                'loc_of_interest': 0,
                'experienced': 0,
                'full_address': 0,
                'username': 0,
                'place_of_interest': 0
                }

# Streamlit Side Bar
with st.sidebar:
    
    # Form to submit User Data
    with st.form(key="form"):
        st.title('Create/Modify a profile with your own unique pinpoints')
        # User input data
        # >> Username, Location, Places to go
        user_input_username = st.text_input("Username","Username/Identifier")
        user_input_location = st.text_input("Location","City, State/Country")
        user_input_places = st.text_input("Places to go","Scarr's Pizza, Empire State, etc")
        # User Submit Form Button
        # >> Add to map
        add_to_map = st.form_submit_button(label='Add to map')
       
        # Initialize DataFrame based on Master Data Columns
        initialize_df = {}
        for i in source_df.columns:
            initialize_df[i] = np.nan
        base_df = pd.DataFrame(initialize_df, index=[0])
        
        # Initialize Selections of Unique Profiles in Master Data
        selections = list(source_df.username.unique())
        st.write(len(user_input_places.split(', ')))
        # Edge Case Rules to not make updates to the Master Data list if USER INPUT data is X
        if user_input_username in ['Username/Identifier','','ys-turkey','ys-canada',' '] or user_input_location in ['City, State/Country','',' '] or user_input_places in ['',' ']:
            st.error('Please enter a username and location in the above format...')
            users_place_of_interest = source_df[source_df.username == selections[0]]['place_of_interest'][0]
        elif len(user_input_places.split(', ')) > 10:
            st.error('Please reduce entries...')
        else:
            # Iterate through each place for the username and place of interest to add to the data
            for places in user_input_places.split(', '):
                # Update intialized dataframe with user input data
                initialize_df['username'] = user_input_username
                initialize_df['place_of_interest'] = user_input_location.replace(',',' ')
                initialize_df['loc_of_interest'] = places
                df_with_user_data = pd.DataFrame(initialize_df, index=[0])
                # Merge 1 record of data to empty initialized data
                base_df = pd.concat([df_with_user_data,base_df]).reset_index().drop(columns='index')
            
            # drop original NaN record used for initialization
            base_df = base_df[~base_df.loc_of_interest.isnull()] # Drop NaN

            # get the user input location from the users input data
            users_place_of_interest = ' '.join(list(base_df['place_of_interest'])[0].split('  '))

            # update the user's dataframe with longitudinal data and other missing data based on Google Places API (update_sheets.py)    
            update_data(base_df, [i for i in base_df[base_df['Longitude'].isnull()].index], travel_destination=users_place_of_interest, update_all=False)
            base_df = base_df.fillna(0)
            
            # Merge the final user dataframe with updated information to the master data and push to Google Sheets
            base_df = pd.concat([source_df.drop_duplicates(),base_df]).reset_index().drop(columns='index')
            sheet.update([base_df.columns.values.tolist()] + base_df.values.tolist())
            
        
    # Update our selections of profiles after update
    sheet = client.open_by_url(st.secrets['public_gsheets_url']).get_worksheet(0)
    source_df = pd.DataFrame(sheet.get_all_records())
    selections = list(source_df.username.unique())    
    
    # >> Click here to pick a profile    
    with st.expander("Click here to pick a profile"):
        user_selection = st.selectbox('Select a previous query', tuple(selections))
        df = source_df[source_df.username == user_selection].iloc[:,:9].reset_index()
        users_place_of_interest = list(source_df[source_df.username == user_selection]['place_of_interest'])[0]
