import logging
import os
import pandas as pd
from distutils.dir_util import copy_tree
from pycroaktools.applauncher.settings import Settings
from pycroaktools.presentation.images import Images
from pycroaktools.presentation.slides import Slides
from pycroaktools.workflow.workflow import Workflow
from pycroaktools.workflow.flowchart import Flowchart
from pycroaktools.easyPresentation.slidesToWorkflow import SlidesToWorkflow
from pycroaktools.easyPresentation.workflowToPresentation import WorkflowToPresentation


class Generator(Settings):
    """
    The Generator class generates presentations either based on a workflow, on a list of images, a list of markdown slides or all together.
    It inherits from pycroaktools.applauncher.settings.Settings that manages the settings.
    """

    def __init__(self, settings: dict):
        """
        builds the class according to the settings dictionary.
        Parameters
        ----------
        settings : dictionary that may contain the following key and values

        - slideFolder: folder that contains markdown files. 
        These files define either a slide thanks to their name or thanks to their header.
        See class Slides to get more details about the header.

        - imageFolder: folder that contains images. These images define either their own slide.
        If the image name complies with the slide definition (see class Slides) or may be called by a markdown file.

        - outputFolder: folder where the presentation is created. If none is provided, the current working directory
        (from where the app is launched) is used.

        - workflowFile: csv file defining the workflow. See class Workflow for a description of this csv file

        - createFlowchart: if True, a graphical representation of the workflow is generated

        - createLinearPresentations: if True, each possible path defined by the workflow generates an individual presentation. 
        Then Each slide has only one next slide. This is a linear sequence from first to last slide.

        - createWorkflowPresentation: if True, a unique presentation is generated to represent the workflow. Each slide may have multiple next slides. 
        Then links give choices to follow a path or another in the workflow
        """

        self.slideFolder = None
        self.imageFolder = None
        self.outputFolder = os.getcwd()
        self.workflowFile = None
        self.versions = [0.]
        self.createFlowchart = False
        self.createLinearPresentations = False
        self.createWorkflowPresentation = True        
        self.setProperties(settings)

        self._build()

    def _build(self):
        slides = self._manageSlides()
        self._manageImages(slides)
        workflow = self._manageWorkflow(slides)
        self._manageMissingSlides(slides, workflow)
        self._generate(workflow, slides)

    def _manageImages(self, slides: Slides):
        if not self.imageFolder:
            return
        slides.catalog(self.imageFolder, images=True)

    def _manageSlides(self):
        slides = Slides()
        if self.slideFolder:
            slides.catalog(self.slideFolder)
        else:
            self.slideFolder = os.path.join(self.outputFolder, 'slides')

        return slides

    def _manageWorkflow(self, slides: Slides):
        if self.workflowFile:
            return Workflow(pd.read_csv(
                self.workflowFile), os.path.basename(self.workflowFile)[:-4])

        return Workflow(SlidesToWorkflow().create(slides), 'presentation')

    def _manageMissingSlides(self, slides: Slides, workflow: Workflow):
        slides.createMissingSlides([step.id for step in workflow.getSteps()])

    def _generate(self, workflow: Workflow, slides: Slides):
        toPres = WorkflowToPresentation(
            workflow, slides, self.outputFolder)

        for version in self.versions:
            logging.info('version {} ...'.format(version))
            if self.createFlowchart:
                Flowchart(workflow).display()
            if self.createLinearPresentations:
                toPres.createLinearPresentations(version)
            if self.createWorkflowPresentation:
                toPres.createWorkflowPresentation(version)
