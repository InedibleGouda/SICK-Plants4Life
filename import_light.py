import requests
import json

# Define the URL for the API endpoint
API_URL = "http://192.168.0.5/iolink/v1/devices/master1port2/processdata/value?format=iodd"

# Function to fetch data from the API and save it to a JSON file
def fetch_and_save_data():
    try:
        # Make a GET request to the API
        response = requests.get(API_URL)
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
fetch_and_save_data()