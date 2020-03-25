from pycroaktools.presentation.slides import Slides
import pandas as pd


class SlidesToWorkflow:
    """
    The SlidesToWorkflow class builds a pandas workflow definition based on a linear sequence of slide ids.
    If the slide ids are ordered in a sequence such as [1, 2, 5, 9], then a workflow is created with this sequence.
    Each step has 1 next (1->2), (2->5), (5->9). The slide title defines the step title.
    """

    def create(self, slides:Slides):
        """
        create a pandas workflow definition from a Slides object
        ---Parameters:
        - slides: Slides object used to create a pandas workflow definition
        """
        slideIds = []
        slideTitles = []
        for slideId in slides.slides:
            slideIds.append(slideId)
            slideTitle = next(iter(slides.getSlide(
                slideId, slides.getHighestVersion())))
            slideTitles.append(slideTitle)

        sortedIds = sorted(slideIds)
        nexts = [sortedIds[index+1]
                 for index, id in enumerate(sortedIds) if index < len(sortedIds)-1]
        if len(nexts) < len(slideIds):
            nexts.append('')

        df = pd.DataFrame(
            {'stepId': slideIds, 'title': slideTitles, 'nexts': nexts})
        df.sort_values(by=['stepId'])
        return df
