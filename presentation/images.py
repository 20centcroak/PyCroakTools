from pathlib import Path
from pycroaktools.presentation.slideGenerator import SlideGenerator
from pycroaktools.presentation.image import Image
import os
import re
import logging


class Images:
    """
    The Images class manages a catalog of Image that may be used by the Presentation object.
    The images are retrieved from a disk location if the image filenames are built as follow: id_title[_part][_version] with
        - title: arbitrary title
        - id: a unique integer. 2 slides can't have the same id, except if it is split.
        - part: [optional] float number. A Slide may be split in multiple parts. In this case, they have the same id but a different part number. If not set, 0.0 is the default value.
        - version: [optional] float number. A slide may have different versions, then a history may be managed (version 0 is older than version 1). If not set, 0.0 is the default value
    """
    def __init__(self, imageFolder: str):
        """
        Builds the object.
        Parameters:
        ---
        - imageFolder: folder that contains image files
        """
        self.images = dict()
        """
        dictionary with keys = image ids and values = version dictionary
        version dictionary has keys = version numbers and values = part dictionary
        part dictionary kas keys = part number and values = Image object
        """
        # self._catalog(imageFolder)

    # def _catalog(self, folder:str):
    #     path = Path(folder).rglob('*.*')
    #     files = [x for x in path if x.is_file()]
    #     for file in files:
    #         slide = SlideGenerator().fromFilename(file)
    #         if not slide:
    #             continue
    #         self._addImage(Image(slide.id, details['title'], file, details['part'], details['version']))

    # def _addImage(self, image:Image):
    #     if image.id not in self.images:
    #         self.images[image.id] = dict()
    #     if image.version not in self.images[image.id]:
    #         self.images[image.id][image.version] = dict()
    #     self.images[image.id][image.version][image.part] = image
