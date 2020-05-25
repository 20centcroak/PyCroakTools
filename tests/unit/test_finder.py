import unittest
import os

from pycroaktools.files import Finder

class TestFinder(unittest.TestCase):

    test_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/test_finder/testFolder')
    test_zip = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/test_finder/myzip.zip')

    def _findFolders(self, properties):
        finder = Finder(properties)
        return finder.findFolders()

    def test_findFolders(self):
        properties = {'parent': self.test_folder, 'regex': r'.*1$'}
        results = self._findFolders(properties)
        self.assertEqual(len(results), 1)
        self.assertEqual(os.path.basename(results[0]), 'folder1')

    def _findFiles(self, properties):
        finder = Finder(properties)
        return finder.findFiles()

    def test_findFiles(self):
        """
        Test that it can retrieve 1 specific file
        """
        properties = {'parent': self.test_folder, 'regex': r't.+t1\.txt$', }
        results = self._findFiles(properties)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(os.path.basename(results[0]), 'test1.txt')

    def _findFilesInZip(self, properties):
        finder = Finder(properties)
        return finder.findFilesInZip()

    def test_findFilesInZip(self):
        """
        Test that it can retrieve 1 specific file in zip file
        """
        properties = {'parent': self.test_zip, 'regex': r'.+level2\.txt$'}
        results = self._findFilesInZip(properties)
        self.assertEqual(len(results), 1)
        self.assertEqual(os.path.basename(results[0]), 'mytextinlevel2.txt')

    if __name__ == '__main__':
        unittest.main()
