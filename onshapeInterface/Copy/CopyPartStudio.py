from onshapeInterface import PartStudios
from onshapeInterface import ProcessUrl
import json

if __name__ == "__main__":
    # Create part studio in destination workspace
    destination_url = ProcessUrl.OnshapeUrl("https://cad.onshape.com/documents/33e9cef34a8710e9af63a96c/w/e904b99375c8197966c234e3/e/744b2414634438185d097327")
    create_studio = PartStudios.NewPartStudio(destination_url)
    create_studio.name = "test name"
    create_studio.send_request()
    created_element_id = create_studio.created_element_id

    # Need to obtain microversion
    getFeatures1 = PartStudios.GetFeatureList(destination_url)
    response = getFeatures1.send_request()
    microversion = getFeatures1.microversion_id

    # Get features from source studio
    source_url = ProcessUrl.OnshapeUrl("https://cad.onshape.com/documents/c0c8de547f698ba23cb11433/w/7507e9ebffdf96bd153ff830/e/753728fe22c7cb5cc890d5d9")
    getFeatures = PartStudios.GetFeatureList(source_url)
    response = getFeatures.send_request()
    features = response["features"]

    with open("source.json", "w") as f:
        json.dump(features, f, indent=4)

    # Add the features to the created part studio
    destination_url.elementID = created_element_id
    addFeature = PartStudios.AddFeature(destination_url)
    addFeature.source_microversion = microversion

    for feature in features:
        addFeature.json_feature = feature
        addFeature.send_request()

    # Save for debugging
    getFeatures1 = PartStudios.GetFeatureList(destination_url)
    response = getFeatures1.send_request()
    features = response["features"]

    with open("new.json", "w") as f:
        json.dump(features, f, indent=4)