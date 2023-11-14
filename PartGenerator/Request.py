from abc import ABC, abstractmethod
from enum import Enum

import numpy as np


class BooleanType(Enum):
    ADD = "ADD"
    SUBTRACT = "SUBTRACT"

class Request(ABC):
    def __init__(self, name, boolean_type: BooleanType):
        self.name = name
        self.boolean_type = boolean_type

    @abstractmethod
    def get_type(self) -> str:
        pass

    def get_name(self) -> str:
        return self.name

    @abstractmethod
    def get_contents(self) -> dict:
        pass

    def get_boolean_type(self) -> str:
        return self.boolean_type.name

class RequestBuilder:
    def __init__(self):
        self.full_request = []

    def add_request(self, request: Request):
        formatted_request = {
            "name": request.get_type() + request.get_name(),
            "request_type": request.get_type(),
            "boolean_type": request.get_boolean_type(),
            "contents": request.get_contents()
            }
        self.full_request.append(formatted_request)


class Hole(Request):
    # All units in mm
    def __init__(self, name: str,
                 boolean_type: BooleanType,
                 axis=np.array([1, 1, 1]),
                 diameter=20,
                 depth=25,
                 origin=np.array([10, 10, 10]),
                 is_thru=False):
        super(Hole, self).__init__(name, boolean_type)
        self.axis = axis
        self.diameter = diameter
        self.depth = depth
        self.origin = origin
        self.is_thru = is_thru

    def get_type(self) -> str:
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
    def __init__(self, name: str,
                 boolean_type: BooleanType,
                 diameter=20,
                 origin=np.array([10, 10, 10])):
        super(Sphere, self).__init__(name, boolean_type)
        self.diameter = diameter
        self.origin = origin

    def get_type(self) -> str:
        return "sphere"

    def get_contents(self) -> dict:
        contents = {
                "diameter": self.diameter,
                "origin": self.origin.tolist()
            }
        return contents


class Prism(Request):
    # All units in mm
    def __init__(self, name: str,
                 boolean_type: BooleanType,
                 dimensions=np.array([10, 20, 30]),
                 origin=np.array([10, 10, 10]),
                 origin_is_corner=True):
        super(Prism, self).__init__(name, boolean_type)
        self.dimensions = dimensions # xyz
        self.origin = origin
        self.origin_is_corner = origin_is_corner

        # self.origin_is_corner = origin_is_corner
        # also x z axis

    def get_type(self) -> str:
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
