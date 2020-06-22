import fiona
import json

class Shape:

    def __init__(self, filename):
        self.filename = filename
    
    def getRecordByFieldName(self, fieldName: str):
        values = []
        with fiona.open(self.filename) as f:
            self.records = f.values()
            for record in self.records:
                values.append(record['properties'][fieldName])
        return values

    