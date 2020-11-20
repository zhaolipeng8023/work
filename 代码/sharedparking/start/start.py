
import unittest
from HTMLTestRunner_cn import HTMLTestRunner
from woniutestV1.tools.util import FileUtil


class Start:

    def start(self, path):

        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        test_class_info = FileUtil.get_txt(path)
        print(test_class_info)
        tests = loader.loadTestsFromNames(test_class_info)
        suite.addTests(tests)

        with open('report.html', 'w') as file:
            runner = HTMLTestRunner(stream=file, verbosity=2)
            runner.run(suite)


if __name__ == '__main__':
    Start().start('..\\conf\\case_class_path.conf')