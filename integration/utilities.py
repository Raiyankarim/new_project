from dotenv import load_dotenv #python-dotenv external package
import os
import requests
import snowflake.connector
# import pandas as pd

class Utility(object):
    def __init__(self):
        self.configs = Utility.read_configs()

    @staticmethod
    def read_configs(configs={}):
        load_dotenv()
        configs['SERVICENOW_HOST'] = os.getenv('SERVICENOW.HOST')
        configs['BASIC_AUTH_USERNAME'] = os.getenv('BASIC_AUTH.USERNAME')
        configs['BASIC_AUTH_PASSWORD'] = os.getenv('BASIC_AUTH.PASSWORD')
        configs['OAUTH_USERNAME'] = os.getenv('OAUTH.USERNAME')
        configs['OAUTH_PASSWORD'] = os.getenv('OAUTH.PASSWORD')
        configs['OAUTH_CLIENT_ID'] = os.getenv('OAUTH.CLIENT_ID')
        configs['OAUTH_CLIENT_SECRET'] = os.getenv('OAUTH.CLIENT_SECRET')
        configs['SERVICENOW_AUTH_TYPE'] = os.getenv('SERVICENOW.AUTH_TYPE')
        configs['SLACK_WEBHOOK_URL'] = os.getenv('SLACK.WEBHOOK_URL')
        configs['SNOWFLAKE_USERNAME'] = os.getenv('SNOWFLAKE_USERNAME')
        configs['SNOWFLAKE_PASSWORD'] = os.getenv('SNOWFLAKE_PASSWORD')
        configs['SNOWFLAKE_ACCOUNT'] = os.getenv('SNOWFLAKE_ACCOUNT')
        return configs

    def post_slack_message(self, get_incident_details):
        slack_webhook_url = self.configs['SLACK_WEBHOOK_URL']
        incident_number = get_incident_details['result'][0].get('number')
        short_description = get_incident_details['result'][0].get('short_description')
        opened_at = get_incident_details['result'][0].get('opened_at')
        message = {
            'text': f"*Incident::* {incident_number}\n*Short Description::* {short_description}\n*Opened At::* {opened_at} UTC"}
        response = requests.post(slack_webhook_url, json=message)
        return response

    def connect_to_snowflake(self):
        conn = snowflake.connector.connect(
            user=self.configs['SNOWFLAKE_USERNAME'],
            password=self.configs['SNOWFLAKE_PASSWORD'],
            account=self.configs['SNOWFLAKE_ACCOUNT']
            # authenticator="" + keyring.get_password("test", "authenticator") + "",
            # warehouse="" + keyring.get_password("test", "warehouse_DSE_QUERY_LST_WH") + "",
            # database="" + keyring.get_password("test", "database_DSE_QUERY_LST_WH") + "",
            # schema="" + keyring.get_password("test", "ACCOUNT_USAGE_DSE_QUERY_LST_WH") + ""
        )
        cur = conn.cursor()
        sql = """Select *     
        from "SNOWFLAKE"."ACCOUNT_USAGE"."TASK_HISTORY" 
        where date(SCHEDULED_TIME) >= Current_Date() 
        --and STATE in ('FAILED', 'SKIPPED')
        and STATE in ('FAILED')"""
        sql = 'select current_version()'
        cur.execute(sql)
        row = cur.fetchone()
        print(row[0])
        # col_names = []
        # for elt in cur.description:
        #     col_names.append(elt[0])
        # df = pd.DataFrame(cur.fetchall(), columns=col_names)
        # df.head()
        cur.close()
        conn.close()