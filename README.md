# Plants4Life project
## a SICK 2024 Hackathon project

## Project goal
To help farmers ensure that the growth for all of their crops are at a consistent rate. This is done by using an AI camera to classify the plants at certain age groups, (eg Young, Medium, Adult). Knowing this, the information of the plants and their environmental conditions will be shown on a Kibana dashboard. 

With this, farmers will be able to know which plants/crops are growing at a faster/slower rate, and can do something about it. The flow of information from the sensors and AI are all automated, as such is an automation project and keep things very simple for the farmer (but not for you ;(  ). Future improvements includes automating the rectifying part, and other things you can think of.

Process: Sensor data (light sensor, temp sensor, AI camera) --> Host (Laptop) --> Elastic Search (Log management) --> Kibana (Dashboard)

There are 3 types of files in total.
1. Scripts to automate the pulling of information from input sensors (Moisture + Temp sensor, Light sensor and SICK AI camera)
2. NOVA HTTP API library (Used to communicate with SICK AI Camera, Inspector 83x. Credits to SICK Hacker Coach for giving it to us)
3. Code that integrates everything together (we have 2, we ran 1 script on VSCode, and one on Command Prompt, due to lack of time)

## Explanation of the setup
```
 Network Connections

SICK Inspector 83X (AI camera): 192.168.0.1
SICK gateway (connecting Moisture + Temp sensor and Light sensor): 192.168.0.5
```

## Explanation of files
**import_light.py**
> Code is used to request data from the light sensor and store it in a json file named light.json
> You might want to change the json_file_path in line 19

**import_temp.py**
> Code is used to request data from the Moisture + Temp sensor and store it in a json file named temp.json
> You might want to change the json_file_path in line 19

**nova_http_api.py**
> This code is from SICK Hackathon coaches (huge thanks and credit to them)
> You can read the code if you want, but honestly, you will not be touching this file unless you are trying to add more interactions with the SICK Inspector 83X

**trigger_inference_on_camera.py**
> Code uses the NOVA HTTP API library to interact with the SICK Inspector 83X. It also merges the data from all the JSON files into 1 JSON file. Lastly, it also asks the user for an interval that the SICK Inspector 83X camera to not take photos (Eg user input is 5, the SICK Inspector 83X will take a photo every 5 seconds)
> Line 13 moisture + temp sensor data file name may be changed
> Line 14 light sensor data file name may be changed
> Line 15 final merged data file name may be changed
> Line 34 and 36 value may be changed if not using AIClassification or getting ClassName (You will understand when you use the SICK Inspector 83X UI)

**withdatetimetest2.py**
> Code pushses the final merged data file (in this scenario urdad.json) to Elastic Search
> Line 10-19 should be changed (should be understandable)
> Line 193 and 211 file directory should be changed to the desired location for light and temp sensor

