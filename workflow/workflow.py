import logging
from pandas import DataFrame
import sys
from pycroaktools.workflow.step import Step
from pycroaktools.applauncher.configuration import Configuration

class Workflow:
    """
    The Workflow class manages a sequence, ie a list of steps which are linked together in a sequential way.  
    To define such a sequence, a pandas object should be supplied. This pandas object is defined with the columns named stepId, title and nexts.  
    stepId is the unique step identifier,  title is an arbitrary name of the step, nexts is a list of stepIds that follows the step. The list is given by stepIds separated with '-'  
    Here is an example:
    |stepId|title|nexts|
    |1|my first step|2-3|
    |2|my second step|4|
    |3|step 3!|12|
    |4|step4||
    |9|step9|12-4|
    |12|step12||
    In this example, steps 1 and 9 are the first steps in the workflow because the don't have any previous step.  
    Steps 4 and 12 are the last steps because they don't have any next step.  
    Step 1 points to 2 next steps: steps 2 and 3, step 2 points to step 4, ...
    Steps have to be defined with a unique identifier. This identifier must be an integer. 
    But, as we can see, there is no need to define a continuous suite and the identifiers don't need to be sorted. 
    """ 

    def __init__(self, workflow:DataFrame, name='workflow'):
        """
        builds the class according to the pandas definition of the workflow and optionally its name.
        Parameters
        ----------
        workflow: pandas object defined by the columns named stepId, title and nexts.
        stepId is the unique step identifier,  title is an arbitrary name of the step, nexts is a list of stepIds that follows the step. The list is given by stepIds separated with '-' .  

        """
        self.name = name
        """name of the workflow"""
        self.firstSteps = []
        """steps without previous steps"""
        self.steps = dict()
        """all steps as a dictionary. Key is the step id and value is a Step object"""
        self._build(workflow)
        self._findFirsts()
        self._order = self._getStepOrder()

    def _build(self, workflow):
        for index, stepId in enumerate(workflow['stepId']):
            try:
                stepId = int(stepId)
            except ValueError:
                Configuration().error('step id {} is not an integer'.format(stepId))
            step = Step(stepId)
            self.steps[stepId] = step

        for index, stepId in enumerate(workflow['stepId']):
            stepId = int(stepId)
            nexts = str(workflow['nexts'][index]).split('-')
            for nextStep in nexts:
                try:
                    nextStep = int(float(nextStep))
                except ValueError:
                    if not nextStep or nextStep == 'nan':
                        continue
                    Configuration().error('next value {} is not an integer'.format(nextStep))
                self.steps[stepId].addNext(self.steps[nextStep])

    def _findFirsts(self):
        for step in self.getSteps():
            previouses = step.getPreviouses()
            if not previouses:
                self.firstSteps.append(step)

    def getAllPaths(self):
        """returns all possible paths (list of steps) starting from first steps, going to next steps down to last steps."""
        return self.getDescending(self.firstSteps)

    def getDescending(self, steps):
        """returns descending sequences, starting from the given steps (list of Step objects), following the next steps down to the last steps."""
        paths = []
        for step in steps:
            self._addPath([], step, paths)
        return paths

    def _addPath(self, root, step, paths):
        path = [item for item in root]
        path.append(step)
        paths.append(path)

        while not step.isLast():

            if len(step.getNexts()) < 2:
                step = step.getNexts()[0]
                path.append(step)
            else:
                root = [item for item in path]
                for index, item in enumerate(step.getNexts()):
                    if index == 0:
                        step = item
                        path.append(step)
                    else:
                        self._addPath(root, item, paths)

    def getAscendings(self, step):
        """returns ascencding sequences, starting from the given step, following the previous steps up to the first steps."""
        paths = []
        self._addAscending([], step, paths)
        return paths

    def _addAscending(self, root, step, paths):
        path = [item for item in root]
        path.append(step)
        paths.append(path)

        while not step.isFirst():
            if len(step.getPreviouses()) < 2:
                step = step.getPreviouses()[0]
                path.append(step)
            else:
                root = [item for item in path]
                for index, item in enumerate(step.getPreviouses()):
                    if index == 0:
                        step = item
                        path.append(step)
                    else:
                        self._addAscending(root, item, paths)

    def printStatusPerStep(self):
        """prints with logging.info the step details for each step in the workflow"""
        logging.info('{} steps in workflow {}'.format(
            len(self.steps), self.name))
        for step in self.getSteps():
            nextString = ''
            for nextStep in step.getNexts():
                nextString += nextStep.id+', '
            nextString = nextString[:-2]
            previousString = ''
            for previousStep in step.getPreviouses():
                previousString += previousStep.id+', '
            previousString = previousString[:-2]
            logging.info('step {} has {} next ({}) and {} previous ({})'.format(step.id, len(
                step.getNexts()), nextString, len(step.getPreviouses()), previousString))

    def getSteps(self):
        """returns the list of all step objects in the workflow"""
        return list(self.steps.values())

    def _getStepOrder(self):
        stepNumberPerId = dict()
        stepNumber = 0
        for step in self.getSteps():
            if step.id in stepNumberPerId:
                continue
            stepNumberPerId[step.id] = stepNumber
            stepNumber += 1
        return stepNumberPerId

    def getLinksPerSteps(self):
        """returns a dictionary with keys= stepID and value = the value return by Workflow.getLinks(step) where step correspond to stepID"""
        links = dict()
        for step in self.getSteps():
            links[step.id] = self.getLinks(step)
        return links

    def getLinks(self, step:Step):
        """returns a dictionary with keys = next step id and values = index of the next step in the list returned by Workflow.getSteps()"""
        nextIds = [step.id for step in step.getNexts()]
        links = dict()
        for nextId in nextIds:
            links[nextId] = self._order[nextId]
        return links
