'''
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
'''
 
import requests
import sys
import time
import json
import datetime


class DNACCollector:

    def __init__(self, dnac_api):

        self.dnac_api = dnac_api
        self.REPORT_CATEGORY = 'Network Devices'
        self.VIEW_NAME = 'VLAN'


    def get_report_view_group_id(self, report_category):
        '''
        Returns the report view group id
        '''
        view_group_id = ''
        report_view_groups = self.dnac_api.get_report_view_groups()
        for view in report_view_groups:
            if view['category'] == report_category:
                view_group_id = view['viewGroupId']
        return view_group_id


    def get_report_view_id_by_name(self, view_name, view_group_id):
        '''
        Returns the specific report id matching a name
        '''
        report_view_id = ''
        report_view_ids = self.dnac_api.get_report_view_ids(view_group_id)
        report_views = report_view_ids['views']
        for view in report_views:
            if view['viewName'] == view_name:
                report_view_id = view['viewId']
        return report_view_id
    

    def generate_VLAN_report(self, view_group_id, report_view_id):
        '''
        Defines the report definition and triggers the creation of a latest DNA Center VLAN report.
        '''

        current_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        report_definition = json.dumps({
            "name": self.REPORT_CATEGORY + "Report - " + self.VIEW_NAME +" - " + str(current_time),
            "dataCategory": self.REPORT_CATEGORY,
            "tags": [],
            "viewGroupId": view_group_id,
            "schedule": {
                "type": "SCHEDULE_NOW"
            },
            "deliveries": [
                {
                    "type": "DOWNLOAD",
                    "default": True
                }
            ],
            "view": {
                "name": self.VIEW_NAME,
                "description": "",
                "fieldGroups": [
                    {
                        "fieldGroupName": "VLAN Details",
                        "fieldGroupDisplayName": "VLAN Details",
                        "fields": [
                            {
                                "name": "ipAddress",
                                "displayName": "IP Address"
                            },
                            {
                                "name": "deviceName",
                                "displayName": "Device Name"
                            },
                            {
                                "name": "location",
                                "displayName": "Location"
                            },
                            {
                                "name": "deviceFamily",
                                "displayName": "Device Family"
                            },
                            {
                                "name": "deviceType",
                                "displayName": "Device Type"
                            },
                            {
                                "name": "vlanId",
                                "displayName": "Vlan Id"
                            },
                            {
                                "name": "vlanName",
                                "displayName": "Vlan Name"
                            },
                            {
                                "name": "interfacename",
                                "displayName": "Interface Name"
                            },
                            {
                                "name": "adminStatus",
                                "displayName": "Admin Status"
                            },
                            {
                                "name": "operStatus",
                                "displayName": "Operational Status"
                            }
                        ]
                    }
                ],
                "filters":[{
                    "type": "REGULAR",
                    "name": "Location",
                    "displayName": "Location",
                    "type": "MULTI_SELECT_TREE",
                    "scope": "",
                    "filterSpecId": "",
                    "value": []
                },
                {
                    "type": "REGULAR",
                    "name": "DeviceFamily",
                    "displayName": "Device Family",
                    "type": "MULTI_SELECT",
                    "scope": "",
                    "filterSpecId": "",
                    "value": [
                        {
                            "value": "Switches and Hubs",
                            "displayValue": "Switches and Hubs"
                        }
                    ]
                },
                {
                    "type": "REGULAR",
                    "name": "DeviceType",
                    "displayName": "Device Type",
                    "type": "MULTI_SELECT",
                    "scope": "",
                    "filterSpecId": "",
                    "value": [
                        {
                            "value": "Cisco Catalyst 9300 Switch",
                            "displayValue": "Cisco Catalyst 9300 Switch"
                        },{
                            "value": "Cisco Catalyst 9500 Switch",
                            "displayValue": "Cisco Catalyst 9500 Switch"
                        },{
                            "value": "Cisco Catalyst 9200L Switch Stack",
                            "displayValue": "Cisco Catalyst 9200L Switch Stack"
                        }
                    ]
                }],
                "format": {
                    "name": "CSV",
                    "formatType": "CSV",
                    "default": True
                },
                "viewInfo": None,
                "viewId": report_view_id
            },
            "viewGroupVersion": "2.0.0"
        })

        response = self.dnac_api.schedule_report(report_definition)

        return response


    def get_custom_VLAN_report(self):
        '''
        Triggers the creation of a latest DNA Center VLAN report, waits for the report to be 
        available and returns the report data.
        '''
        print('Retrieving view group and report view id for ' +self.REPORT_CATEGORY + ' and ' + self.VIEW_NAME + '...')

        view_group_id = self.get_report_view_group_id (report_category=self.REPORT_CATEGORY)
        report_view_id = self.get_report_view_id_by_name (view_name=self.VIEW_NAME, view_group_id=view_group_id)

        create_report_status = self.generate_VLAN_report(view_group_id, report_view_id)

        if (create_report_status.status_code == requests.codes.ok):
            
            report_id = create_report_status.json()['reportId']

            print('VLAN Report submitted with ID', report_id)
            print('Wait for report execution to start ...')

            execution_count = 0
            while execution_count == 0:
                time.sleep(1)
                print('!', end="", flush=True)
                report_details = self.dnac_api.get_report_executions(report_id)
                execution_count = report_details['executionCount']

            print('\n Report execution started, wait for process to complete ...')

            process_status = None
            while process_status != 'SUCCESS':
                time.sleep(1)
                print('!', end="", flush=True)
                report_details = self.dnac_api.get_report_executions(report_id)
                execution_info = report_details['executions'][0]
                process_status = execution_info['processStatus']

            execution_id = report_details['executions'][0]['executionId']
            print('\n Report execution completed with ID: ', execution_id)

            report_content = self.dnac_api.get_report_file(report_id, execution_id)
            print('Downloaded report content:', report_content)

            return report_content, report_id

        else:
            print('Report not submitted. Code:\t{0}tatus:\t{1} '.format(create_report_status.status_code, create_report_status.reason))
            sys.exit(1)


    def delete_report(self, report_id):
        self.dnac_api.delete_report(report_id)