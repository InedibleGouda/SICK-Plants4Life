
from pathlib import Path
from PIL import Image
import requests
from io import BytesIO
import base64
import numpy as np
import json
import pickle
from nova_http_api import CrownHTTPAPI
import time

filename_temp = 'temp.json'
filename_light = 'light.json'
final_filename = "urdad.json"
number = 1
estimate = "NIL"
while True:
    try:
        camera_interval = int(input("Interval between images taken (in seconds): "))
        break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    device_ip = "192.168.0.1"
    api = CrownHTTPAPI(device_ip=device_ip, target_folder="/public/http_api", result_folder="/public/http_api")
    while True:
        # trigger new run
        api.trigger_new_image()
    
        # retrieve result from 
        # tool url
        url = f"http://{device_ip}/api/crown/AIClassification/ui"
        # result names can be found in en.json file (e.g. NumDetections)
        result_name = "ClassName"
        result = api.get_result(result_name, url)
        print(result)

        if (result == "young_plant"):
            estimate = "70-120 days"
        elif (result == "adult plant"):
            estimate = "15-50 days"
        elif (result == "no_plants_identified"):
            estimate = "NIL"

     
        # Storing results of in json
        json_result = {"class": result}

        # Reading data from sensors in json format
        with open(filename_temp, 'r') as file:  
            temp_data = json.load(file)
        
        with open(filename_light, 'r') as file:
            light_data = json.load(file)
        
        # Append contents of light_data to temp_data
        temp_data['light_senosrData'] = light_data

        # Write the updated data back to urmom.json
        with open(filename_temp, 'w') as file:
            json.dump(temp_data, file, indent=4)

        print("Contents of light sensor information have been appended to temp_data successfully.")

        # Read updated json file
        with open(filename_temp, 'r') as file:  
            temp_data = json.load(file)

        # Prepare the new values to be appended
        new_values = {
            "Class": {
                "value": result
            },
            "Plant_number": {
                "value": number
            },
            "Estimate date": {
                "value": estimate
            }        
        }

        # Append the new values after the "Light" section
        temp_data.update(new_values)

        # Save the updated JSON data back to the file
        with open(final_filename, 'w') as file:  
            json.dump(temp_data, file, indent=4)

        print("New values have been appended successfully.")

       
        # Duration that camera doesn't take images (set above in camera_interval)    
        time.sleep(camera_interval)
        number = number + 1
    
    
   

        