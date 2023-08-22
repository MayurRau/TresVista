import pandas as pd


def model():
    # Load the Excel file
    df = pd.read_excel("BIGC Model.xlsx", sheet_name="Data extraction",
                       header=[0, 1, 2, 3, 4], skiprows=[0, 3, 4],
                       skipfooter=32, index_col=[1])

    # Convert column headers to strings
    df.columns = df.columns.map(lambda x: '-'.join(map(str, x)))

    # Reset the index
    df.reset_index(inplace=True)

    # Drop unnecessary columns
    columns_to_drop = ['Unnamed: 0_level_0-Unnamed: 0_level_1-Unnamed: 0_level_2-Unnamed: 0_level_3-Unnamed: 0_level_4']
    df.drop(columns=columns_to_drop, axis=1, inplace=True)

    # Filter out unwanted columns
    excluded_columns = [i for i in df.columns if 'Q' in i or 'KPI' in i or '2024' in i]
    df1 = df.drop(columns=excluded_columns)

    # Define key_list and value_list
    key_list = [i for i in df1.columns[2:] if 'FY' in i]
    value_list = [f"{i[-3]}-{i[-2]}-{i[-1]}" for i in [i.split('-') for i in df1.columns if 'FY' in i]]

    d = {df1.columns[0]: 'Category', df1.columns[1]: df1.columns[1].split('-')[-1]}
    for i, j in zip(key_list, value_list):
        d[i] = j

    df1.rename(columns=d, inplace=True)

    # Melt the DataFrame
    melted_df = df1.melt(id_vars=['Category', 'Line Item'],
                         var_name='Estimate/Actual_Year_Period', value_name='Value')

    melted_df[['Estimate/Actual', 'Year', 'Period']] = melted_df['Estimate/Actual_Year_Period'] \
        .apply(lambda x: pd.Series(str(x).split('-')))

    melted_df.drop(columns=['Estimate/Actual_Year_Period'], inplace=True)

    # Reorder the columns
    column_order = ['Category', 'Line Item', 'Year', 'Period', 'Estimate/Actual', 'Value']
    melted_df = melted_df[column_order]

    # Define desired criteria
    desired_categories = ['Income Statement Inputs', 'Balance Sheet Inputs', 'Cash Flow Statement Inputs']
    desired_line_items = ['Revenue', 'COGS (ex D&A)', 'Cash & Short-Term Investments', 'Depreciation & Amortization',
                          'Change in Net Working Capital']
    desired_years = ['2018', '2019', '2020', '2021', '2022', '2023']
    desired_estimate_actual = ['Actual', 'Estimate']

    # Apply filters to the melted DataFrame
    filtered_df = melted_df[
        melted_df["Category"].isin(desired_categories) &
        melted_df["Line Item"].isin(desired_line_items) &
        melted_df["Year"].isin(desired_years) &
        melted_df["Estimate/Actual"].isin(desired_estimate_actual)
    ].sort_values(by=['Category', 'Line Item'], ascending=False)

    # Load additional data from Excel
    c2 = pd.read_excel("BIGC Model.xlsx", sheet_name="Data extraction", skipfooter=85, index_col=[1])
    c2.reset_index(inplace=True)
    c2.dropna(axis=1, inplace=True)

    # Create a DataFrame from selected data
    c2 = pd.DataFrame({'Author_Name': [c2['BigCommerce Holdings Inc'][1]],
                       'Ticker_Name': [c2['BigCommerce Holdings Inc'][0]]})

    # Concatenate DataFrames
    final_df = pd.concat([c2, filtered_df], axis=1)
    final_df.fillna(method='ffill', inplace=True)

    return final_df


# Call the model function
result = model()

# print(result)

# Load to excel format
output_file = "output_data.xlsx"
result.to_excel(output_file, index=False)
