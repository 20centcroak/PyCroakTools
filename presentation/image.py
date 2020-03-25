class Image:
    """
    The Image class defines the image details needed to display it in a presentation.
    """

    def __init__(self, id, title, filename, part=0, version=0):
        """
        Build the object.
        ---
        Parameters:
        - id: a unique integer. 2 slides can't have the same id, except if it is split.
        - title: arbitrary title
        - filename: absolute path to image file
        - part: [optional] float number. A Slide may be split in multiple parts. 
        In this case, they have the same id but a different part number. If not set, 0.0 is the default value.
        - version: [optional] float number. 
        A slide may have different versions, then a history may be managed (version 0 is older than version 1). If not set, 0.0 is the default value
        """
        self.id = id
        self.title = title
        self.filename = filename
        self.part = float(part)
        self.version = float(version)

    