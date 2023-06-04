from conway.database.single_root_data_hub                      import SingleRootDataHub, DataHubHandle

class GeneratedScenarioDataHub(SingleRootDataHub):

    def __init__(self, name, hub_handle: DataHubHandle):

        super().__init__(name, hub_handle)

    def _instantiate(self, name, hub_handle: DataHubHandle):

        return GeneratedScenarioDataHub(name, hub_handle)
