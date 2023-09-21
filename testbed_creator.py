"""
Copyright (c) 2023 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""


import yaml
from dotenv import load_dotenv

load_dotenv()

class TestbedCreator():

    def __init__(self, dnac_api, testbed_filename, enable_username, enable_password):

        self.dnac_api = dnac_api
        self.testbed_filename = testbed_filename
        self.enable_username = enable_username
        self.enable_password = enable_password


    def populate_testbed_file(self):
        '''
        Retrieves all inventory devices of the type Cisco Catalyst 9500 Switch,
        Cisco Catalyst 9200L Switch or Cisco Catalyst 9300 Switch, and populates 
        the testbed file based on it.
        '''

        all_inventory_devices_list = self.get_dnac_inventory_devices()

        if self.format_testbed_info(all_inventory_devices_list, self.testbed_filename):
            print(f"Successfully created a testbed file with name: {self.testbed_filename}")
        else:
            print("Error! We could not successfully create a testbed file")


    def get_dnac_inventory_devices(self):
        '''
        Retrieves all inventory devices of the type Cisco Catalyst 9500 Switch,
        Cisco Catalyst 9200L Switch and Cisco Catalyst 9300 Switch.
        '''

        limit = 500 
        offset = 1 
        type = "Cisco Catalyst 9500 Switch&type=Cisco Catalyst 9200L Switch&type=Cisco Catalyst 9300 Switch"
        filter = f"?type={type}&offset={offset}&limit={limit}"
        all_inventory_devices_list = []
        
        inventory_devices = self.dnac_api.get_device_list(filter=filter)['response']
        all_inventory_devices_list.extend(inventory_devices)

        while len(inventory_devices) == limit:
            offset = offset + limit
            filter = f"?type={type}&offset={offset}&limit={limit}"
            inventory_devices = self.dnac_api.get_device_list(filter=filter)['response']
            all_inventory_devices_list.extend(inventory_devices)

        return all_inventory_devices_list


    def format_testbed_info(self, device_list, testbed_filename):
        '''
        Creates the content of the testbed file based on a list 
        of inventory devices.
        '''

        devices_dict = {}
        for device in device_list:
            try:
                hostname = device['hostname']
                ip = device['managementIpAddress']

                device_dict = {
                    'connections': {
                        'cli': {
                            'ip': ip,
                            'protocol': 'ssh'
                        }
                    },
                    'os': 'iosxe', 
                    'type': 'iosxe',
                    'credentials': {
                        'default': {
                            'username': self.enable_username,
                            'password': self.enable_password
                        }
                    }
                }
                devices_dict[hostname] = device_dict
            except Exception as e:
                print(e)
                print(f"Exception in parsing filtered_device_list for device {device['hostname']}")
                return False
        
        testbed_dict = {
            'devices': devices_dict
        }

        with open(testbed_filename, 'w') as testbed_file:
            yaml.dump(testbed_dict, testbed_file, default_flow_style=False)
        return True




        
        
        




