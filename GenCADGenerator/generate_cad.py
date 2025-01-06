import onshapeInterface.ProcessUrl as RequestUrlCreator
import onshapeInterface.OnshapeAPI as OnshapeAPI
import json
from onshapeInterface import PartStudios
import numpy as np
from onshapeInterface import FeaturescriptPayloadCreator

class Plane:
    def __init__(self):
        direction = []
        geometry_id = []
        name = "hello"
        self.message = {
            "type": 134,
            "typeName": "BTMFeature",
            "message": {
                "featureType": "cPlane",
                "featureId": name,
                "name": "Plane 1",
                "parameters": [
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [
                                {
                                    "type": 138,
                                    "typeName": "BTMIndividualQuery",
                                    "message": {
                                        "geometryIds": [
                                            "JCC"
                                        ],
                                    }
                                }
                            ],
                            "parameterId": "entities",
                        }
                    },
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "CPlaneType",
                            "value": "OFFSET",
                            "namespace": "",
                            "parameterId": "cplaneType",
                        }
                    },
                    {
                        "type": 147,
                        "typeName": "BTMParameterQuantity",
                        "message": {
                            "units": "",
                            "value": 0.0,
                            "expression": "25 mm",
                            "parameterId": "offset",
                        }
                    },
                    {
                        "type": 147,
                        "typeName": "BTMParameterQuantity",
                        "message": {
                            "value": 0.0,
                            "expression": "0 deg",
                            "parameterId": "angle",
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "parameterId": "oppositeDirection",
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "parameterId": "flipAlignment",
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "parameterId": "flipNormal"
                        }
                    },
                ],
            }
        }
    def get_json(self):
        return self.message

class SketchFeature:
    def __init__(self, name, plane_geometry_id):
        self.message = {
            "type": 151,
            "typeName": "BTMSketch",
            "message": {
                "entities": [],
                "constraints": [],
                "featureType": "newSketch",
                "name": name,
                "parameters": [
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [
                                {
                                    "type": 138,
                                    "typeName": "BTMIndividualQuery",
                                    "message": {
                                        "geometryIds": [
                                            plane_geometry_id
                                        ]
                                    }
                                }
                            ],
                            "parameterId": "sketchPlane"
                        }
                    }
                ]
            }

        }

    def add_entity(self, entity):
        self.message["message"]["entities"].append(entity.get_json())

    def add_constraint(self, constraint):
        self.message["message"]["constraints"].append(constraint.get_json())

    def get_json(self):
        return self.message

    def get_geometry_id(self):
        pass



class SketchEntityLine:
    def __init__(self, start, stop, name, is_construction=False):
        start /= 1000.0
        stop /= 1000.0
        direction = stop - start
        length = np.linalg.norm(direction)
        direction = direction / length
        self.name = name

        self.message = {
            "type": 155,
            "typeName": "BTMSketchCurveSegment",
            "message": {
                "startPointId": name + ".start",
                "endPointId": name + ".end",
                "startParam": 0.0,
                "endParam": length,
                "geometry": {
                    "type": 117,
                    "typeName": "BTCurveGeometryLine",
                    "message": {
                        "pntX": float(start[0]),
                        "pntY": float(start[1]),
                        "dirX": float(direction[0]),
                        "dirY": float(direction[1])
                    }
                },
                "entityId": name,
                "isConstruction": is_construction,
            }
        }

    def get_json(self):
        return self.message


class SketchConstraintCoincident:
    def __init__(self, name1, name2):
        self.message = {
            "type": 2,
            "typeName": "BTMSketchConstraint",
            "message": {
                "constraintType": "COINCIDENT",
                "parameters": [
                    {
                        "type": 149,
                        "typeName": "BTMParameterString",
                        "message": {
                            "value": name2 + ".start",
                            "parameterId": "localFirst"
                        }
                    },
                    {
                        "type": 149,
                        "typeName": "BTMParameterString",
                        "message": {
                            "value": name1 + ".end",
                            "parameterId": "localSecond"
                        }
                    }
                ]
            }
        }

    def get_json(self):
        return self.message



# class SketchPlane:
#     def __init__(self, theta, phi, lambd, px, py, pz):
#         # If theta is a default plane, choose simply
#         # If not default plane, do hard mode
#         self.final_sketch_plane = create_sketch_plane(theta, phi, lambd, px, py, pz)
#
#     def get_json(self):
#         # extrude1, extrude2, sketch
#         pass
#
#     def get_geometry_id(self):
#         pass


class MateConnector:
    def __init__(self, feature_name, id_name, rotation_axis, rotation, origin_geometry_id, origin_translation):
        if rotation_axis == "x":
            rotation_axis = "ABOUT_X"
        elif rotation_axis == "y":
            rotation_axis = "ABOUT_Y"
        else:
            rotation_axis = "ABOUT_Z"
        self.message = {
            "type": 134,
            "typeName": "BTMFeature",
            "message": {
                "featureType": "mateConnector",
                "featureId": id_name,
                "name": feature_name,
                "parameters": [
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "OriginCreationType",
                            "value": "ON_ENTITY",
                            "namespace": "",
                            "parameterId": "originType"
                        }
                    },
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [
                                {
                                    "type": 138,
                                    "typeName": "BTMIndividualQuery",
                                    "message": {
                                        "geometryIds": [
                                            origin_geometry_id
                                        ]
                                    }
                                }
                            ],
                            "parameterId": "originQuery"
                        }
                    },
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "EntityInferenceType",
                            "value": "POINT",
                            "namespace": "",
                            "parameterId": "entityInferenceType"
                        }
                    },
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [],
                            "parameterId": "secondaryOriginQuery"
                        }
                    },
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [],
                            "parameterId": "originAdditionalQuery"
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": True,
                            "parameterId": "realign"
                        }
                    },
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [],
                            "parameterId": "primaryAxisQuery"
                        }
                    },
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [],
                            "parameterId": "secondaryAxisQuery"
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": True,
                            "parameterId": "transform"
                        }
                    },
                    {
                        "type": 147,
                        "typeName": "BTMParameterQuantity",
                        "message": {
                            "units": "",
                            "value": 0.0,
                            "expression": str(origin_translation[0]) + " mm",
                            "isInteger": False,
                            "parameterId": "translationX"
                        }
                    },
                    {
                        "type": 147,
                        "typeName": "BTMParameterQuantity",
                        "message": {
                            "units": "",
                            "value": 0.0,
                            "expression": str(origin_translation[1]) + " mm",
                            "isInteger": False,
                            "parameterId": "translationY"
                        }
                    },
                    {
                        "type": 147,
                        "typeName": "BTMParameterQuantity",
                        "message": {
                            "units": "",
                            "value": 0.0,
                            "expression": str(origin_translation[2]) + " mm",
                            "isInteger": False,
                            "parameterId": "translationZ"
                        }
                    },
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "RotationType",
                            "value": rotation_axis,
                            "namespace": "",
                            "parameterId": "rotationType"
                        }
                    },
                    {
                        "type": 147,
                        "typeName": "BTMParameterQuantity",
                        "message": {
                            "units": "",
                            "value": 0.0,
                            "expression": str(rotation) + " deg",
                            "isInteger": False,
                            "parameterId": "rotation"
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": True,
                            "parameterId": "allowOwnerEntity"
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": False,
                            "parameterId": "requireOwnerPart"
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": True,
                            "parameterId": "specifyNormal"
                        }
                    },
                    {
                        "type": 147,
                        "typeName": "BTMParameterQuantity",
                        "message": {
                            "units": "",
                            "value": 1.0,
                            "expression": "0",
                            "isInteger": False,
                            "parameterId": "nx"
                        }
                    },
                    {
                        "type": 147,
                        "typeName": "BTMParameterQuantity",
                        "message": {
                            "units": "",
                            "value": 2.0,
                            "expression": "0",
                            "isInteger": False,
                            "parameterId": "ny"
                        }
                    },
                    {
                        "type": 147,
                        "typeName": "BTMParameterQuantity",
                        "message": {
                            "units": "",
                            "value": 0.0,
                            "expression": "0",
                            "isInteger": False,
                            "parameterId": "nz"
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": False,
                            "parameterId": "flipPrimary"
                        }
                    },
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "MateConnectorAxisType",
                            "value": "PLUS_X",
                            "namespace": "",
                            "parameterId": "secondaryAxisType"
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": False,
                            "parameterId": "isForSubFeature"
                        }
                    }
                ],
                "suppressed": False,
                "namespace": "",
                "subFeatures": [],
                "returnAfterSubfeatures": False,
                "suppressionState": {
                    "type": 0
                }
            }
        }

    def get_json(self):
        return self.message

class TransformRotation:
    def __init__(self, feature_name, feature_id, target_geometry_id, axis_geometry_id, angle):
        self.message = {
            "type": 134,
            "typeName": "BTMFeature",
            "message": {
                "featureType": "transform",
                "featureId": feature_id,
                "name": feature_name,
                "parameters": [
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [
                                {
                                    "type": 138,
                                    "typeName": "BTMIndividualQuery",
                                    "message": {
                                        "geometryIds": [
                                            target_geometry_id
                                        ]
                                    }
                                }
                            ],
                            "parameterId": "entities"
                        }
                    },
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "TransformType",
                            "value": "ROTATION",
                            "namespace": "",
                            "parameterId": "transformType"
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": False,
                            "parameterId": "oppositeDirectionEntity"
                        }
                    },
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [
                                {
                                    "type": 138,
                                    "typeName": "BTMIndividualQuery",
                                    "message": {
                                        "geometryIds": [
                                            axis_geometry_id
                                        ]
                                    }
                                }
                            ],
                            "parameterId": "transformAxis"
                        }
                    },
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [],
                            "parameterId": "transformDirection"
                        }
                    },

                    {
                        "type": 147,
                        "typeName": "BTMParameterQuantity",
                        "message": {
                            "units": "",
                            "value": 0.0,
                            "expression": str(angle) + " deg",
                            "isInteger": False,
                            "parameterId": "angle"
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": False,
                            "parameterId": "oppositeDirection"
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": False,
                            "parameterId": "makeCopy"
                        }
                    }
                ]
            }
        }

    def get_json(self):
        return self.message

class FeatureExtrude:
    def __init__(self, name, sketch_geometry_id, e1, e2):
        self.message = {
            "type": 134,
            "typeName": "BTMFeature",
            "message": {
                "featureType": "extrude",
                "featureId": name,
                "name": name,
                "parameters": [
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "OperationDomain",
                            "value": "MODEL",
                            "namespace": "",
                            "parameterId": "domain"
                        }
                    },
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "ExtendedToolBodyType",
                            "value": "SOLID",
                            "namespace": "",
                            "parameterId": "bodyType"
                        }
                    },
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "NewBodyOperationType",
                            "value": "NEW",
                            "namespace": "",
                            "parameterId": "operationType"
                        }
                    },
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "NewSurfaceOperationType",
                            "value": "NEW",
                            "namespace": "",
                            "parameterId": "surfaceOperationType"
                        }
                    },
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "FlatOperationType",
                            "value": "REMOVE",
                            "namespace": "",
                            "parameterId": "flatOperationType"
                        }
                    },
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [
                                {
                                    "type": 138,
                                    "typeName": "BTMIndividualQuery",
                                    "message": {
                                        "geometryIds": [
                                            sketch_geometry_id
                                        ]
                                    }
                                }
                            ],
                            "parameterId": "entities"
                        }
                    },
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [],
                            "parameterId": "surfaceEntities"
                        }
                    },
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "BoundingType",
                            "value": "BLIND",
                            "namespace": "",
                            "parameterId": "endBound"
                        }
                    },
                    {
                        "type": 147,
                        "typeName": "BTMParameterQuantity",
                        "message": {
                            "expression": str(e1) + " mm",
                            "parameterId": "depth"
                        }
                    },
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [],
                            "parameterId": "extrudeDirection"
                        }
                    },

                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": True,
                            "parameterId": "hasSecondDirection"
                        }
                    },
                    {
                        "type": 145,
                        "typeName": "BTMParameterEnum",
                        "message": {
                            "enumName": "BoundingType",
                            "value": "BLIND",
                            "namespace": "",
                            "parameterId": "secondDirectionBound"
                        }
                    },
                    {
                        "type": 147,
                        "typeName": "BTMParameterQuantity",
                        "message": {
                            "expression": str(e2) + " mm",
                            "parameterId": "secondDirectionDepth"
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": False,
                            "parameterId": "defaultScope"
                        }
                    },
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [],
                            "parameterId": "booleanScope"
                        }
                    },
                    {
                        "type": 144,
                        "typeName": "BTMParameterBoolean",
                        "message": {
                            "value": False,
                            "parameterId": "defaultSurfaceScope"
                        }
                    },
                    {
                        "type": 148,
                        "typeName": "BTMParameterQueryList",
                        "message": {
                            "queries": [],
                            "parameterId": "booleanSurfaceScope"
                        }
                    }
                ]
            }
        }

    def get_json(self):
        return self.message

def json_print(parsed):
    print(json.dumps(parsed, indent=4))

def get_microversion(url):
    getFeatures = PartStudios.GetFeatureList(url)
    response = getFeatures.send_request()
    microversion = response["sourceMicroversion"]
    return microversion

def create_sketch_plane(name, url, yaw, pitch, roll, px, py, pz):
    microversion = get_microversion(url)

    # First place the mate connector
    ev_featurescript = PartStudios.EvaluateFeaturescipt(url)
    ev_featurescript.source_microversion = microversion
    ev_featurescript.set_query_points()
    output = ev_featurescript.send_request()
    query = ev_featurescript.get_query_result(output)

    mate_connector = MateConnector("Sketch Plane " + name, "sk"+name, "z", yaw, query[0], np.array([px, py, pz]))
    feature = mate_connector.get_json()

    addFeature = PartStudios.AddFeature(url)
    addFeature.json_feature = feature
    addFeature.source_microversion = microversion
    addFeature.send_request()

    # Get the mc
    ev_featurescript.set_query_mate_connectors()
    output = ev_featurescript.send_request()
    query = ev_featurescript.get_query_result(output)
    microversion = get_microversion(url)

    # Put the axis handle on the mate connector
    sketch = SketchFeature("Yaw_sketch", query[-1])
    line1 = SketchEntityLine(start=np.array([0., 0.]), stop=np.array([1., 0.]), name="hello"+name, is_construction=True)
    sketch.add_entity(line1)
    feature = sketch.get_json()

    addFeature = PartStudios.AddFeature(url)
    addFeature.json_feature = feature
    addFeature.source_microversion = microversion
    addFeature.send_request()

    # Transform 1
    # First grab the mate connector and the axis of rotation
    microversion = get_microversion(url)
    ev_featurescript.set_query_mate_connectors()
    output = ev_featurescript.send_request()
    query = ev_featurescript.get_query_result(output)
    mate_connector = query[-1]

    ev_featurescript.set_query_sketch_construction()
    output = ev_featurescript.send_request()
    query = ev_featurescript.get_query_result(output)
    rotation_axis = query[-1]

    feature = TransformRotation(feature_name="Transform Pitch", feature_id="asdf2"+name, target_geometry_id=mate_connector,
                                axis_geometry_id=rotation_axis, angle=pitch)
    feature = feature.get_json()
    addFeature = PartStudios.AddFeature(url)
    addFeature.json_feature = feature
    addFeature.source_microversion = microversion
    addFeature.send_request()

    # Transform 2
    # Grab the MC again
    microversion = get_microversion(url)
    ev_featurescript.set_query_mate_connectors()
    output = ev_featurescript.send_request()
    query = ev_featurescript.get_query_result(output)
    mate_connector = query[-1]

    feature = TransformRotation(feature_name="Transform Roll", feature_id="asdf_roll"+name,
                                target_geometry_id=mate_connector, axis_geometry_id=mate_connector, angle=roll)
    feature = feature.get_json()
    addFeature = PartStudios.AddFeature(url)
    addFeature.json_feature = feature
    addFeature.source_microversion = microversion
    addFeature.send_request()

    microversion = get_microversion(url)
    ev_featurescript.set_query_mate_connectors()
    output = ev_featurescript.send_request()
    query = ev_featurescript.get_query_result(output)
    sketch_plane = query[-1]
    return sketch_plane, microversion




if __name__ == "__main__":
    url = RequestUrlCreator.OnshapeUrl("https://cad.onshape.com/documents/c36fe1255ee04ace7323d7d2/w/5f2505bde953b6cf71b7011f/e/e41a3a4624ccb8c5ee3a50f3")
    # getFeatures = PartStudios.GetFeatureList(url)
    # response = getFeatures.send_request()
    # json_print(response["features"])

    # with open("mate_connector_reference.json", "r") as f:
    #     s = f.read()
    # feature = json.loads(s)


    sketch_plane, microversion = create_sketch_plane("sketch 1", url, yaw=30, pitch=30, roll=30, px=10, py=10, pz=10)

    # The sketch plane has been created. Now add the sketch
    sketch = SketchFeature("Sketch42", plane_geometry_id=sketch_plane)
    line1 = SketchEntityLine(start=np.array([0., 0.]), stop=np.array([10., 10.]), name="hello")
    sketch.add_entity(line1)
    sketch.add_entity(SketchEntityLine(start=np.array([10., 10.]), stop=np.array([40., 0.]), name="hello2"))
    sketch.add_entity(SketchEntityLine(start=np.array([40., 0.]), stop=np.array([0., 0.]), name="hello3"))

    sketch.add_constraint(SketchConstraintCoincident("hello", "hello2"))
    sketch.add_constraint(SketchConstraintCoincident("hello2", "hello3"))

    feature = sketch.get_json()
    addFeature = PartStudios.AddFeature(url)
    addFeature.json_feature = feature
    addFeature.source_microversion = microversion
    addFeature.send_request()

    # Now extrude
    # Grab sketch
    microversion = get_microversion(url)

    ev_featurescript = PartStudios.EvaluateFeaturescipt(url)
    ev_featurescript.source_microversion = microversion
    ev_featurescript.set_query_sketch_faces()
    output = ev_featurescript.send_request()
    query = ev_featurescript.get_query_result(output)

    extrude = FeatureExtrude("Extrude Triangle", query[-1], 15, 20)
    feature = extrude.get_json()
    addFeature = PartStudios.AddFeature(url)
    addFeature.json_feature = feature
    addFeature.source_microversion = microversion
    addFeature.send_request()

