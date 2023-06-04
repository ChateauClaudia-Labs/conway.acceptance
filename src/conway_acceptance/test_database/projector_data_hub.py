from conway.database.single_root_data_hub                      import SingleRootDataHub, DataHubHandle

class Projector_DataHub(SingleRootDataHub):

    def __init__(self, name, hub_handle: DataHubHandle):
        '''
        DataHub abstraction representing the folder structure from which the Projector reads the external
        data from which to generate a database.That "external data" consists of two folders:

        * One represents the `input_db`

        * The other represents the `ouput_db`

        We treat each as a DataHub, and two instances of this class are used to represent those two areas.

        :param DataHubHandle hub_handle: Handle to the folder under which this DataHub resides.
        '''
        super().__init__(name, hub_handle)

    def _instantiate(self, name, hub_handle):

        return Projector_DataHub(self.name, name, hub_handle)

