# Adjust the import statement to account for the 'processing' directory
import data_processing.extract as extractor
# from data_processing.database_handler import create_tables, bulk_insert, Rocket, Launch
import data_processing.data_transformer as transformation
import data_processing.database_handler as database



# Example usage
if __name__ == "__main__":
    database.create_tables()

    rockets = extractor.retrive_rocket_data() #Data extraction

    if rockets:
        print(f"Fetched {len(rockets)} rockets. Now doing the cleaning and transformations")
        cleaned_r_data = transformation.clean_and_transform_rocket_data(rockets)
        print(f"Cleaning completed. Now uploading the data to database")

        # database.bulk_insert(cleaned_r_data,'rockets')

    launches = extractor.retrive_launch_data() #Data extraction
    if launches:
        print(f"Fetched {len(launches)} launches. Now doing the cleaning and transformations")
        cleaned_data = transformation.clean_and_transform_launch_data(launches)
        print(f"Cleaning completed. Now uploading the data to database")

    #     database.bulk_insert(cleaned_data,'launch')
    
       
