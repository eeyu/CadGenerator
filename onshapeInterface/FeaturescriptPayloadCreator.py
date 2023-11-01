# Class creates the payload to send via the Featurescript API endpoint

class FeaturescriptCreator:
    def get_attribute(attribute_name : str):
        script = """
        function (context is Context, queries is map)
        {{
            var instantiatedBodies = qHasAttribute(qEverything(EntityType.BODY), "{attributeName}");

            // This is what we are looking for
            var outputKinematics = getAttribute(context, {{"entity" : instantiatedBodies, "name" : "{attributeName}"}});
            return outputKinematics;
        }}
        """.format(attributeName=attribute_name)
        queries = []
        return script, queries
