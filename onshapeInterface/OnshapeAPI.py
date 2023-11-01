import json
from onshape_client.client import Client
from onshapeInterface.ConfigurationEncoder import ConfigurationEncoder
from abc import abstractmethod, ABC
from enum import Enum

# Move this to a text file
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
        # base = 'https://cad.onshape.com'
        self.client = Client.get_client()
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
            config = configuration.get_encoding()
            params = {'configuration': config}

        # Send the request to onshape
        # multipart post needs to pass post_params
        # normal post passes body
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
        return response





