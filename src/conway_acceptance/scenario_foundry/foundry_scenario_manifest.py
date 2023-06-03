from conway.database.single_root_data_hub                                      import RelativeDataHubHandle

from conway_acceptance.scenario_foundry.scenario_manifest                                  import ScenarioManifest
from conway_acceptance.util.test_statics                                                   import TestStatics
from conway_acceptance.test_database.generated_scenario_data_hub                           import GeneratedScenarioDataHub
from conway_acceptance.test_database.global_datasets_data_hub                              import GlobalDatasetsDataHub

class Foundry_ScenarioManifest(ScenarioManifest):

    def __init__(self, scenarios_root_folder, scenario_id, fake_scenario_id):
        '''
        This is a manifest class for an unusual kind of scenario: instead of testing the application 
        (i.e., `vulnerability_management`), these scenarios test the scenario-generation logic itself.

        Thus, these are "meta tests" in which we have the "fake world" living under the "real world":

        * These tests generate "fake scenarios"

        * These "fake scenarios" live in a "fake scenario area"

        * This "fake scenario areas" live under a "real scenario" (the one for which this class is a manifest)

        * And that lives in the "real scenario area"

        @param scenarios_root_folder A string representing the absolute path to a folder which serves as the root
            for all test databases across all test scenarios. The test database for which this is a specification
            will be created in `scenarios_root_folder/scenario/`
 
        @param scenario_id An integer that serves as the unique identifier for the scenario for which this is a
            a specification. A YAML file that maps such numerical ids to the classname of the code that implements
            a test scenario can be found in `scenarios_root_folder/ScenarioIds.yaml`

        @param fake_scenario_id An integer pretending to identify a scenario, but not one that lives in the real
            world - just a fake scenario that is being acted on by the test case for this manifest.
        '''
        super().__init__(scenarios_root_folder, scenario_id)

        self.fake_scenario_id                       = fake_scenario_id


    def get_data_hubs(self):
        '''
        Returns an list of conway.database.data_hub.DataHub objects that define all the DataHubs
        that need to be set up for the test database specific by this Foundry_ScenarioManifest instance.
        '''
        global_datasets_hub                         = GlobalDatasetsDataHub(
                                                        name        = TestStatics.GLOBAL_DATASETS_FOLDER,
                                                        hub_handle  = RelativeDataHubHandle(
                                                                        db_root_folder      = self.path_to_actuals(), 
                                                                        relative_path       = TestStatics.GLOBAL_DATASETS_FOLDER))

        fake_scenario_hub                           = GeneratedScenarioDataHub(
                                                        name        = self.fake_scenario_id,
                                                        hub_handle  = RelativeDataHubHandle(
                                                                        db_root_folder      = self.path_to_actuals(), 
                                                                        relative_path       = self.fake_scenario_id))


        return [global_datasets_hub, fake_scenario_hub]
    
    
