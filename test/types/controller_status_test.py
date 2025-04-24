import unittest
from plico_io.controller_types.controller_status import DriveStatus
from plico_motor.client.snapshot_entry import SnapshotEntry


class Test(unittest.TestCase):

    def setUp(self):
        self.ms = DriveStatus(
            'pippo',
            )

    def test_as_dict(self):
        self.ms.set_on(True)  
        got = self.ms.as_dict()
        self.assertCountEqual(got['name'], 'pippo')
        self.assertCountEqual(got['is_on'], True)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
