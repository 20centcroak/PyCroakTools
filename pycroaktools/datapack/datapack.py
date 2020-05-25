import re
import logging
from os.path import splitext
from math import ceil
from pandas import DataFrame, read_csv, read_excel, concat
from numpy import full


class DataPack:
    """The DataPack class manages data to be used in the app by offering basic methods to 
    manipulate and format data. It makes use of pandas to to do so.
    """

    def __init__(self, files: dict, dataprocessing: dict):
        """
        constructor: it defines the resource files and operations to apply on data. It is possible to chain processings by applying an operation on output data
        Parameters
        ----------
        files: resource files in a dictionary. Key id the file name used by dataprocessing to apply operation on the given file. The files are either csv or xls files
        dataprocessing: operation name and parameters. Examples: 

            processing: dataframe
            output: data1
            parameters:
                sep: '\s+' 
                skip: 1 
                file: file1

            processing: split
            output: table1
            parameters:
                cols: 2
                data: data1

            processing: replaceValues
            output: data2
            parameters:
                data: data2
                search: "YES"
                replace: X

            processing: fillna
            output: data2
            parameters:
                data: data2
                fillwith: ""
        """
        self.pack = dict()
        self.files = files

        switcher = {'dataframe': self.getDataFrame, 'fillna': self.fillna,
                    'split': self.splitDataFrame, 'replaceValues': self.replaceValues, 'table': self.formatDataframe}

        for processing in dataprocessing:
            self.pack[processing['output']] = switcher[processing['processing']](
                processing['parameters'])

    def getDataFrame(self, parameters: dict):
        sep = parameters['sep'] if 'sep' in parameters else ','
        skip = parameters['skip'] if 'skip' in parameters else None
        filename = parameters['file']
        file = self.files[filename]
        logging.info('retrieving data from {}'.format(file))
        _, extension = splitext(file)
        logging.info(extension)
        if extension in ['.xls', '.xlsx']:
            logging.info('read xls file')
            df = read_excel(file)
        else:
            logging.info('read csv file')
            df = read_csv(file, sep=sep,
                          skiprows=skip, header=None)

        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        return df

    def splitDataFrame(self, parameters: dict):
        data = self.pack[parameters['data']]
        cols = parameters['cols']
        nb_of_rows = len(data)
        nb_per_row = ceil(nb_of_rows/cols)

        series = []

        for col in range(0, cols):
            min_range = col*nb_per_row
            max_range = min(min_range+nb_per_row-1, nb_of_rows-1)
            df = data.loc[min_range:max_range]
            df = df.reset_index(drop=True)
            series.append(df)

        return concat(series, axis=1)

    def replaceValues(self, parameters: dict):
        return self.pack[parameters['data']].replace(parameters['search'], parameters['replace'])

    def formatDataframe(self, parameters: dict):
        descriptions = self.formatDescription(parameters['cols'])
        datacols = []
        for description in descriptions:
            dataname = description['dataname']
            filecol = description['colindex']
            datacols.append(self.pack[dataname].loc[:, filecol])

        df = concat(datacols, axis=1)
        df = df.fillna("")
        df.columns = range(0, df.shape[1])
        return df

    def formatDescription(self, cols):
        coldescriptions = []
        for col in cols:
            patterns = re.search(r'(.*)\[([0-9]+)\]', col)
            filename = patterns.group(1)
            colindex = int(patterns.group(2))
            coldescriptions.append(
                {'dataname': filename, 'colindex': colindex})
        return coldescriptions

    def fillna(self, parameters: dict):
        return self.pack[parameters['data']].fillna(parameters['fillwith'])
