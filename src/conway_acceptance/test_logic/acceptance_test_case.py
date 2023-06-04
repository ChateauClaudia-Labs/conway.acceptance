import abc
import os                                                                       as _os
from pathlib                                                                    import Path
import pandas                                                                   as _pd
import datetime                                                                 as _datetime
import re                                                                       as _re

import unittest

from conway.database.data_accessor                                 import DataAccessor
from conway.util.path_utils                                        import PathUtils
from conway.application.application                                import Application
from conway.observability.logger                                   import Logger


# GOTCHA
#
# Multiple inheritance is not ideal, and here we use it only in a "soft way". The "real parent class" for us is
# unittest.TestCase, and abc.ABC we only use as a way to tag some methods as abstract.
#
# Since Python does support multiple inheritance, this is allowed, but Python also has method resolution order (MRO)
# semantics whereby if there are multiple parent classes and a parent class's method is called, it will first try to
# match a method signature in the parent that was declared first (when reading left to right)
# 
# So it is essential that we put the unittest.TestCase parent *before* the abc.ABC parent in the declaration.
#
class AcceptanceTestCase(unittest.TestCase, abc.ABC): 

    def setUp(self):
        '''
        '''
        super().setUp()

        #self.assertTrue(False, msg="\n\n************** in setup for scenariod=" )#+ str(self.scenario_id) + "\n\n")

        self.spec                                                   = None # TODO - derived class should set it

        # Timestamp used to identify this run. A use case is to prefix all the notes created by the test case's
        # AcceptanceTestContext with this timestamp prefix. 
        # Example value: 
        #               "230409.070219" means: April 9, 2023 at 7:02 am and 19 seconds
        self.run_timestamp                                          = _datetime.datetime.now().strftime("%y%m%d.%H%M%S")


    def tearDown(self):
        '''
        '''
        super().tearDown()

    def round_msg(self, ctx):
        '''
        '''
        msg                                                         = "Round #" + str(ctx.seeding_round)
        return msg

    def assert_database_structure(self, ctx, excels_to_compare, snapshot_count=None):
        '''
        Checks if the ACTUALS@latest database has exactly the same files and folders as EXPECTED@latest.

        This is a "deep check" - validates filenames and their contents.

        @param ctx An AcceptanceTestContext object corresponding to the context manager object within which
                this test case is running at the time that this method is invoked.

        @param excels_to_compare An ExcelsToCompare object, containing the information on which Excel files
                must be compared as part of the assertion.

        '''
        actuals_root                                                = ctx.manifest.path_to_actuals()
        expected_root                                               = ctx.manifest.path_to_expected(snapshot_count)

        actuals_files                                               = self._get_files(root_folder = actuals_root)
        expected_files                                              = self._get_files(root_folder = expected_root)

        extra_files                                                 = [f for f in actuals_files if not f in expected_files]
        missing_files                                               = [f for f in expected_files if not f in actuals_files]
        difference_message                                          = "Database contents don't match expectations."  \
                                                                        + "\n\nNOT EXPECTED:\n\t" + "\n\t".join(extra_files) \
                                                                        + "\n\nMISSING:\n\t" + "\n\t".join(missing_files) 
        
        #ctx.notes.add_line("\n---------------- ACTUAL " + self.round_msg(ctx) + "--------------\n")
        ctx.notes.add_line("\n---------------- ACTUAL ; snapshot = " + str(snapshot_count) + "--------------\n")
        ctx.notes.add_multiple_lines(actuals_files)
        #ctx.notes.add_line("\n---------------- EXPECTED " + self.round_msg(ctx) + "--------------\n")
        ctx.notes.add_line("\n---------------- EXPECTED ; snapshot = " + str(snapshot_count) + "--------------\n")
        ctx.notes.add_multiple_lines(expected_files)

        self.assertEqual(actuals_files, expected_files, msg=difference_message)

        self._compare_dataframes(ctx, excels_to_compare, snapshot_count)

    def _compare_dataframes(self, ctx, excels_to_compare, snapshot_count):
        '''

        Verifies (i.e., asserts) equality of each database in the list `files_to_compare`

        @param ctx An AcceptanceTestContext object corresponding to the context manager object within which
                this test case is running at the time that this method is invoked.

        @param excels_to_compare An ExcelsToCompare object, containing the information on which Excel files
                must be compared as part of the assertion.
        '''
        ctx.notes.add_line("\n---------------- Comparing dataframes " + self.round_msg(ctx) + "--------------\n")

        actuals_root                                                = ctx.manifest.path_to_actuals()
        expected_root                                               = ctx.manifest.path_to_expected(snapshot_count)


        for relative_excel_path in excels_to_compare.relative_paths():
            for sheet_info in excels_to_compare.worksheets_info(relative_excel_path):
                sheet                                               = sheet_info.worksheet_name
    
                with DataAccessor(actuals_root + "/" + relative_excel_path, subpath = sheet) as ax:
                    actual_df                                       = ax.retrieve()
                with DataAccessor(expected_root + "/" + relative_excel_path, subpath = sheet) as ax:
                    expected_df                                     = ax.retrieve()

                if actual_df is None or expected_df is None:
                    if sheet_info.is_optional == True:
                        # In this case, the worksheet is missing but it is optional, so that's OK. 
                        # Just skip it and move on to the next sheet
                        continue
                    else:
                        raise ValueError("Worksheet '" + sheet + "' missing in '" + relative_excel_path + "'")


                # We do 3 rounds to compare the two DataFrames, and each of them would be an assertion failure
                #   1. do they contain the same row indices? 
                #   2. do they contain the same columns?
                #   3. if they are of the same shape & labels, are the cells actually equal?
                FILE_EXTENSION                                      = ".xlsx"
                relative_path_no_file_extension                     = relative_excel_path.replace(FILE_EXTENSION, "")
                df_description                                      = relative_path_no_file_extension + "[" + sheet + "]" + FILE_EXTENSION

                def _add_note_on_differences(actual_labels, expected_labels):
                    missing_s                                       =set(expected_labels).difference(set(actual_labels))
                    unexpected_s                                    =set(actual_labels).difference(set(expected_labels))
                    ctx.notes.add_line("\t\tMISSING in ACTUAL: [" + ", ".join([str(label) for label in missing_s]) + "]")
                    ctx.notes.add_line("\t\tUNEXPECTED in ACTUAL: [" + ", ".join([str(label) for label in unexpected_s]) + "]")
                def _compare_labels(label_type, actual_labels, expected_labels):
                    failure_message                                 = ''
                    if list(actual_labels) != list(expected_labels): # GOTCHA: Convert to list or comparator fails saying its ambiguous
                        failure_message                             = "ACTUAL " + label_type + " don't match EXPECTED's:" + df_description
                        ctx.notes.add_line("\t" + failure_message)
                        _add_note_on_differences(actual_labels, expected_labels)
                    # GOTCHA: Convert to list or comparator fails saying its ambiguous
                    actual_sorted                                   = list(actual_labels)
                    expected_sorted                                 = list(expected_labels)
                    self.assertEqual(actual_sorted, expected_sorted, failure_message) 
                    

                # Check 1: are the row indices the same?
                _compare_labels("row labels", actual_df.index, expected_df.index)

                # Check #2: are the columns the same?
                _compare_labels("columns", actual_df.columns, expected_df.columns)

                # Check #3: are the cell values the same?
                differences_df                                      = actual_df.compare(expected_df)

                expected_size                                       = len(expected_df.index)
                difference_size                                     = len(differences_df.index)

                ctx.notes.add_line("\t" + str(difference_size) + "/" + str(expected_size) + " ERRORS in " + df_description)

                difference_message                                  = "ACTUAL doesn't match EXPECTED:" + df_description

                if difference_size!=0:
                    # Save the differences, to support debugging
                    notes_folder                                    = ctx.manifest.path_to_notes()
                    
                    DIFF_FILENAME                                   = self.run_timestamp + " DIFFERENCES/" + df_description
                    DIFF_FILENAME                                   = PathUtils().clean_path(DIFF_FILENAME)
                    DIFF_FOLDER                                     = _os.path.dirname(DIFF_FILENAME)
                    Path(notes_folder + "/" +DIFF_FOLDER).mkdir(parents=True, exist_ok=True)
                    differences_df.to_excel(notes_folder + "/" + DIFF_FILENAME)

                self.assertTrue(difference_size==0, difference_message)

    def _get_files(self, root_folder):
        '''
        Returns a list of strings, listing all the filenames under the `root_folder`
        Each filename is a relative path relative to the `root_folder`, and the returned list of filenames is sorted.

        @param root_folder A string representing the root of a folder structure
        '''
        files_l                                                     = []
        walker                                                      = _os.walk(root_folder)
        for path, folders, files in walker:
            relative_path                                           = path.replace(root_folder, "")
            for f in files:
                # Cleanup a bit some "pollution" in the paths with the delimeters "\" and "/", so that we get Unix-style paths
                relative_filename                                   = relative_path + "/" + f
                #relative_filename                                   = relative_filename.replace("\\", "/").replace("//", "/")
                relative_filename                                   = PathUtils().clean_path(relative_filename)
                files_l.append(relative_filename)
        files_l                                                     = sorted(files_l)
        
        return files_l



