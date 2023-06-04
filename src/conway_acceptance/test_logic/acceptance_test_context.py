import abc

from conway.application.application                        import Application
from conway.observability.logger                           import Logger

class AcceptanceTestContext(abc.ABC):

    def __init__(self, scenario_id, manifest, notes, seeding_round=0):
        '''
        This class is a Python context manager intended to be invoked by each test method of an AcceptanceTestCase
        concrete class.

        When entered into using the "with" Python keyword, it returns a TestDatabase initialized with the parameter `spec`.

        @param manifest A ScenarioManifest object that has connection strings to access the test database that should be used
            by the test case using this AcceptanceTestContext.

        @param scenario_id An integer that serves as the unique identifier for the scenario for which this is a
            a specification. A YAML file that maps such numerical ids to the classname of the code that implements
            a test scenario can be found in `scenarios_root_folder/ScenarioIds.yaml`

        @param notes A AcceptanceTestNotes object, that should be the data structure in which the test case can record
                observations in the course of its execution under this context. When the context exits these notes
                will be saved to the sceneario folder, under the subfolder given by the static variable
                TestStatics.

        @param seeding_round An int, designating the round fo seeding for which we seek the path.
                By default it is 0, meaning that the test datbase should be seeded from conteint in a folder called "SEED@T0". 
                For some test cases that is the only seeding event in the lifecycle of the test, but other test cases require 
                multiple phases where at each phase we need to simulate that the user has changed or added additional
                content to the database. In that case, the test harness pattern calls for multiple seeding events each of
                which will enrich the database at different times from data in different folders. For example,
                a folder "SEED@T0" would be used for an initial seeding at the start of the test,
                then "SEED@T1" for content that must be used to enrich the database in a subsequent phase 1, then
                "SEED@T2" for a subsequent phase 2, etc. Each seeding event should use a different AcceptanceTestContext
                object
        '''
        self.scenario_id                                            = scenario_id
        self.manifest                                               = manifest
        self.current_snapshot_id                                    = None

        # Notes will be aggregated throughout the test case
        self.notes                                                  = notes

        # This will be set by self.initialize_database(-)
        self.seeding_round                                          = seeding_round
        self.test_database                                          = None

        Application.app().log("--------- Starting Test Scenario " + str(scenario_id) 
                              + " [round=" + str(seeding_round) + "] ---------", 
                              log_level                             = Logger.LEVEL_INFO,
                              stack_level_increase                  = 2)

        
        self.initialize_database() 
                      

    @abc.abstractmethod
    def initialize_database(self):
        '''
        Constructs an instance of a TestDatabase concrete class and sets it as the value of self.test_database

        @param spec A ScenarioSpec object used to create the TestDatabase object created by this method.
        '''
    def __enter__(self):
        '''
        Returns self
        
        Intention is that this context manager is used by a specific
        test case method to surround the business logic it runs, and that business logic should be run against
        the TestDatabase returned by this method.
        '''
        if self.seeding_round == 0:
            self.test_database.populate_from_seed()
        else:
            self.test_database.enrich_from_seed(self.seeding_round)

        return                                                      self

    def __exit__(self, exc_type, exc_value, exc_tb):

        # Save the notes
        self.notes.save_notes(path_to_scenario=self.manifest.path_to_scenario())

        ''' TODO - figure out if we want to handle some types of exceptions
        if isinstance(exc_value, IndeExError):
            # Handle IndexError here...
            print(f"An exception occurred in your with block: {exc_type}")
            print(f"Exception message: {exc_value}")
            return True
        '''