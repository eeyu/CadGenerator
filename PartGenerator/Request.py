from abc import ABC, abstractmethod
from enum import Enum

import numpy as np

class RequestGroup(Enum):
    PRIMITIVE = "PRIMITIVE"
    BOOLEAN = "BOOLEAN"


class Request(ABC):
    def __init__(self, id, request_group: RequestGroup):
        self.id = id
        self.request_group = request_group

    @abstractmethod
    def get_method(self) -> str:
        pass

    def get_id(self) -> str:
        return self.id

    @abstractmethod
    def get_contents(self) -> dict:
        pass

    def get_formatted_request(self) -> dict:
        formatted_request = {
            "id": self.get_method() + self.get_id(),
            "request_group": self.request_group,
            "request_method": self.get_method(),
            "contents": self.get_contents()
            }
        return formatted_request


class RequestBuilder:
    def __init__(self):
        self.full_request = []

    def add_request(self, request: Request):
        formatted_request = {
            "name": request.get_method() + request.get_id(),
            "request_type": request.get_method(),
            "contents": request.get_contents()
            }
        self.full_request.append(formatted_request)


class Hole(Request):
    # All units in mm
    def __init__(self, id: str,
                 axis=np.array([1, 1, 1]),
                 diameter=20,
                 depth=25,
                 origin=np.array([10, 10, 10]),
                 is_thru=False):
        super(Hole, self).__init__(id, RequestGroup.PRIMITIVE)
        self.axis = axis
        self.diameter = diameter
        self.depth = depth
        self.origin = origin
        self.is_thru = is_thru

    def get_method(self) -> str:
        return "hole"

    def get_contents(self) -> dict:
        contents = {
                "axis": self.axis.tolist(),
                "diameter": self.diameter,
                "is_thru": self.is_thru,
                "depth": self.depth,
                "origin": self.origin.tolist()
            }
        return contents


class Sphere(Request):
    # All units in mm
    def __init__(self, id: str,
                 diameter=20,
                 origin=np.array([10, 10, 10])):
        super(Sphere, self).__init__(id, RequestGroup.PRIMITIVE)
        self.diameter = diameter
        self.origin = origin

    def get_method(self) -> str:
        return "sphere"

    def get_contents(self) -> dict:
        contents = {
                "diameter": self.diameter,
                "origin": self.origin.tolist()
            }
        return contents


class Prism(Request):
    # All units in mm
    def __init__(self, id: str,
                 dimensions=np.array([10, 20, 30]),
                 origin=np.array([10, 10, 10]),
                 origin_is_corner=True):
        super(Prism, self).__init__(id, RequestGroup.PRIMITIVE)
        self.dimensions = dimensions # xyz
        self.origin = origin
        self.origin_is_corner = origin_is_corner

        # self.origin_is_corner = origin_is_corner
        # also x z axis

    def get_method(self) -> str:
        return "prism"

    def get_contents(self) -> dict:
        if self.origin_is_corner:
            origin = self.origin
        else:
            origin = self.origin - self.dimensions / 2.0

        contents = {
                "dimensions": self.dimensions.tolist(),
                "origin": origin.tolist(),
            }
        return contents

class BooleanType(Enum):
    UNION = "UNION"
    SUBTRACT = "SUBTRACT"
    INTERSECT = "INTERSECT"

class BooleanRequest(Request):
    def __init__(self, boolean_type: BooleanType, name: str):
        super(BooleanRequest, self).__init__(name, RequestGroup.BOOLEAN)
        self.boolean_type = boolean_type
        self.base_request = None
        self.further_requests = [] # Request or CombiedRequest

    def add_request(self, request: Request):
        if self.base_request is None:
            request.id = self.get_id()
            self.base_request = request
        else:
            sub_name = self.get_id() + str(len(self.further_requests))
            request.id = sub_name
        self.further_requests.append(request)

    def get_method(self) -> str:
        return self.boolean_type.name


    def get_contents(self) -> list:
        contents = []
        for request in self.further_requests:
            contents.append(request.get_formatted_request())
        return contents

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
