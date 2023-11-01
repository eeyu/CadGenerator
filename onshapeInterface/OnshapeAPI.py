import json
from onshape_client.client import Client
from onshapeInterface.ConfigurationEncoder import ConfigurationEncoder
from abc import abstractmethod, ABC
from enum import Enum

secret_key = "6omX9qirGWPl2ZfPK5Ephr76NbdgqL3ATg57gXKqWIdsjcGs"
access_key = "w0aYMqeAYCpmYbo8OZAeNv6G"
base = 'https://cad.onshape.com'
client = Client(configuration={"base_url": base,
                                    "access_key": access_key,
                                    "secret_key": secret_key})
class ApiMethod(Enum):
    POST = "POST"
    GET = "GET"


class OnshapeAPI(ABC):
    def __init__(self, method : ApiMethod):
        base = 'https://cad.onshape.com'
        self.client = Client.get_client()
        # self.headers = {'Accept': 'application/json;charset=UTF-8;qs=0.09',
        #                 'Content-Type': 'application/json'}
        self.method = method.value

    @abstractmethod
    def _get_api_url(self):
        pass

    @abstractmethod
    def _get_headers(self):
        pass

    # inputs is np array, unitsList is string array
    # returns parsed API request, or None if error occurred
    def make_request(self, configuration: ConfigurationEncoder = None, payload: dict | list | None = None, use_post_param: bool = False):
        # Configuration of the request
        params = {}
        if configuration is not None:
            config = configuration.getEncoding()
            params = {'configuration': config}

        # Send the request to onshape
        if use_post_param:
            response = self.client.api_client.request(method=self.method,  # specific
                                                           url=self._get_api_url(),  # general-specific
                                                           query_params=params,  # general
                                                           headers=self._get_headers(),  # general
                                                           post_params=payload) # specific
        else:
            response = self.client.api_client.request(method=self.method,  # specific
                                                           url=self._get_api_url(),  # general-specific
                                                           query_params=params,  # general
                                                           headers=self._get_headers(),  # general
                                                           body=payload)  # specific
        # multipart needs to pass post_params
        # normal passes body
        return response
        # parsed = json.loads(response.data)
        #
        # if "notices" in parsed.keys() and len(parsed["notices"]) > 0:
        #     print("Onshape Error: ")
        #     print(configuration.numpyParameters)
        #     return None

        # return parsed




