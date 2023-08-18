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

import pandas
from io import StringIO
import re

class CustomReport():
    
    def __init__(self):
        self.down_times = []
        self.up_times = []


    def create_custom_report(self, collected_device_data, collected_dnac_data):
        '''
        Appends the uptime and down time retrieved from the device directly to the DNAC VLAN report.
        '''

        print("Creating custom report ...")

        columns = 'IP Address,Device Name,Location,Device Family,Device Type,Vlan Id,Vlan Name,Interface Name,Admin Status,Operational Status'
        dnac_vlan_data_rows = collected_dnac_data.split(columns)[1]
        
        csvStringIO = StringIO(dnac_vlan_data_rows)
        csv_data = pandas.read_csv(csvStringIO, sep=",", header=None, names=columns.split(','))
        
        self.initialize_device_time_lists(csv_data)

        for index in range(len(csv_data)):

            ip_address = csv_data.loc[index, 'IP Address']
            interface_name = csv_data.loc[index,'Interface Name']
            interface_abbr = interface_name[:2] + re.findall(r"\d+(?:/\d+)+", interface_name)[0]

            self.update_device_time_list_entries(collected_device_data, ip_address, interface_name, interface_abbr, index)
        
        csv_data['Uptime'] = self.up_times
        csv_data['Down Time'] = self.down_times
        
        data_frame = pandas.DataFrame(data=csv_data)
        data_frame.to_csv("vlan_report.csv", sep=";", header=True, index=False)

        print("Custom report with the name *vlan_report.csv* created. Check the local demo app folder.")


    def initialize_device_time_lists(self, csv_data):
        '''
        Separate lists to store down_times and up_times of data retrieved from the device directly.
        Each index corresponds with the associated line for the same IP and interface in the DNAC VLAN report.
        '''
        self.down_times = [''] * len(csv_data)
        self.up_times =  [''] * len(csv_data)


    def update_device_time_list_entries(self, collected_device_data, ip_address, interface_name, interface_abbr, index):
        '''
        Takes one line of the DNAC report and checks in the device data offers down time and uptime values for the associated 
        device IP and interface in that line. If data is available it updates the uptime and down time lists at 
        the specific, provided index.
        '''
        
        for device in collected_device_data:
                if ip_address in device:
                    interfaces = device[ip_address]['interfaces']
                    down_time, up_time = self.get_time_or_None(interfaces, interface_name, interface_abbr) 
                    if down_time != None:
                        self.down_times[index] = down_time
                    if up_time != None:
                        self.up_times[index] = up_time


    def get_time_or_None(self, device_interfaces, interface_name, interface_abbr):
        '''
        Takes interfaces dictionary (which is part of the data retrieved from the device directly) 
        and returns the uptime and down time values for a specific interface. 
        '''
        down_time = None
        up_time = None

        for interface in device_interfaces:
            if interface_name == interface or interface == interface_abbr:

                if 'up_time' in device_interfaces[interface]:
                    up_time = device_interfaces[interface]['up_time']
                if 'down_time' in device_interfaces[interface]:
                    down_time = device_interfaces[interface]['down_time']
                break

        return down_time, up_time
  
            
                  
