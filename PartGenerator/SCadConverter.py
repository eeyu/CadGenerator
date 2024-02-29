import io
from abc import ABC, abstractmethod
from collections import OrderedDict
import PartGenerator.Request as Request
import numpy as np
import PartGenerator.Math3d as Math3d
import os
import json
from csg import tokenizer
import onshapeInterface.ProcessUrl as ProcessUrl
import PartGenerator.Send as Send

# TODO: Finish cylinder
# TODO: more robust to scad file format

# parse through line by line
# build a tree
# Master: intersection, union, difference
# Subitems: requests or master
from enum import Enum

BOOLEAN_NAMES_MAP = {"union": Request.BooleanType.UNION,
                      "difference": Request.BooleanType.SUBTRACT,
                      "intersection": Request.BooleanType.INTERSECT
                     }
PRIMITIVE_NAMES = ["sphere", "cube", "cylinder"]
TRANSLATE = "translate"

# extracts name of function from line
def read_function_name_in_line(line: str):
    cleaned_line = line.strip()
    name_end = cleaned_line.find("(")
    if name_end == -1:
        return None
    return cleaned_line[:name_end]

def read_vector_from_text(text: str):
    start = text.find("[")
    end = text.find("]")
    cleaned_text = text[start + 1: end].replace(" ", "")
    numbers = cleaned_text.split(sep=",")
    array = []
    for i in numbers:
        array.append(float(i))
    return np.array(array)

# Returns either:
# - Dictionary of arg_name: arg_value
# - Single value: arg_value (if there is a single unnamed argument)
def read_arguments_in_line(line: str):
    start = line.find("(")
    end = line.find(")")
    cleaned_text = line[start + 1: end].replace(" ", "")
    arguments_split = cleaned_text.split(sep=",")

    # Here combine vector values together
    arguments_raw = []
    i = 0
    while i < len(arguments_split):
        token = arguments_split[i]
        if "[" in token:
            built_token = token
            while "]" not in token:
                i += 1
                token = arguments_split[i]
                built_token += "," + token
            arguments_raw.append(built_token)
        else:
            arguments_raw.append(token)
        i += 1


    if len(arguments_raw) == 1 and arguments_raw[0].find("=") == -1:
        # There is only 1 unnamed argument ex. translate([1.0, 2.3, 4.1])
        return convert_text_to_value(arguments_raw[0])
    else:
        # Separate into dictionary
        arguments = {}
        for raw_argument in arguments_raw:
            equals_ind = raw_argument.find("=")
            name = raw_argument[:equals_ind]

            value = raw_argument[equals_ind+1:]
            arguments[name] = convert_text_to_value(value)
        return arguments

def convert_text_to_value(text: str):
    if text == "true":
        return True
    elif text == "false":
        return False
    elif "[" in text:
        return read_vector_from_text(text)
    else:
        return float(text)

def read_function_in_line(line: str):
    function_name = read_function_name_in_line(line)
    arguments = read_arguments_in_line(line)
    return function_name, arguments

# dictionary of function_name: arguments
# reads lines building a primitive until reach a ;
def read_primitive_functions(first_line: str, scad_file: io.TextIOWrapper) -> OrderedDict:
    functions = OrderedDict()
    function_name, arguments = read_function_in_line(first_line)
    functions[function_name] = arguments
    while True:
        line = scad_file.readline()
        if ";" in line: # Assumes ; is on its own line, which will occur after cleaning
            break
        function_name, arguments = read_function_in_line(line)
        functions[function_name] = arguments


    return functions

def build_primitive_request(first_line: str, scad_file: io.TextIOWrapper):
    functions = read_primitive_functions(first_line, scad_file)
    function_names = list(functions.keys())
    function_names.reverse()

# TODO translate/rotate are in an order
    csys = Math3d.CoordSystem()
    for function_name in function_names:
        # get rotate
        if "rotate" == function_name:
            orientation = functions["rotate"]
            csys.rotate(xyz_angles=orientation)

        if "translate" == function_name:
            translation = functions["translate"]
            csys.translate(translation)

    if "sphere" in function_names:
        arguments = functions["sphere"]
        if "r" in arguments:
            diameter = arguments["r"] * 2.0
        else:
            diameter = arguments["d"]
        return Request.Sphere(origin=csys.origin,
                              diameter=diameter)
    elif "cube" in function_names:
        # TODO: rotations are not yet supported
        arguments = functions["cube"]
        return Request.Prism(dimensions=arguments["size"],
                             origin=csys.origin,
                             origin_is_corner=not arguments["center"])
    elif "cylinder" in function_names:
        arguments = functions["cylinder"]
        # TODO: cones are not yet supported.
        # TODO center shift
        if "r" in arguments:
            diameter = arguments["r"] * 2.0
        elif "r1" in arguments:
            diameter = arguments["r1"] * 2.0
        elif "d" in arguments:
            diameter = arguments["d"]
        else: # "d1"
            diameter = arguments["d1"]
        return Request.Hole(axis=csys.z_axis,
                            depth=arguments["h"],
                            origin=csys.origin,
                            diameter=diameter)
    # end at ;
def build_boolean_request(first_line: str, scad_file: io.TextIOWrapper) -> Request.BooleanRequest:
    boolean_name = read_function_name_in_line(first_line)
    combined_request = Request.BooleanRequest(boolean_type=BOOLEAN_NAMES_MAP[boolean_name])
    while True: # Continue until reach "}"
        line = scad_file.readline()
        function_name = read_function_name_in_line(line)
        if function_name is not None:
            if function_name in BOOLEAN_NAMES_MAP.keys():
                request = build_boolean_request(first_line=line, scad_file=scad_file)
            else: # normal request
                request = build_primitive_request(first_line=line, scad_file=scad_file)
            combined_request.add_request(request)

        #case for empty line
        if "}" in line: # End of combined
            break
    return combined_request


def build_tree_from_scad(scad_file_name: str):
    create_cleaned_scad_file(scad_file_name)
    with open(get_cleaned_scad_name(scad_file_name), "r") as f:
        first_line = f.readline()
        function_name = read_function_name_in_line(first_line)
        while function_name is None:
            first_line = f.readline()
            function_name = read_function_name_in_line(first_line)
        tree = build_boolean_request(first_line, f)
    os.remove(get_cleaned_scad_name(scad_file_name))
    return tree

def print_file_line(f):
    next_line = f.readline()
    print(next_line)

def get_cleaned_scad_name(scad_file_name):
    return scad_file_name + ".temp"

def create_cleaned_scad_file(scad_file_name):
    END_SEQUENCES = [")", "}", ";", "{"]
    with open(scad_file_name, "r") as f:
        with open(get_cleaned_scad_name(scad_file_name), "w") as f_temp:
            for line in f:
                separator, index = tokenizer.get_separator_index(line, separators=END_SEQUENCES)
                while index != -1:
                    until_token = line[:index+1] + "\n"
                    f_temp.write(until_token)
                    line = line[index+1:]
                    separator, index = tokenizer.get_separator_index(line, separators=END_SEQUENCES)

if __name__ == "__main__":
    # text = "translate([0, 0, 0])\n"
    # print(read_vector_from_text(text))

    filename = "scad/test.scad"
    combined_requset = build_tree_from_scad(filename)
    json_request = combined_requset.get_formatted_request()

    json_url = ProcessUrl.OnshapeUrl("https://cad.onshape.com/documents/c3b4576ef97b70b3e09ba2f0/w/ada9dc9da5700854d4df4e25/e/43845e67493d95a88592d49d")
    part_url = ProcessUrl.OnshapeUrl("https://cad.onshape.com/documents/c3b4576ef97b70b3e09ba2f0/w/ada9dc9da5700854d4df4e25/e/2a5362fe0e6cb33b327a98de")

    your_mesh = Send.build_part(json_request, part_url=part_url, json_url=json_url, name="aaa")
    # print(json.dumps(json_request, indent=4))
    # a = "sphere(r = 57, $fn = 12);"
    # print(read_arguments_in_line(a))