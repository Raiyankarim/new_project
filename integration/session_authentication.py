import requests


class SessionAuthentication(object):
    def __init__(self, configs, incident_payload):
        self.configs = configs
        self.incident_payload = incident_payload

    def basic_auth_open_inc(self):
        username = self.configs['BASIC_AUTH_USERNAME']
        password = self.configs['BASIC_AUTH_PASSWORD']
        servicenow_host = self.configs['SERVICENOW_HOST']
        response = requests.post(servicenow_host+'/api/now/table/incident', auth=(username,password), json=self.incident_payload)
        print("response.status_code", response.status_code)
        if response.status_code == 201:
            return response.json()
        else:
            return {"status": "Failed to open servicenow incident"}


    def oauth_auth_open_inc(self):
        username = self.configs['OAUTH_USERNAME']
        password = self.configs['OAUTH_PASSWORD']
        client_id = self.configs['OAUTH_CLIENT_ID']
        client_secret = self.configs['OAUTH_CLIENT_SECRET']
        grant_type = 'password'
        servicenow_host = self.configs['SERVICENOW_HOST']

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        request_data = {
           'grant_type': grant_type,
            'username': username,
            'password': password,
            'client_id': client_id,
            'client_secret': client_secret
        }
        oauth_response = requests.post(servicenow_host+'/oauth_token.do', headers=headers, data=request_data)
        if oauth_response.status_code == 200:
            oauth_response = oauth_response.json()
            if oauth_response.get('access_token', '') != '':
                access_token = oauth_response['access_token']
                headers = {'Authorization': f'Bearer {access_token}'}
                response = requests.post(servicenow_host + '/api/now/table/incident', headers=headers,
                                         json=self.incident_payload)
                if response.status_code == 201:
                    return response.json()
                else:
                    return {"status": "Failed to open servicenow incident"}
            else:
                return {"status": "Wrong oauth api response"}
        else:
            return {"status": "oauth authentication failed"}





