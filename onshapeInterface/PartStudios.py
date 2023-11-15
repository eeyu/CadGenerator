import onshapeInterface.ProcessUrl as RequestUrlCreator
import onshapeInterface.OnshapeAPI as OnshapeAPI
import json


class GetStl(OnshapeAPI.OnshapeAPI):
    def __init__(self, url: RequestUrlCreator.OnshapeUrl):
        super(GetStl, self).__init__(OnshapeAPI.ApiMethod.GET)
        self.stl = None
        self.request_url = RequestUrlCreator.get_api_url("partstudios",
                                                    "stl",
                                                         document=url.documentID,
                                                         workspace=url.workspaceID,
                                                         element=url.elementID,
                                                         wvm=url.wvm)

    def _get_api_url(self):
        return self.request_url

    def _get_headers(self):
        return {'Accept': 'application/vnd.onshape.v1+octet-stream',
                'Content-Type': 'application/json'}

    def send_request(self):
        payload = {
            "units": "millimeter",
            "grouping": "true",
            "scale": 1
        }
        self.stl = self.make_request(payload=payload, use_post_param=False)

    def get_response(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.stl.data.encode())


class GetFeatureList(OnshapeAPI.OnshapeAPI):
    def __init__(self, url: RequestUrlCreator.OnshapeUrl):
        super(GetFeatureList, self).__init__(OnshapeAPI.ApiMethod.GET)
        self.stl = None
        self.request_url = RequestUrlCreator.get_api_url("partstudios",
                                                         "features",
                                                         document=url.documentID,
                                                         workspace=url.workspaceID,
                                                         element=url.elementID,
                                                         wvm=url.wvm)

    def _get_api_url(self):
        return self.request_url

    def _get_headers(self):
        return {'Accept': 'application/json;charset=UTF-8; qs=0.09',
                'Content-Type': 'application/json'}

    def send_request(self):
        payload = {
            "rollbackBarIndex": -1,
            "includeGeometryIds": True,
            # "featureId": [], # There are issues with sending this array
            "noSketchGeometry": False
        }
        response = self.make_request(payload=payload, use_post_param=False)
        return response.data

class AddFeature(OnshapeAPI.OnshapeAPI):
    def __init__(self, url: RequestUrlCreator.OnshapeUrl):
        super(AddFeature, self).__init__(OnshapeAPI.ApiMethod.POST)
        self.request_url = RequestUrlCreator.get_api_url("partstudios",
                                                         "features",
                                                         document=url.documentID,
                                                         workspace=url.workspaceID,
                                                         element=url.elementID,
                                                         wvm=url.wvm)
        self.json_feature = None
        self.source_microversion = None

    def _get_api_url(self):
        return self.request_url

    def _get_headers(self):
        return {'Accept': 'application/json;charset=UTF-8; qs=0.09',
                'Content-Type': 'application/json'}

    def send_request(self):
        payload = {
            "sourceMicroversion": self.source_microversion,
            "feature": self.json_feature
        }
        response = self.make_request(payload=payload, use_post_param=False)
        return response.data

if __name__ == "__main__":
    # url = RequestUrlCreator.OnshapeUrl("https://cad.onshape.com/documents/c3b4576ef97b70b3e09ba2f0/w/75bec76c270d0cb4899d9ce4/e/2a5362fe0e6cb33b327a98de")
    # getStl = GetStl(url)
    # getStl.send_request()
    # getStl.get_response("got.stl")


    url = RequestUrlCreator.OnshapeUrl("https://cad.onshape.com/documents/c3b4576ef97b70b3e09ba2f0/w/75bec76c270d0cb4899d9ce4/e/8fbf440a3480ee969c03c26f")
    # getFeatures = GetFeatureList(url)
    # response = getFeatures.send_request()
    # print(response)

    with open("sketch.json", 'r') as f:
        s = f.read()
    feature = json.loads(s)

    addFeature = AddFeature(url)
    addFeature.json_feature = feature
    addFeature.source_microversion =  "ddffa8be62383c06c91cfe6f"
    addFeature.send_request()