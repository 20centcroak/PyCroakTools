import unittest
import os
import pandas as pd

from pycroaktools.workflow.workflow import Workflow
from pycroaktools.workflow.step import Step


class TestWorkflow(unittest.TestCase):

    test_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/test_workflow')

    def test_workflow(self):
        data = pd.read_csv(os.path.join(self.test_folder, 'workflow.csv'))
        workflow = Workflow(data, 'myWorkflow')
        paths = workflow.getAllPaths()
        self.assertEqual(len(paths), 4)
        steps = workflow.getSteps()

        nexts = {1:[2,3], 2:[4], 3:[12], 4:[], 12:[], 9:[4,12]}
        previouses = {1:[], 2:[1], 3:[1], 4:[2,9], 12:[3,9], 9:[]}

        for step in steps:
            nextSteps = [step.id for step in step.getNexts()]
            previousSteps = [step.id for step in step.getPreviouses()]
            self.assertEqual(len(set(nextSteps) & set(nexts[step.id])), len(nexts[step.id]))
            self.assertEqual(len(set(previousSteps) & set(previouses[step.id])), len(previouses[step.id]))

    