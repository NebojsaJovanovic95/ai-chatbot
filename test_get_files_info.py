import unittest
from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def setUp(self):
        self.working_dir = "calculator"

    def test_current_directory(self):
        print("Result for current directory:")
        result = get_files_info(self.working_dir, ".")
        print(result)

    def test_pkg_directory(self):
        print("Result for 'pkg' directory:")
        result = get_files_info(self.working_dir, "pkg")
        print(result)

    def test_bin_directory_outside(self):
        print('Result for "/bin" directory:')
        result = get_files_info(self.working_dir, "/bin")
        print(result)
    def test_parent_directory_outside(self):
        print('Result for "../" directory:')
        result = get_files_info(self.working_dir, "../")
        print(result)

if __name__ == "__main__":
    unittest.main()
