from flask import Flask, request
from flask_classful import FlaskView, route

import requests
import json

class NewRelicAdapter(FlaskView):
    
    route_base = '/'

    @route('/chat', methods=['POST'])
    def ingest(self):
        json_data = request.get_json(force=True)
        custom_json = ""
        
        METRICA = json_data.get('METRICA')
        HOST = json_data.get('HOST')
        OPERACION = json_data.get('OPERACION')
        
        url = "https://api.newrelic.com/graphql"
        
        headers = {
            'Content-Type': "application/json",
            'API-Key': "NRAK-T0S50S2RPT5BAQPASPFCOK8KYBT",
            'Host': "api.newrelic.com",
        }
        
        if (OPERACION == 'CALCULAR_VALOR'):
            
            payload = "{\"query\":\"{  actor {    account(id: 1666361) { nrql(query: \\\"SELECT latest(" + METRICA + ") FROM SystemSample WHERE displayName = \\u0027" + HOST + "\\u0027\\\") {        results      }    }  }}\", \"variables\":\"\"}"
            response = requests.request("POST", url, data=payload, headers=headers)
            
            print("########################################################################")
            print(response.json())
            print("########################################################################")
            print(response.json().get("data").get("actor").get("account").get("nrql").get("results")[0])
            
            valorTmp = response.json().get("data").get("actor").get("account").get("nrql").get("results")[0]
    
            custom_json = '{"resultado":"' + str(valorTmp.get("latest." + METRICA)) + '"}'
            parsed_json = json.dumps(custom_json)
            
        if (OPERACION == 'GRAFICAR'):
            
            payload = "{\"query\":\"{  actor {    account(id: 1666361) { nrql(query: \\\"SELECT count(" + METRICA + ") FROM SystemSample FACET " + METRICA + " SINCE 30 MINUTES AGO WHERE displayName = \\u0027" + HOST + "\\u0027 TIMESERIES\\\") {        embeddedChartUrl      }    }  }}\", \"variables\":\"\"}"
            response = requests.request("POST", url, data=payload, headers=headers)
    
            valorTmp = response.json().get("data").get("actor").get("account").get("nrql")
            custom_json = '{"resultado":"' + valorTmp.get("embeddedChartUrl") + '"}'
            parsed_json = json.dumps(custom_json)
            
            print("########################################################################")
            print(parsed_json)
            
        return parsed_json, 200