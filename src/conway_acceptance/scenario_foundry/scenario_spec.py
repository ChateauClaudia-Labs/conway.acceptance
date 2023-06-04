import abc


class ScenarioSpec(abc.ABC):

    def __init__(self, scenario_id):
        '''
        This is a datastructure class, used to hold the specification for a testing database that is to be created
        by a concrete class extending the TestDataFactory. 

        @param scenario_id An integer that serves as the unique identifier for the scenario for which this is a
            a specification. A YAML file that maps such numerical ids to the classname of the code that implements
            a test scenario can be found in `scenarios_root_folder/ScenarioIds.yaml`
        '''
        self.scenario_id                            = scenario_id

    
    