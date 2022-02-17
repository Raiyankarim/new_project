import json
import requests
from integration.session_authentication import SessionAuthentication
from integration.utilities import Utility


def handler(event=None, context=None):
    with open('incident_payload.json') as file_object:
        incident_payload = json.load(file_object)

    utility = Utility()
    configs = utility.configs

    ##Connect to snowflake task history table to fetch the latest failure records
    utility.connect_to_snowflake()
    for i in range(1):
        session_auth = SessionAuthentication(configs, incident_payload)
        print("AUTH TYPE = ", configs['SERVICENOW_AUTH_TYPE'])
        if configs['SERVICENOW_AUTH_TYPE'] == 'BASIC':
            response = session_auth.basic_auth_open_inc()
        elif configs['SERVICENOW_AUTH_TYPE'] == 'OAUTH':
            response = session_auth.oauth_auth_open_inc()
        else:
            return {
                'statusCode': 505,
                'body': json.dumps('Please, provide servicenow authentication type in environment variable')
            }
        if response.get('result', '') != '':
            incident_number = response.get('result').get('number')
            print("incident_number ::", incident_number)
            #Get incident details by incident number
            get_incident_details = requests.get(configs['SERVICENOW_HOST']+'/api/now/table/incident?sysparm_query=number='+incident_number,
                                                auth=(configs['BASIC_AUTH_USERNAME'], configs['BASIC_AUTH_PASSWORD']))
            #Send slack message using slack api
            # response = utility.post_slack_message(get_incident_details.json())
            # print(f"Slack Message Status:: {response.text}")
            return {
                'statusCode': 200,
                'body': json.dumps('Successfully opened incident and posted the same in slack')
            }
    return {
                'statusCode': 505,
                'body': json.dumps('Execution failed')
            }


if __name__ == "__main__":
    print(handler())
