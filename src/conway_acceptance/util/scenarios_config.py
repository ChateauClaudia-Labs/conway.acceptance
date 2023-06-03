import yaml                                                                     as _yaml

# We cache the dictionaries for static configurations loaded from YAML files, so that we don't have to load
# each time we want to check out a field
_YAML_CACHE = {}

class ScenariosConfig():

    SCENARIOS_CONFIG_FILE                                       = "ScenarioIds.yaml"  

    SCENARIOS_IDS                                               = "scenario_ids"


    def __init__(self, scenarios_repo):
        '''
        '''
        self.scenarios_repo                                     = scenarios_repo
        self.scenarios_id_dict                                  = self._load_scenarios_id_config(scenarios_repo)

    def _load_scenarios_id_config(self, scenarios_repo):
        '''
        '''
        path                                                    = scenarios_repo + "/" + self.SCENARIOS_CONFIG_FILE

        if path in _YAML_CACHE.keys():
            scenarios_id_dict                                   = _YAML_CACHE[path]                 
        else:
            with open(path, 'r', encoding="UTF8") as file:
                scenarios_id_dict                               = _yaml.load(file, Loader=_yaml.FullLoader)
                _YAML_CACHE[path]                               = scenarios_id_dict

        return scenarios_id_dict
    
    def get_scenario_id(self, test_case_name):
        '''
        Returns an int, such as 1001, which serves as scenario id for the test case with name `test_case_name`

        @param test_case_name A string, such as "services.post_reports_governance", that identifies a test case.
        '''
        mappings_dict                                           = self.scenarios_id_dict[self.SCENARIOS_IDS]
        if test_case_name in mappings_dict.keys():
            return mappings_dict[test_case_name]
        else:
            return None