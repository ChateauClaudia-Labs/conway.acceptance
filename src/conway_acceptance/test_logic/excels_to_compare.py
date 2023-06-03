import abc

class ExcelsToCompare(abc.ABC):

    def __init__(self):
        '''
        Data structure class, aiming to offer a more concise ways for test cases to define what at the Excel
        files they want to compare.
        
        Specifically, it provides a service to record:

        * The Excel files to compare, where an Excel file is identified by its relative path. "Relative" here
          means with respect to the root of the test scenario area (i.e., an ACTUALS@<timestamp> or
          EXPECTED@<timestamp> folder)
        
        * For each such Excel file, this class records:

          * What worksheets it contains, that must be compared
          * Whether the existence of such worksheets in a given Excel are mandatory or optional. If mandatory
            (the default), then the test case will fail if the worksheet is missing in either the ACTUALS or EXPECTED
            output.
        
        '''
        self.excels_to_compare_dict                                 = {}

    def addXL(self, relative_path, worksheets_info_list):
        '''
        '''
        self.excels_to_compare_dict[relative_path]                  = worksheets_info_list

    def relative_paths(self):
        '''
        Returns an iterable object that lists the relative paths of all the Excel files that must be loaded
        '''
        return self.excels_to_compare_dict.keys()

    def worksheets_info(self, relative_path):
        '''
        Returns an iterable object that lists the WorksheetComparisonInfo for the Excel at the given relative path

        @param relative_path A string, representing the path of an Excel spreadsheet relative to the root of the 
                test scenario area (i.e., an ACTUALS@<timestamp> or EXPECTED@<timestamp> folder)
        '''
        info_list                                                   = self.excels_to_compare_dict[relative_path]
        return info_list


class WorksheetComparisonInfo():

    def __init__(self, worksheet_name, is_optional=False):
        '''
        Helper data structure class that holds some information about a worksheet in an Excel spreadsheet pertinent
        to the business logic of comparing if a test case's actual Excel files output matches the expected output.

        @param is_optional A boolean, which is False by default. If True, it indicates that the worksheet represented
            by this object may exist in the Excel spreadsheet in question, but is not mandatory.
        '''
        self.worksheet_name                                         = worksheet_name
        self.is_optional                                            = is_optional
