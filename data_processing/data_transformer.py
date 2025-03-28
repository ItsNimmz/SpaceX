import pandas as pd
from datetime import datetime

# Function to Clean and Transform the data
def clean_and_transform_data(data):

        df = pd.DataFrame(data)
        df.to_excel('metadata.xlsx', index=False)

        # Convert mission_id from list to string
        df['mission_id'] = df['mission_id'].apply(lambda x: x[0] if isinstance(x, list) else x)

        # Extract rocket_data from the dictionary in column I
        df['rocket_id'] = df['rocket'].apply(lambda x: x['rocket']['id'] if isinstance(x, dict) and 'rocket' in x and isinstance(x['rocket'], dict) else None)
        df['name'] = df['rocket'].apply(lambda x: x['rocket_name'] if isinstance(x, dict) else None)
        df['type'] = df['rocket'].apply(lambda x: x['rocket_type'] if isinstance(x, dict) else None)
        df['company'] = df['rocket'].apply(lambda x: x['rocket']['company'] if isinstance(x, dict) and 'rocket' in x and isinstance(x['rocket'], dict) else None)
        df['cost_per_launch'] = df['rocket'].apply(lambda x: x['rocket']['cost_per_launch'] if isinstance(x, dict) and 'rocket' in x and isinstance(x['rocket'], dict) else None)
        df['country'] = df['rocket'].apply(lambda x: x['rocket']['country'] if isinstance(x, dict) and 'rocket' in x and isinstance(x['rocket'], dict) else None)
        df['success_rate_pct'] = df['rocket'].apply(lambda x: x['rocket']['success_rate_pct'] if isinstance(x, dict) and 'rocket' in x and isinstance(x['rocket'], dict) else None)
        df['active'] = df['rocket'].apply(lambda x: x['rocket']['active'] if isinstance(x, dict) and 'rocket' in x and isinstance(x['rocket'], dict) else None)
        df['description'] = df['rocket'].apply(lambda x: x['rocket']['description'] if isinstance(x, dict) and 'rocket' in x and isinstance(x['rocket'], dict) else None)
        df['diameter_meters'] = df['rocket'].apply(lambda x: x['rocket']['diameter']['meters'] if isinstance(x, dict) and 'rocket' in x and isinstance(x['rocket'], dict) and 'diameter' in x['rocket'] else None)
        df['height_meters'] = df['rocket'].apply(lambda x: x['rocket']['height']['meters'] if isinstance(x, dict) and 'rocket' in x and isinstance(x['rocket'], dict) and 'height' in x['rocket'] else None)
        df['mass_kg'] = df['rocket'].apply(lambda x: x['rocket']['mass']['kg'] if isinstance(x, dict) and 'rocket' in x and isinstance(x['rocket'], dict) and 'mass' in x['rocket'] else None)

        # Extract payload weights from the nested structure
        df['payload_data'] = df['rocket'].apply(lambda x: x['rocket']['payload_weights'] if isinstance(x, dict) and 'rocket' in x and isinstance(x['rocket'], dict) else None)
    
        #  Convert launch_date_utc to datetime
        df['launch_date_utc'] = pd.to_datetime(df['launch_date_utc'])

        # Remove the timezone information (make datetime timezone-unaware)
        df['launch_date_utc'] = df['launch_date_utc'].dt.tz_localize(None)

        # Replace NaN values in the 'details' column with a default value, e.g., 'No details available'
        df['details'] = df['details'].fillna('No details available')

        # Drop columns where all values are NaN (empty columns)
        df = df.dropna(axis=1, how='all')
        df = df.drop(columns=['id', 'rocket'], errors='ignore')


        # Drop rows with missing values in any of the specified columns
        df = df.dropna(subset=['mission_id', 'mission_name', 'rocket_id'])

        df.to_excel('cleaned_launch_dataLatest.xlsx', index=False)

        return df
        
def clean_and_transform_rocket_data(data):
        
        df = pd.DataFrame(data)
        
        # Fill missing success_rate_percentage with mean
        df["success_rate_pct"] = df["success_rate_pct"].fillna(df["success_rate_pct"].mean())
        
        df = df.rename(columns={
            'success_rate_pct': 'success_rate_percentage',
            'id' : 'rocket_id'
        })
        # Extract rocket_id from the dictionary in column I
        df['diameter'] = df['diameter'].apply(lambda x: x['meters'] if isinstance(x, dict) else None)   
        df['mass'] = df['mass'].apply(lambda x: x['kg'] if isinstance(x, dict) else None)
        df['height'] = df['height'].apply(lambda x: x['meters'] if isinstance(x, dict) else None)

        
        numeric_cols = ["cost_per_launch", "diameter", "mass", "height", "success_rate_percentage"]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

        df["active"] = df["active"].astype(bool)

        df.to_excel('cleaned_rocket_data.xlsx', index=False)     
        
        return df
        



