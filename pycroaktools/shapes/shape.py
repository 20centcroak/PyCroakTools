# from fiona import open as fionaopen
# import json

import shapefile


class Shape:
    
    def getRecordByFieldName(self, filename: str, fieldName: str):
        # values = []
        # with fionaopen(filename) as f:
        #     records = f.values()
        #     for record in records:
        #         values.append(record['properties'][fieldName])
        # return values
        shape = shapefile.Reader(filename)
        records = shape.records()
        #first feature of the shapefile
        names = [x[0] for x in records]
        return names
        # records = shape.records()
        # for record in records:
        #     print(record)
        # feature = shape.shapeRecords()[0]
        # first = feature.shape. 
        # print(first)

    