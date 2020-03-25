import xml.etree.ElementTree as ET

class Xml:
    def __init__(self, file=None, text=None):
        if file:
            tree = ET.parse(file)
        elif text:
            tree = ET.fromstring(text)
        else:
            return
        self.root = tree.getroot()

    def getTagsFromRoot(self, name):
        return self.root.findall('.//'+name)

    def getTagFromRoot(self, name):
        return self.root.find('.//'+name)

    def getTagsFromTag(self, name, tag):
        return tag.findall(name)

    def getTagFromTag(self, name, tag):
        return tag.find(name)

    def getValueFromRoot(self, name):
        return self.getValueInTag(self.getTagFromRoot(name)) 

    def getValueInTag(self, tag):
        if tag is None:
            return None
        return tag.text