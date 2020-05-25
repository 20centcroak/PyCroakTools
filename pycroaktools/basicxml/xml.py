from xml.etree.ElementTree import parse, fromstring

class Xml:
    """
    The Xml class makes it easy tor retrieve values from a basic xml structure.
    """
    def __init__(self, file=None, text=None):
        """
        builds the object from either a file or a string (at least one should be supplied).
        """
        if file:
            tree = parse(file)
        elif text:
            tree = fromstring(text)
        else:
            return
        self.root = tree.getroot()

    def getTagsFromRoot(self, name):
        """find all tags with the given name"""
        return self.root.findall('.//'+name)

    def getTagFromRoot(self, name):
        """find the first occurence of the given name"""
        return self.root.find('.//'+name)

    def getTagsFromTag(self, name, tag):
        """find all tags with the given name under the given tag"""
        return tag.findall(name)

    def getTagFromTag(self, name, tag):
        """find the first occurence of the given name under the given tag"""
        return tag.find(name)

    def getValueFromRoot(self, name):
        """find the first occurence of the given tag name and returns its value"""
        return self.getValueInTag(self.getTagFromRoot(name)) 

    def getValueInTag(self, tag):
        """get value of the given tag"""
        if tag is None:
            return None
        return tag.text