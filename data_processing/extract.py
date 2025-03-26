import requests
import json
import time

import os
from dotenv import load_dotenv

load_dotenv()

# GraphQL endpoint
SPACEX_API_URL = os.getenv('SPACEX_API_URL')

# Function to execute GraphQL query
def fetch_graphql_data(query, variables=None, headers=None):
    payload = {
        "query": query,
        "variables": variables or {}
    }
    try:
        response = requests.post(
            SPACEX_API_URL,  
            headers=headers,
            json=payload
            )
        response.raise_for_status()  # Raise HTTPError for bad responses
        response_data = response.json()
        
        # Check for GraphQL errors in the response
        if 'errors' in response_data:
            print(f"GraphQL errors: {response_data['errors']}")
            return None
        return response.json()  # Return the data part of the response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError:
        print("Failed to decode JSON from the response.")
        return None


def fetch_batched_data_with_rate_limiting():
    
    # GraphQL query with limit and offset for batch processing
    query = """
    query($limit: Int!, $offset: Int!) {
      launches(limit: $limit, offset: $offset) {
        mission_name
        launch_date_utc
        launch_success
        launch_year
        launch_site {
        site_id
        site_name_long
        site_name
        }
        details
        rocket {
            rocket_name
            rocket_type
        }
    }
        payloads {
            id
            nationality
            payload_mass_kg
            payload_type
            manufacturer
            payload_mass_lbs
            customers
            reused
        }
    }
    """
    
    limit = 100  # Number of launches per batch
    offset = 0  # Start with the first batch of data
    all_launches = []
    
    # Rate limiting: maximum requests per minute (60 requests)
    rate_limit_per_minute = 60
    delay_between_requests = 60 / rate_limit_per_minute  # Delay in seconds (1 request per second)

    while True:
        # Set the variables for this batch
        variables = {"limit": limit, "offset": offset}
        
        # Call the fetch_graphql_data function
        data = fetch_graphql_data( query, variables)
        
        if data and 'launches' in data['data']:
            launches = data['data']['launches']
            all_launches.extend(launches)
            
            # If the number of results is less than the limit, we have reached the last page
            if len(launches) < limit:
                break

            # Update the offset to get the next batch of data
            offset += limit
        
        else:
            print("No data received or error occurred.")
            break
        
        # Sleep to respect rate limit: wait a bit before making the next request
        time.sleep(delay_between_requests)  # Delay to avoid rate-limiting

    return all_launches


