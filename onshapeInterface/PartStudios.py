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
        print(self.request_url)
        return self.request_url

    def _get_headers(self):
        return {'Accept': 'application/vnd.onshape.v1+octet-stream',
                'Content-Type': 'application/json'}

    def send_request(self):
        # payload = {}
        self.stl = self.make_request()
    
    def get_response(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.stl.data.encode())


if __name__ == "__main__":
    url = RequestUrlCreator.OnshapeUrl("https://cad.onshape.com/documents/c3b4576ef97b70b3e09ba2f0/w/75bec76c270d0cb4899d9ce4/e/2a5362fe0e6cb33b327a98de")
    getStl = GetStl(url)
    getStl.send_request()
    getStl.get_response("got.stl")