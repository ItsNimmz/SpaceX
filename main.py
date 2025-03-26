# Adjust the import statement to account for the 'processing' directory
from data_processing.extract import fetch_batched_data_with_rate_limiting



# Example usage
if __name__ == "__main__":
    launches = fetch_batched_data_with_rate_limiting()

    if launches:
        print(f"Fetched {len(launches)} launches.")
