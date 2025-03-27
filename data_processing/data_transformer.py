import pandas as pd
from datetime import datetime

# Function to Clean and Transform the data
def clean_and_transform_launch_data(data):

        # Convert data to DataFrame 
        df = pd.DataFrame(data)
        
        # Get basic info about the dataset
        # print('Information about the dataset\n\n', df.info())

        # Convert mission_id from list to string
        df['mission_id'] = df['mission_id'].apply(lambda x: x[0] if isinstance(x, list) else x)

        # Extract rocket_id from the dictionary in column I
        df['rocket_id'] = df['rocket'].apply(lambda x: x['rocket']['id'] if isinstance(x, dict) and 'rocket' in x and isinstance(x['rocket'], dict) else None)

        #  Convert launch_date_utc to datetime
        df['launch_date_utc'] = pd.to_datetime(df['launch_date_utc'])

        # Remove the timezone information (make datetime timezone-unaware)
        df['launch_date_utc'] = df['launch_date_utc'].dt.tz_localize(None)

        # Replace NaN values in the 'details' column with a default value, e.g., 'No details available'
        df['details'] = df['details'].fillna('No details available')

        # Drop columns where all values are NaN (empty columns)
        df = df.dropna(axis=1, how='all')

        # Drop the unwanted column
        df = df.drop(columns=['id','rocket'])

        # Drop rows with missing values in any of the specified columns
        df = df.dropna(subset=['mission_id', 'mission_name', 'rocket_id'])

        df.to_excel('cleaned_launch_data.xlsx', index=False)

        return df
        
def clean_and_transform_rocket_data(data):
        # Convert data to DataFrame 
        df = pd.DataFrame(data)
        
        df = df.rename(columns={
            'success_rate_pct': 'success_rate_percentage'
        })
        # Extract rocket_id from the dictionary in column I
        df['diameter'] = df['diameter'].apply(lambda x: x['meters'] if isinstance(x, dict) else None)   
        df['mass'] = df['mass'].apply(lambda x: x['kg'] if isinstance(x, dict) else None)     
        
        return df
        



