category_names = {
    0: 'Not Experienced',
    1: 'Experienced',
    2: 'Newly Added',
    3: 'Sites to See'
}

experienced_df = df[['formatted_name', 'experienced']]

modified_exp_df = st.experimental_data_editor(experienced_df, key='main')

for name, exp in zip(modified_exp_df.formatted_name,modified_exp_df.experienced):
    
    user_df = source_df[source_df['username'] == user_selection]
    ix = user_df[user_df.formatted_name == name].index
    ix = list(ix)[0]

    
    
    if source_df.loc[ix, 'experienced'] != modified_exp_df[modified_exp_df.formatted_name == name]['experienced'].values.tolist()[0]:
        print("FOR USERNAME:", user_selection, "| IX:", ix)
        print("CHANGING EXPERIENCE OF PLACE:", source_df.loc[ix, 'formatted_name'], source_df.loc[ix, 'experienced'], "to", modified_exp_df[modified_exp_df.formatted_name == name]['experienced'].values.tolist()[0])
        
        source_df.loc[ix, 'experienced'] = modified_exp_df[modified_exp_df.formatted_name == name]['experienced'].values.tolist()[0]

# Push updated sheet to google sheets
sheet.update([source_df.columns.values.tolist()] + source_df.values.tolist())

# re-instantiate main dataframe for map
#sheet = client.open_by_url(st.secrets['public_gsheets_url']).get_worksheet(0)
#source_df = pd.DataFrame(sheet.get_all_records())
df = source_df[source_df.username == user_selection].iloc[:,:9].reset_index()
users_place_of_interest = list(source_df[source_df.username == user_selection]['place_of_interest'])[0]
# st.dataframe(source_df)