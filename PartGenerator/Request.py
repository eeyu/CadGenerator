# determine json to send,
# send as blob
# extract STL

from enum import Enum
from abc import ABC, abstractmethod

class Request(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _get_type(self) -> str:
        pass

    @abstractmethod
    def create_request(self) -> dict:
        pass

class RequestBuilder:
    def __init__(self):
        self.full_request = []

    def add_request(self, request: Request):
        self.full_request.append(request.create_request())




class Hole(Request):
    # All units in mm
    def __init__(self, name: str):
        super(Hole, self).__init__()
        self.name = name
        self.axis = [1,1,1]
        self.diameter = 20
        self.depth = 25
        self.origin = [10, 10, 10]
        self.is_thru = False

    def _get_type(self) -> str:
        return "hole"

    def create_request(self) -> dict:
        request = {
            "name": self._get_type() + self.name,
            "request_type": self._get_type(),
            "contents": {
                "axis": self.axis,
                "diameter": self.diameter,
                "is_thru": self.is_thru,
                "depth": self.depth,
                "origin": self.origin
            }
        }
        return request

class Sphere(Request):
    # All units in mm
    def __init__(self, name: str):
        super(Sphere, self).__init__()
        self.name = name
        self.diameter = 20
        self.origin = [10, 10, 10]

    def _get_type(self) -> str:
        return "sphere"

    def create_request(self) -> dict:
        request = {
            "name": self._get_type() + self.name,
            "request_type": self._get_type(),
            "contents": {
                "diameter": self.diameter,
                "origin": self.origin
            }
        }
        return request

class Prism(Request):
    # All units in mm
    def __init__(self, name: str):
        super(Prism, self).__init__()
        self.name = name
        self.dimensions = [10, 20, 30] # xyz
        self.origin = [10, 10, 10]
        self.origin_is_corner = True
        # also x z axis

    def _get_type(self) -> str:
        return "prism"

    def create_request(self) -> dict:
        request = {
            "name": self._get_type() + self.name,
            "request_type": self._get_type(),
            "contents": {
                "dimensions": self.dimensions,
                "origin": self.origin,
                "origin_is_corner": self.origin_is_corner
            }
        }
        return request


if __name__ == "__main__":
    builder = RequestBuilder()

    prism1 = Prism("1")
    prism1.origin = [0,0,0]
    prism1.dimensions = [100, 200, 300]
    builder.add_request(prism1)

    prism2 = Prism("2")
    prism2.origin = [50,100,150]
    prism2.dimensions = [100, 200, 300]
    builder.add_request(prism2)

    hole1 = Hole("1")
    hole1.origin = [0,0,0]
    hole1.axis = [1,1,1]
    hole1.diameter = 30
    hole1.depth = 100
    builder.add_request(hole1)

    print(builder.full_request)
