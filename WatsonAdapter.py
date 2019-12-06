from flask import Flask, request
from adaptadores.NewRelicAdapter import NewRelicAdapter
from flask_httpauth import HTTPBasicAuth
from flask_pyoidc.flask_pyoidc import OIDCAuthentication

import requests
import os
import json

app = Flask(__name__)
auth = HTTPBasicAuth()
port = os.getenv("PORT")
vcapEnv = ''

if 'VCAP_SERVICES' in os.environ:
    vcapEnv = json.loads(os.environ['VCAP_SERVICES'])
else:
    with open('configAppId.json') as json_file:
        vcapEnv = json.load(json_file)
    
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

auth = OIDCAuthentication(app, provider_configuration_info=provider_config, client_registration_info=client_info, userinfo_endpoint_method=None)

@app.route('/chat', methods=['POST'])
#@auth.oidc_auth
@auth.login_required
def ingest():
    
    print(authenticate(username, password))
    nr = NewRelicAdapter()
    json_data = request.get_json(force=True)
    
    return nr.ingest(json_data)


@auth.verify_password
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
