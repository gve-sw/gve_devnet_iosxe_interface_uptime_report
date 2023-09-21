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

import os
from dotenv import load_dotenv
from device_collector import DeviceCollector
from dnac_collector import DNACCollector
from custom_report import CustomReport
from dnac_api import DNACenterAPI
from testbed_creator import TestbedCreator

load_dotenv()

if __name__ == "__main__":

    testbed_filename = "testbed.yaml"
    command = "show interfaces link"
    dnac_username = os.getenv('DNAC_USERNAME')
    dnac_password = os.getenv('DNAC_PASSWORD')
    dnac_base_url = os.getenv('DNAC_BASE_URL')
    enable_username = os.getenv('ENABLE_USERNAME')
    enable_password = os.getenv('ENABLE_PASSWORD')
    
    dnac_api = DNACenterAPI(dnac_username, dnac_password, dnac_base_url)

    testbed_creator = TestbedCreator(dnac_api, testbed_filename, enable_username, enable_password)
    testbed_creator.populate_testbed_file()

    device_collector = DeviceCollector(testbed_filename, command)
    collected_device_data = device_collector.parse_all_devices()

    dnac_collector = DNACCollector(dnac_api)
    collected_dnac_data, report_id = dnac_collector.get_custom_VLAN_report()
 
    custom_report = CustomReport()
    custom_report = custom_report.create_custom_report(collected_device_data, collected_dnac_data)

    dnac_collector.delete_report(report_id)
        



    