# Testing approach of conway_acceptance module


NEED TO EXPLAIN DIFFERENCE BETWEEN:
* test case (the code logic) vs scenario (a folder with a test database, an input area, and possibly snapshot areas)

(TO BE RE_WRITTEN)
        Each test method in an AcceptanceTestCase class corresponds to a test scenario, which implies some state specific
        to that test case, such as:

        * scenario_id, such as 1123, which identifies the location of a test database, containing the Excel files that are
            meant to be inputs to the business logic being tested, as well as other Excel files representing the expected
            output of the business logic being tested

        * current_snapshot_id as the test case execution traverses across multiple "snapshots". A "snapshot" is a concept
            in the `conway_acceptance` model that applies to a test database. As a test case's execution progresses, it
            creates data (Excel files, typically) which are saved to the test database. Some test cases may want to snapshot
            a version of that evolving database output at various milestones in the execution of the test case, to make
            it possible for the test case to assert that the output matches the expected output in an incremental way.
            That makes the test case more transparent: if it fails half-way through its execution, then the snapshot for
            the processing phase at which the test case failed can more easily help understand why the failure took place.

# Sharing this project in development

To make this Python module visible, do:

`pip install -e .`