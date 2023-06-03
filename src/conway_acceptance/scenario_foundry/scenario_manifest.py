import abc

from conway.database.database_manifest                 import DataBaseManifest

from conway_acceptance.util.test_statics                           import TestStatics

class ScenarioManifest(DataBaseManifest):

    def __init__(self, scenarios_root_folder, scenario_id):
        '''
        This is a datastructure class, used to hold the some metadata about a test scenario after it has already
        been created by the ScenarioGenerator (recall that a "scenario" is really a special kind of folder structure
        in the file system containing all inputs and outputs for a test case. In other words, a "scenario" is not
        the code for a test case; that would be the "test logic").
    
        Thus, this class does not hold enough information to create a test scenario - to generate test scenarios
        the class that contains how to do it is the ScenarioSpec, not this ScenarioManifest. Thus, a ScenarioManifest
        can be thought of like a "subset" of the information in a ScenarioSpec. 
        In terms of lifecycle, one can think of the ScenarioSpec as an object that plays a role before a scenario
        is created, and its user is the ScenarioGenerator. By contract, the ScenarioManifest plays a role after a scenario
        is generated, and is used by other classes like TestDatabase and AcceptanceTestContext in order for them to 
        contain "connection strings"  to the right scenario.
 
        @param scenarios_root_folder A string representing the absolute path to a folder which serves as the root
            for all test databases across all test scenarios. The test database for which this is a specification
            will be created in `scenarios_root_folder/scenario/`
        @param scenario_id An integer that serves as the unique identifier for the scenario for which this is a
            a specification. A YAML file that maps such numerical ids to the classname of the code that implements
            a test scenario can be found in `scenarios_root_folder/ScenarioIds.yaml`
        '''
        super().__init__()

        self.scenarios_root_folder                  = scenarios_root_folder
        self.scenario_id                            = scenario_id

    def path_to_seed(self, seeding_round=0):
        '''
        Returns the full path to the folder where the "seed" for the scenario resides, i.e., the content with which
        to initialize a new test database for this scenario.

        @param seeding_round An int, designating the round fo seeding for which we seek the path.
                By default it is 0, so it returns a path to a folder called "SEED@T0". For some test cases that is the
                only seeding event in the lifecycle of the test, but other test cases require multiple phases where
                at each phase we need to simulate that the user has changed or added additional
                content to the database. In that case, the test harness pattern calls for multiple seeding events each of
                which will enrich the database at different times from data in different folders. For example,
                a folder "SEED@T0" would be used for an initial seeding at the start of the test,
                then "SEED@T1" for content that must be used to enrich the database in a subsequent phase 1, then
                "SEED@T2" for a subsequent phase 2, etc.

        '''
        snapshot_timestamp                          = TestStatics.TEST_DB_SNAPSHOT_PREFIX + str(seeding_round)

        seed_folder                                 = self.path_to_scenario() + "/" + TestStatics.SEED_FOLDER + "@" + snapshot_timestamp
        return seed_folder
    
    def path_to_actuals(self, snapshot_count=None):
        '''`
        Returns the absolute path to the ACTUALS database. If `snapshot_count` is None than it returns the
        path to ACTUALS@latest; otherwwise the path to ACTUALS@T{snapshot_count}

        @param snapshot_count An int, designating the snapshot of the test database for which we seek the
                root. It may be None.
        '''
        return self._path_to_test_db(db_type=TestStatics.TEST_DATABASE_ACTUALS, snapshot_count=snapshot_count)
    
    def path_to_expected(self, snapshot_count=None):
        '''
        Returns the absolute path to the EXPECTED database. If `snapshot_count` is None than it returns the
        path to EXPECTED@latest; otherwwise the path to EXPECTED@T{snapshot_count}

        @param snapshot_count An int, designating the snapshot of the test database for which we seek the
                root. It may be None.
        '''
        return self._path_to_test_db(db_type=TestStatics.TEST_DATABASE_EXPECTED, snapshot_count=snapshot_count)
    
    def path_to_notes(self):
        '''
        '''
        notes_folder                                            = self.path_to_scenario() + "/" + TestStatics.RUN_NOTES
        return notes_folder

    def _path_to_test_db(self, db_type, snapshot_count=None):
        '''

        @param db_type A string, which must be either TestStatics.TEST_DATABASE_ACTUALS or 
                    TestStatics.TEST_DATABASE_EXPECTED

        @param snapshot_count An int, which is None by default. If None, then we return the path to the 
            "live" snapshot of the database, something like "ACTUALS@LATEST" or "EXPECTED@LATEST".
            If `snaphot_count` is not None and has a value like, say 2, then we return a path to the snapshot
            at folder "ACTUALS@T2", for example.
        '''
        if not db_type in [TestStatics.TEST_DATABASE_ACTUALS, TestStatics.TEST_DATABASE_EXPECTED]:
            raise ValueError("Invalid test database type '" + str(db_type) + "': should be one of '"
                             +  TestStatics.TEST_DATABASE_ACTUALS + "' or '" + TestStatics.TEST_DATABASE_EXPECTED + "'")
        if snapshot_count is None:
            snapshot_timestamp                      = TestStatics.TEST_DB_SNAPSHOT_LATEST
        else:
            snapshot_timestamp                      = TestStatics.TEST_DB_SNAPSHOT_PREFIX + str(snapshot_count)

        db_root                                     = self.path_to_scenario() + "/" + db_type + "@" + snapshot_timestamp
        return db_root
    
    def path_to_scenario(self):
        '''
        '''
        return self.scenarios_root_folder + "/" + str(self.scenario_id)