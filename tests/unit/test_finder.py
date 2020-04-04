import unittest
import os

from pycroaktools.files import Finder

class TestFinder(unittest.TestCase):

    test_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/test_finder/testFolder')
    test_zip = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/test_finder/myzip.zip')

    def _recursiveFindFolders(self, properties):
        finder = Finder(properties)
        return finder.recursiveFindFolders()

    def test_recursiveFindFolders(self):
        properties = {'parent': self.test_folder, 'regex': r'.*1$'}
        results = self._recursiveFindFolders(properties)
        self.assertEqual(len(results), 1)
        self.assertEqual(os.path.basename(results[0]), 'folder1')

    def _recursiveFindFiles(self, properties):
        finder = Finder(properties)
        return finder.recursiveFindFiles()

    def test_recursiveFindFiles(self):
        """
        Test that it can retrieve 1 specific file
        """
        properties = {'parent': self.test_folder, 'regex': r't.+t1\.txt$', }
        results = self._recursiveFindFiles(properties)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(os.path.basename(results[0]), 'test1.txt')

    def _recursiveFindFilesInZip(self, properties):
        finder = Finder(properties)
        return finder.recursiveFindFilesInZip()

    def test_recursiveFindFilesInZip(self):
        """
        Test that it can retrieve 1 specific file in zip file
        """
        properties = {'parent': self.test_zip, 'regex': r'.+level2\.txt$'}
        results = self._recursiveFindFilesInZip(properties)
        self.assertEqual(len(results), 1)
        self.assertEqual(os.path.basename(results[0]), 'mytextinlevel2.txt')

    if __name__ == '__main__':
        unittest.main()
