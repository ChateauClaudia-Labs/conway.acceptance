from conway.database.single_root_data_hub                                      import RelativeDataHubHandle

from conway_acceptance.scenario_foundry.scenario_manifest                                  import ScenarioManifest
from conway_acceptance.util.test_statics                                                   import TestStatics
from conway_acceptance.test_database.projector_data_hub                                    import Projector_DataHub

class ProjectorScenarioManifest(ScenarioManifest):

    def __init__(self, scenarios_root_folder, scenario_id):
        '''
        This is a manifest class for an unusual kind of scenario: instead of testing the normal
        "rolling" behavior of the application, these scenarios test the troubleshooting tooling that is provided
        through the DatabaseProjector.

        @param scenarios_root_folder A string representing the absolute path to a folder which serves as the root
            for all test databases across all test scenarios. The test database for which this is a specification
            will be created in `scenarios_root_folder/scenario/`
 
        @param scenario_id An integer that serves as the unique identifier for the scenario for which this is a
            a specification. A YAML file that maps such numerical ids to the classname of the code that implements
            a test scenario can be found in `scenarios_root_folder/ScenarioIds.yaml`

        '''
        super().__init__(scenarios_root_folder, scenario_id)


    def get_data_hubs(self):
        '''
        Returns an list of conway.database.data_hub.DataHub objects that define all the DataHubs
        that need to be set up for the test database specific by this ProjectorScenarioManifest instance.
        '''
        
        input_db_hub                         = Projector_DataHub(name       = TestStatics.PROJECTOR_INPUT_DB_FOLDER,
                                                                 hub_handle = RelativeDataHubHandle(
                                                                                        self.path_to_actuals(), 
                                                                                        TestStatics.PROJECTOR_INPUT_DB_FOLDER))

        return [input_db_hub]
    
    
