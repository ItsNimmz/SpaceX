# Adjust the import statement to account for the 'processing' directory
from data_processing.extract import fetch_batched_data_with_rate_limiting
import data_processing.data_transformer as transformation



# Example usage
if __name__ == "__main__":
    launches = fetch_batched_data_with_rate_limiting() #Data extraction

    if launches:
        print(f"Fetched {len(launches)} launches. Now doing the cleaning and transformations")
        cleaned_data = transformation.clean_and_transform_launch_data(launches)
        print(cleaned_data)
