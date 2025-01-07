import onshapeInterface.ProcessUrl as RequestUrlCreator
import onshapeInterface.OnshapeAPI as OnshapeAPI
import json
from onshapeInterface import PartStudios
import numpy as np

def json_print(parsed):
    print(json.dumps(parsed, indent=4))

if __name__ == "__main__":
    url = RequestUrlCreator.OnshapeUrl("https://cad.onshape.com/documents/c36fe1255ee04ace7323d7d2/w/5f2505bde953b6cf71b7011f/e/e41a3a4624ccb8c5ee3a50f3")
    getFeatures = PartStudios.GetFeatureList(url)
    response = getFeatures.send_request()
    json_print(response["features"])