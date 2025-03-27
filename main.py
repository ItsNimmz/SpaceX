# Adjust the import statement to account for the 'processing' directory
import data_processing.extract as extractor
import data_processing.data_transformer as transformation
import data_processing.database as database

def run_pipeline():
    # Create tables if they don't exist
    database.create_tables()

    # Fetch data from API
    launches = extractor.retrive_data() 
    if launches:
        print(f"Fetched {len(launches)} launches. Now doing the cleaning and transformations")
        cleaned_data = transformation.clean_and_transform_data(launches)
        print(f"Cleaning completed. Now uploading the data to database")

        # Insert cleaned data into database
        rocket_df = cleaned_data.drop_duplicates(subset=["rocket_id"])
        database.insert_to_database(rocket_df,'rockets')
        database.insert_to_database(cleaned_data,'launches')

        # Load payload data into the database
        database.load_payload(cleaned_data)

# Example usage
if __name__ == "__main__":
    run_pipeline()

        
        

    
       
