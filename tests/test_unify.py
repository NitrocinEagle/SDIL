import configparser
import unittest
import os

from main import unify_data


class TestDataUnify(unittest.TestCase):
    def setUp(self):
        self.config_name = 'test_config.ini'
        config = configparser.ConfigParser()
        config.read(self.config_name)
        self.unified_folder = config['main']['unified_folder']
        self.unified_filename = config['main']['unified_filename']

    def test_unify(self):
        unify_data(self.config_name)

        with open(os.path.join(self.unified_folder, self.unified_filename), 'r', encoding='UTF8') as f:
            test_result = f.read().split('\n')

        with open(os.path.join('test_results', 'bank.csv'), 'r', encoding='UTF8') as f:
            test_assert_result = f.read().split('\n')

        for result, assert_result in zip(test_result, test_assert_result):
            if result != assert_result:
                assert False

        assert True


if __name__ == "__main__":
    unittest.main()
