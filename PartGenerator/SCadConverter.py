from abc import ABC, abstractmethod

# parse through line by line
# build a tree
# Master: intersection, union, difference
# Subitems: requests or master

class CombinedRequest(ABC):
    def __init__(self):
        self.type = type
        self.items = [] # Request or CombiedRequest

class UnionRequest(CombinedRequest):
    def __init__(self):
        pass

def build_tree_from_scad(scad_file: str):
    tree = {}
    with open(scad_file, "r") as f:
        while f has lines:
            line = f.next_line()
            if line has intersetc/union/difference
                build tree

def build_tree_from_scad_file(scad_file: File):
    read a line
    tree = create_comined_request(name from line)
    while f has lines:
        line = f.next_line()
        if line has intersect/union/difference:
            request = buid_tree_from_scad(line)
        if line has normal request
            request = convert(read 2 lines)
        tree.append(request)
    return tree