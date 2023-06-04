import abc

class ScenarioGenerator(abc.ABC):

    def __init__(self, spec):
        '''
        This class provides functionality to create the "scenario" required by a test case, where the notion of "scenario"
        has a specific meaning in the domain model of the `conway_acceptance` module. We refer the user to the
        README.md of that module for an explanation.


        @param spec A ScenarioSpec object, representing the specification for how to seed the test database to be created.
        '''
        self.spec                                       = spec

    @abc.abstractmethod
    def create_scenario(self):
        '''
        '''
