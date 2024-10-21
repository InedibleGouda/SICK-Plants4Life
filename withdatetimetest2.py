import requests
import time
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ConnectionError, RequestError
import json
import os
from datetime import datetime  # Import datetime module

# Set up your Elasticsearch connection details
ES_URL = "https://f63f337b0d7f41009dd4b76df8ae6a2c.us-central1.gcp.cloud.es.io"  # Your Elasticsearch endpoint
ES_USER = "sickuser"  # username
ES_PASSWORD = "Censored!!!!"  # Pass

# Set up your REST API endpoints
API_URL_1 = "http://192.168.0.5/iolink/v1/devices/master1port1/processdata/value?format=iodd"  # Temp and Humid
API_URL_2 = "http://192.168.0.5/iolink/v1/devices/master1port2/processdata/value?format=iodd"  # Light Intensity 0-999

# JSON file path
JSON_FILE_PATH = "C:\\Users\\horat\\Downloads\\Camera\\urdad.json"  # Update with the actual path

# Create an Elasticsearch client instance
es = Elasticsearch(
    ES_URL,
    basic_auth=(ES_USER, ES_PASSWORD),
    verify_certs=True
)

# Function to fetch data from API 1
def fetch_data_from_api_1():
    try:
        response = requests.get(API_URL_1)
        response.raise_for_status()
        data = response.json()
        print(f"Data fetched from API 1: {data}")  # Print entire data for debugging
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API 1: {e}")
        return None

# Function to fetch data from API 2
def fetch_data_from_api_2():
    try:
        response = requests.get(API_URL_2)
        response.raise_for_status()
        data = response.json()
        print(f"Data fetched from API 2: {data}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API 2: {e}")
        return None

# Function to get the current timestamp
def get_current_timestamp():
    return datetime.utcnow().isoformat() + 'Z'  # Use UTC format

# Function to transform and index data for API 1 (Temp and Humidity Sensor)
def transform_and_index_data_api_1(index_name, data):
    if data is None:
        print(f"No data to index for {index_name}. Skipping...")
        return

    try:
        # Extract relevant fields
        transformed_data = []
        get_data = data.get('getData', {})

        if 'iolink' in get_data:
            iolink_data = get_data['iolink']
            print(f"Iolink data (API 1): {iolink_data}")  # Print iolink_data for debugging

            # Transform data for API 1 (Temp and Humidity Sensor)
            transformed_record = {
                "valid": iolink_data.get('valid'),
                "Switching_output_1": iolink_data['value'].get('Switching_output_1', {}).get('value'),
                "Switching_output_2": iolink_data['value'].get('Switching_output_2', {}).get('value'),
                "Temperature": iolink_data['value'].get('Temperature', {}).get('value'),
                "Measured_value": iolink_data['value'].get('Measured_value', {}).get('value'),
                "iqValue": get_data.get('iqValue'),
                "timestamp": get_current_timestamp()  # Add timestamp here
            }

            transformed_data.append(transformed_record)
            print(f"Transformed data for index '{index_name}': {transformed_data}")

        # Prepare bulk actions
        actions = [
            {
                "_index": index_name,
                "_source": item  # Ensure that 'item' is a valid JSON object
            }
            for item in transformed_data
        ]

        # Use the helpers.bulk method for bulk indexing
        response = helpers.bulk(es, actions)
        print(f"Indexed {response[0]} documents in index '{index_name}'.")

    except helpers.BulkIndexError as e:
        print(f"BulkIndexError: {e}")
        for error in e.errors:
            print(f"Error: {error}")

    except (ConnectionError, RequestError) as e:
        print(f"Error indexing data to Elasticsearch: {e}")

# Function to transform and index data for API 2 (Light Intensity Sensor)
def transform_and_index_data_api_2(index_name, data):
    if data is None:
        print(f"No data to index for {index_name}. Skipping...")
        return

    try:
        # Extract relevant fields
        transformed_data = []
        get_data = data.get('getData', {})

        if 'iolink' in get_data:
            iolink_data = get_data['iolink']
            print(f"Iolink data (API 2): {iolink_data}")  # Print iolink_data for debugging

            # Transform data for API 2 (Light Intensity Sensor)
            transformed_record = {
                "valid": iolink_data.get('valid'),
                "Light_Intensity": iolink_data['value'].get('Intensity', {}).get('value'),  # Update according to actual structure
                "iqValue": get_data.get('iqValue'),
                "Measurement_Value_of_Emission_Color": iolink_data['value'].get('Measurement_Value_of_Emission_Color', {}).get('value'),
                "timestamp": get_current_timestamp()  # Add timestamp here
            }

            transformed_data.append(transformed_record)
            print(f"Transformed data for index '{index_name}': {transformed_data}")

        # Prepare bulk actions
        actions = [
            {
                "_index": index_name,
                "_source": item  # Ensure that 'item' is a valid JSON object
            }
            for item in transformed_data
        ]

        # Use the helpers.bulk method for bulk indexing
        response = helpers.bulk(es, actions)
        print(f"Indexed {response[0]} documents in index '{index_name}'.")

    except helpers.BulkIndexError as e:
        print(f"BulkIndexError: {e}")
        for error in e.errors:
            print(f"Error: {error}")

    except (ConnectionError, RequestError) as e:
        print(f"Error indexing data to Elasticsearch: {e}")

def index_data(index_name, data):
    if data is None:
        print(f"No data to index for {index_name}. Skipping...")
        return

    try:
        # Prepare the data to include a timestamp
        data['timestamp'] = get_current_timestamp()  # Add timestamp here

        # Prepare bulk actions
        actions = [
            {
                "_index": index_name,
                "_source": data  # Directly use the data from the JSON file
            }
        ]

        # Use the helpers.bulk method for bulk indexing
        response = helpers.bulk(es, actions)
        print(f"Indexed {response[0]} documents in index '{index_name}'.")

    except helpers.BulkIndexError as e:
        print(f"BulkIndexError: {e}")
        for error in e.errors:
            print(f"Error: {error}")

    except (ConnectionError, RequestError) as e:
        print(f"Error indexing data to Elasticsearch: {e}")

def fetch_and_save_data_temp():
    # Make a GET request to the API
    response = requests.get(API_URL_1)
    response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        
    # Get the JSON data from the response
    data = response.json()
    print(f"Data fetched: {data}")  # Optional: print the fetched data for debugging

    # Define the path for the JSON file
    json_file_path = "C://Users//horat//Downloads//Camera//temp.json"
        
    # Write the JSON data to the file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)  # Use indent for pretty-printing

# Function to fetch data from the API and save it to a JSON file
def fetch_and_save_data_light():
    try:
        # Make a GET request to the API
        response = requests.get(API_URL_2)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        
        # Get the JSON data from the response
        data = response.json()
        print(f"Data fetched: {data}")  # Optional: print the fetched data for debugging

        # Define the path for the JSON file
        json_file_path = "C://Users//horat//Downloads//Camera//light.json"
        
        # Write the JSON data to the file
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)  # Use indent for pretty-printing

        print(f"Data saved to {json_file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except Exception as e:
        print(f"Error saving data to file: {e}")

# Call the function to fetch and save data
fetch_and_save_data_light()

# Main function to fetch and index data
def main():
    while True:
        # Fetch data from both APIs
        data_from_api_1 = fetch_data_from_api_1()
        data_from_api_2 = fetch_data_from_api_2()

        # Index the data into separate Elasticsearch indices
        # transform_and_index_data_api_1("api_data_source_1", data_from_api_1)  # Index name for Temp Humidity Sensor
        # transform_and_index_data_api_2("api_data_source_2", data_from_api_2)  # Index name for Light Sensor

        fetch_and_save_data_temp()
        fetch_and_save_data_light()
        # Read data from the JSON file and index it
        try:
            with open(JSON_FILE_PATH, 'r') as json_file:
                json_data = json.load(json_file)
                print(f"Data read from JSON file: {json_data}")  # Debugging output
                index_data("complete_data", json_data)  # Index the JSON data
        except Exception as e:
            print(f"Error reading JSON file: {e}")

        # Wait for a specified interval (e.g., 60 seconds)
        time.sleep(2)  # Adjust the interval as needed

if __name__ == "__main__":
    main()
