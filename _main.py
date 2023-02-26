## Config -- Page Layout
exec(open("config.py").read())

## Gets location metadata from Google Places API
exec(open("get_details.py").read())

## Update master sheet with data based on user input
exec(open("update_sheets.py").read())

## Contains sidebar UI/UX flow
exec(open("sidebar.py").read())

## Contains map application
exec(open("folium_map.py").read())



# --------------------------------------------------------------------------------------------- # 
# This section is not wrapped in a Python File because the Emoji's will not properly show on UI #
# Experienced Section
# >> Shows parts of the dataframe filtered by experience number
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.write('### Experienced 🟥:')
    st.write(exp)
with c2:
    st.write('### Not Experienced 🟦:')
    not_experienced_df = list(df[df.experienced == 0].formatted_name)
    st.write(not_experienced_df)
with c3:
    st.write('### Newly Added 🟩:')
    newly_added_df = list(df[df.experienced == 2].formatted_name)
    st.write(newly_added_df)
with c4:
    st.write('### Sites To See 🟧:')
    to_see_df = list(df[df.experienced == 3].formatted_name)
    st.write(to_see_df)

