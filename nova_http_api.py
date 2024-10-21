
from pathlib import Path
from PIL import Image
import requests
from io import BytesIO
import base64
import numpy as np
import json
import pickle

class CrownHTTPAPI:
    def __init__(self, device_ip, target_folder=None, result_folder=None):
        self.proxies = {"http": None, "https": None}
        self.headers = {"Content-Type": "application/json"}
        self.device_ip = device_ip
        self.target_folder = target_folder
        self.result_folder = result_folder

    def upload_data(self, base64_encoded_data: str, file_name): 
        try:
            # open file
            url_open = f"http://{self.device_ip}/api/crown/File/open"
            data = {
                "data":
                    {
                        "filePath": f"{self.target_folder}/{file_name}",
                        "mode": "wb"
                        } 
                    }
            response = requests.post(url_open, json=data, headers=self.headers, proxies=self.proxies)
            resp = response.json()
            print(f"Opening file: {resp}")
            handle_id = resp['data']['handle']['id']
            
            # write file
            url_write = f"http://{self.device_ip}/api/crown/File/write"
            data = {
                "data":
                    {
                        "handle": 
                            {
                                "type": "handle",
                                "id": handle_id
                                },
                        "data":
                            {
                                "type": "binary",
                                "encoding": "base64",
                                "mimetype": "image/png",
                                "data": base64_encoded_data
                            }
                        } 
                    }
            response = requests.post(url_write, json=data, headers=self.headers, proxies=self.proxies)
            resp = response.json()
            print(f"Writing data: {resp}")
            
            # close file
            url_close = f"http://{self.device_ip}/api/crown/File/close"
            data = {
                "data":
                    {
                        "handle": 
                            {
                                "edpType": "handle",
                                "id": handle_id
                                },
                        } 
                    }
            response = requests.post(url_close, json=data, headers=self.headers, proxies=self.proxies)
            resp = response.json()
            print(f"Closing file handle: {resp}")
            
        except Exception as e:
            print(f"Error on {file_name}, skipping: {e}")

    def set_playback_in_run(self):
        url = f"http://{self.device_ip}/api/crown/NovaExecution/setPlaybackInRun"
        data = {
            "data":
                {
                    "playbackInRun": True 
                    } 
                }
        response = requests.post(url, json=data, headers=self.headers, proxies=self.proxies)
        resp = response.json()
        print(f"Set Playback in Run: {resp}")
    
    def trigger_new_image(self):
        url = f"http://{self.device_ip}/api/crown/NovaExecution/trigger"
        response = requests.post(url, headers=self.headers, proxies=self.proxies)
        resp = response.json()
        print(f"Trigger next image: {resp}")
        
    def rewind(self):
        url = f"http://{self.device_ip}/api/crown/NovaExecution/rewind"
        response = requests.post(url, headers=self.headers, proxies=self.proxies)
        resp = response.json()
        print(f"Rewind queue: {resp}")
    
    def delete_file(self, file_name):
        url = f"http://{self.device_ip}/api/crown/File/del"
        data = {
            "data":
                {
                    "fileName": f"{self.target_folder}/{file_name}",
                    } 
                }
        response = requests.post(url, json=data, headers=self.headers, proxies=self.proxies)
        resp = response.json()
        print(f"Deleting {file_name}: {resp}")
        
    def retrieve_image(self):
        # this only works if the app saves the image to device (custom app needed)
        try:
            # open file
            url_open = f"http://{self.device_ip}/api/crown/File/open"
            data = {
                "data":
                    {
                        "filePath": f"{self.result_folder}/resultImg.png",
                        "mode": "rb"
                        } 
                    }
            response = requests.post(url_open, json=data, headers=self.headers, proxies=self.proxies)
            resp = response.json()
            print(f"Opening file: {resp}")
            handle_id = resp['data']['handle']['id']
            
            # read file
            url_read = f"http://{self.device_ip}/api/crown/File/read"
            data = {
                "data":
                    {
                        "handle": 
                            {
                                "type": "handle",
                                "id": handle_id
                                },
                        } 
                    }
            response = requests.post(url_read, json=data, headers=self.headers, proxies=self.proxies)
            resp_data = response.json()
            print(f"Reading data: {resp}")
            
            # close file
            url_close = f"http://{self.device_ip}/api/crown/File/close"
            data = {
                "data":
                    {
                        "handle": 
                            {
                                "edpType": "handle",
                                "id": handle_id
                                },
                        } 
                    }
            response = requests.post(url_close, json=data, headers=self.headers, proxies=self.proxies)
            resp = response.json()
            print(f"Closing file handle: {resp}")
            return resp_data
        
        except Exception as e:
            print(f"Error on reading image, skipping: {e}")
    
    def get_result(self, result_name, url, tool_instance_index="0"):

        args = {
            "item": result_name,
            "toolIndex": tool_instance_index,
                        }
        args_stringified = json.dumps(args)
        
        data =  {   "data": {
                        "cmd": "getToolResult",
                        "arg": args_stringified
                }}
            
        response = requests.post(url, json=data, headers=self.headers, proxies=self.proxies)
        resp = response.json()
        print(f"Get Result {result_name}: {resp}")
        result_dict = json.loads(resp['data']['result'])
        result = result_dict['value']

        
        return result
    
    
   

        