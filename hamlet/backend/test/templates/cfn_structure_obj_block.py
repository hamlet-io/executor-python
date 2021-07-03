# NOTE: This file must remain valid python file in order to perform tests on it.
# NOTE: Imports can't be used inside a template block because all code will be merged into a single file.
# NOTE: The class is wrapped into function in order to make it testable. This adds an ability to provide parent classes
# at runtime, otherwise, the module will raise NameError


def CFNStructure(JSONValidator):
    class CFNStructure(JSONValidator):

        RESOURCES_KEY = "Resources"
        RESOURCE_TYPE_KEY = "Type"
        OUTPUT_KEY = "Outputs"

        def __resource(self, id, type):
            def validator():
                resources = self._body.get(self.RESOURCES_KEY, {})
                target = resources.get(id)
                assert target is not None, "cfn resource {} is missing".format(id)
                assert (
                    target[self.RESOURCE_TYPE_KEY] == type
                ), "cfn resource {}.{}!={}".format(id, self.RESOURCE_TYPE_KEY, type)

            validator.__name__ = "cfn resource {}.{} == {}".format(
                id, self.RESOURCE_TYPE_KEY, type
            )
            return validator

        def __output(self, id):
            def validator():
                output = self._body.get(self.OUTPUT_KEY, {})
                value = output.get(id)
                assert value is not None, "cfn output {} is missing".format(id)

            validator.__name__ = "cfn output {} exists".format(id)
            return validator

        def resource(self, id, type):
            self._validators.append(self.__resource(id, type))
            return self

        def output(self, id):
            self._validators.append(self.__output(id))
            return self

    return CFNStructure
