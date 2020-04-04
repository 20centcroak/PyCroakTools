import unittest
import os
import pandas as pd

from pycroaktools.workflow import Workflow
from pycroaktools.workflow import Step


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
            nextSteps = [step.stepId for step in step.getNexts()]
            previousSteps = [step.stepId for step in step.getPreviouses()]
            self.assertEqual(len(set(nextSteps) & set(nexts[step.stepId])), len(nexts[step.stepId]))
            self.assertEqual(len(set(previousSteps) & set(previouses[step.stepId])), len(previouses[step.stepId]))

    def test_noTitle(self):
        
        stepId =[1,2,3,4]
        nexts = [2,3,4,None]
        data = pd.DataFrame({'stepId':stepId, 'nexts':nexts})

        workflow = Workflow(data, 'myWorkflow')
        paths = workflow.getAllPaths()
        self.assertEqual(len(paths), 1)
        steps = workflow.getSteps()

        nexts = {1:[2], 2:[3], 3:[4], 4:[]}
        previouses = {1:[], 2:[1], 3:[2], 4:[3]}

        for index, step in enumerate(steps):
            nextSteps = [step.stepId for step in step.getNexts()]
            previousSteps = [step.stepId for step in step.getPreviouses()]
            self.assertEquals('step '+str(index+1), step.title)
            self.assertEqual(len(set(nextSteps) & set(nexts[step.stepId])), len(nexts[step.stepId]))
            self.assertEqual(len(set(previousSteps) & set(previouses[step.stepId])), len(previouses[step.stepId]))

    