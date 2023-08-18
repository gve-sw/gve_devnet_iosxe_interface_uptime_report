from requests.auth import HTTPBasicAuth 
import requests
import sys
import urllib3
urllib3.disable_warnings()

class DNACenterAPI():

    def __init__(self, username, password, base_url):

        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password)
        self.token = self.get_dnac_jwt_token()
        self.headers = {'Content-Type': 'application/json', 'X-Auth-Token': self.token}


    def get_dnac_jwt_token(self):
        '''
        Retieve token for authentication with DNA Center. Used in concurring API calls.
        '''

        dnac_jwt_token = 0

        url = self.base_url + '/dna/system/api/v1/auth/token'
        header = {'content-type': 'application/json'}
        response = requests.post(url, auth=self.auth, headers=header, verify=False)

        if(response.status_code == requests.codes.ok):
            dnac_jwt_token = response.json()['Token']
        else:
            print("Authentication to DNAC failed. Status: ", response.status_code)
            sys.exit(1)

        print ("Connected to DNAC {0}. Status: {1}".format(self.base_url, response.status_code))
        
        return dnac_jwt_token


    def get_report_view_groups(self):
        '''
        Returns the report view groups.
        '''
        url = self.base_url + '/dna/intent/api/v1/data/view-groups'
        response = requests.get(url, headers=self.headers, verify=False)
        report_view_groups = response.json()
        return report_view_groups


    def get_report_view_ids(self, view_group_id):
        '''
        Returns the views for the groups id {view_group_id}.
        '''
        url = self.base_url + '/dna/intent/api/v1/data/view-groups/' + view_group_id
        response = requests.get(url, headers=self.headers, verify=False)
        report_view_ids = response.json()
        return report_view_ids


    def schedule_report(self, report_definition):
        '''
        Triggers the creation of a DNA Center report.
        '''
        
        url = self.base_url + "/dna/intent/api/v1/data/reports"
        payload = report_definition
        response = requests.request("POST", url, headers=self.headers, data=payload, verify=False)

        return response

    
    def get_report_executions(self, report_id):
        '''
        Get details of all executions for a given report.
        '''

        url = self.base_url + '/dna/intent/api/v1/data/reports/' + report_id + '/executions'
        response = requests.get(url, headers=self.headers, verify=False)

        return response.json()

    
    def get_report_file(self, report_id, execution_id):
        '''
        Returns report content. 
        '''

        url = self.base_url + '/dna/intent/api/v1/data/reports/' + report_id + '/executions/' + execution_id
        response = requests.get(url, headers=self.headers, verify=False)
        
        return response.text


    def delete_report(self, report_id):
        '''
        Deletes a schedule report.
        '''
        
        print('Deleting report in DNA Center after successfully retrieving the associated data...')
        
        url = self.base_url + '/dna/intent/api/v1/data/reports/' + report_id
        operation_result = requests.delete(url, headers=self.headers, verify=False)
        
        return operation_result

