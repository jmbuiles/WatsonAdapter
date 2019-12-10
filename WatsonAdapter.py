from flask import Flask, request
from adaptadores.NewRelicAdapter import NewRelicAdapter
from flask_httpauth import HTTPBasicAuth
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata

import requests
import os
import json

app = Flask(__name__)
auth = HTTPBasicAuth()
port = os.getenv("PORT")
vcapEnv = ''

if 'VCAP_SERVICES' in os.environ:
    vcapEnv = json.loads(os.environ['VCAP_SERVICES'])    
    app.config.update({'SERVER_NAME': json.loads(os.environ['VCAP_APPLICATION'])['uris'][0],
                      'SECRET_KEY': 'ZDc4MzI3MzEtOTZiNi00N2VhLTk4NjgtNzVlZDA3MDc1NzM1',
                      'PREFERRED_URL_SCHEME': 'https',
                      'PERMANENT_SESSION_LIFETIME': 1800, # session time in second (30 minutes)
                      'DEBUG': False})
    
else:
    with open('/Users/jmbuiles/Desktop/WatsonWS/chatbots/configAppId.json') as json_file:
        vcapEnv = json.load(json_file)        
    app.config.update({'SERVER_NAME': '0.0.0.0:5000',
                      'SECRET_KEY': 'ZDc4MzI3MzEtOTZiNi00N2VhLTk4NjgtNzVlZDA3MDc1NzM1',
                      'PREFERRED_URL_SCHEME': 'http',
                      'PERMANENT_SESSION_LIFETIME': 2592000, # session time in seconds (30 days)
                      'DEBUG': True})   
        
    
appIDInfo = vcapEnv['AppID'][0]['credentials']

# Configure access to App ID service for the OpenID Connect client
provider_config={
     "issuer": "appid-oauth.ng.bluemix.net",
     "authorization_endpoint": appIDInfo['oauthServerUrl']+"/authorization",
     "token_endpoint": appIDInfo['oauthServerUrl']+"/token",
     "userinfo_endpoint": appIDInfo['profilesUrl']+"/api/v1/attributes",
     "jwks_uri": appIDInfo['oauthServerUrl']+"/publickeys"
}
client_info={
    "client_id": appIDInfo['clientId'],
    "client_secret": appIDInfo['secret']
}

appID_clientinfo = ClientMetadata(client_id=appIDInfo['clientId'],client_secret=appIDInfo['secret'])
appID_config = ProviderConfiguration(issuer=appIDInfo['oauthServerUrl'],client_metadata=appID_clientinfo)

auth = OIDCAuthentication({'default': appID_config}, app)
#auth = OIDCAuthentication(app, provider_configuration_info=provider_config, client_registration_info=client_info, userinfo_endpoint_method=None)

@app.route('/chat', methods=['POST'])
@auth.oidc_auth('default')
#@auth.login_required
def ingest():
    
    username = request.json.get('username')
    password = request.json.get('password')
    
    print(authenticate(username, password))
    nr = NewRelicAdapter()
    json_data = request.get_json(force=True)
    
    return nr.ingest(json_data)


#@auth.verify_password
def authenticate(username, password):
    if username and password:
        
        if username == 'jmbuiles' and password == 'jmbuiles':
            return True
        else:
            return False
    return False


if port is None:
    port = 8080
else:
    port = int(port)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
