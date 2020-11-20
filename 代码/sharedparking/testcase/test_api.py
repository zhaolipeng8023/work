import unittest

from sharedparking.tools.lib_util import APIUtil
from sharedparking.tools.util import FileUtil


class TestPtAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_lessor(self):
        test_info = FileUtil.get_test_info('..\\conf\\test_info.ini', 'lessor', 'lessor_info_api')
        APIUtil.assert_api(test_info)

    def test_pt(self):
        test_info = FileUtil.get_test_info('..\\conf\\test_info.ini', 'pt', 'pt_info_api')
        APIUtil.assert_api(test_info)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()