import os                                                                   as _os

from conway_acceptance.util.test_statics                                   import TestStatics

class AcceptanceTestNotes():

    def __init__(self, notes_filename, notes_timestamp):
        '''
        Helper class that represents observations that the test case makes in the course of its execution.
        There normally is an instance of this object for each run of each test case, and they are saved in the
        in the test case's scenario folder, in a subfolder whose name is given by the static variable
        TestStatics.RUN_NOTES
        '''
        self.notes_filename                                     = notes_filename
        self.notes_timestamp                                    = notes_timestamp
        self.notes_l                                            = []

    def add_line(self, line):
        '''
        @param line A string, that should be added as a new line to this notes object.
        '''
        self.notes_l.append(line)

    def add_multiple_lines(self, multiple_lines):
        '''
        @param multiple_lines A list of strings, each of which should be added as a separate line to this notes object.
        '''
        self.notes_l.extend(multiple_lines)


    def save_notes(self, path_to_scenario):
        '''
        '''
        notes_folder                                            = path_to_scenario + "/" + TestStatics.RUN_NOTES

        FILE                                                    = self.notes_timestamp + " " + self.notes_filename + ".txt"

        _os.makedirs(notes_folder, exist_ok=True)
        with open(notes_folder + "/" + FILE, 'w') as writer:
            for line in self.notes_l:
                writer.write(line + "\n")
