
class TestStatics():

    def __init__(self):
        '''
        Class of "enums", i.e., static string-value variables used throughout the test cases
        as a way to use consistent strings when they reference a named domain structural element.
        '''

    SEED_FOLDER                                                 = "SEED"

    # These are used to create the root folders of the test database used by the test cases.
    #   There are (possibly) several folders because a test case might create snapshots if its wants to check
    #   things along the way and preserve that state (so that, for example, we can later debug)
    #
    #   For that reason, each test case may use multiple test database snapshots:
    #
    #   * actuals@latest is always the live, latest test database. Here is where the application's business logic is reading/writing data
    #   * actuals@T1, actuals@T2, etc - these are snapshots created by the test harness if the test cases asks the test harness to remember 
    #                           data along the way
    TEST_DATABASE_ACTUALS                                       = "ACTUALS"
    TEST_DATABASE_EXPECTED                                      = "EXPECTED"
    TEST_DB_SNAPSHOT_LATEST                                     = "latest"
    TEST_DB_SNAPSHOT_PREFIX                                     = "T"    

    # This is a folder for datasets that are common across all scenarios. Typically this would be data that can be used
    # as inputs by the scenario foundry business logic (e.g., by the ScenarioGenerator logic) to create the seeds for 
    # test scenarios.
    GLOBAL_DATASETS_FOLDER                                      = "global_datasets"

    GLOBAL_DATASETS_HUB                                         = "GLOBAL_DATASETS_HUB"
    GENEARATED_SCENARIO_HUB                                     = "GENEARATED_SCENARIO_HUB"


    # Folder used to save some notes about the test run. Useful to verify what happened in the test and/or debug
    RUN_NOTES                                                   = "RUN_NOTES"

    # When testing the projector, we need to simulate input, output, and seed db's. We use this statics to 
    # to define their roots in VM_ProjectorTestContext
    #
    PROJECTOR_INPUT_DB_FOLDER                   = "projector_input_db"
    PROJECTOR_OUTPUT_DB_FOLDER                  = "projector_output_db"
    PROJECTOR_SEED_DB_FOLDER                    = "projector_seed_db"