# #modified_exp_df = st.experimental_data_editor(df[['formatted_name', 'experienced']])

# #st.dataframe(modified_exp_df)




# category_names = {
#     0: 'Not Experienced',
#     1: 'Experienced',
#     2: 'Newly Added',
#     3: 'Sites to See'
# }

# experienced_df = df[['formatted_name', 'experienced']]

# dummy_df = pd.get_dummies(experienced_df['experienced'], prefix='category').astype('bool')

# dummy_df.columns = dummy_df.columns.map(lambda x: category_names[int(x.split('_')[-1])])

# exp_select_boxes_df = pd.concat([experienced_df,dummy_df],axis=1).drop('experienced',axis=1)

# modified_exp_df = st.experimental_data_editor(exp_select_boxes_df)

# for i, row in modified_exp_df.iterrows():
#     num_true = row[['Not Experienced', 'Experienced', 'Newly Added', 'Sites to See']].sum()
#     if num_true > 1:
#         # raise an error with a custom message
#         st.error(f"More than one category is True in row {i+1}.")
#     else:
#         pass

# transform_back_df_1 = modified_exp_df.melt(id_vars=['formatted_name'], value_vars=list(category_names.values()))
# transform_back_df_1 = transform_back_df_1.rename(columns={'variable': 'category', 'value': 'encoded_column'})
# transform_back_df_1['encoded_column'] = transform_back_df_1['category'].map({value: key for key, value in category_names.items()})

# transform_back_df_1.rename(columns={'encoded_column':'experienced'}, inplace=True)
# transform_back_df_1.drop(columns='category',axis=1,inplace=True)

# st.dataframe(transform_back_df_1)

# st.dataframe(experienced_df)