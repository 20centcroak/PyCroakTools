import yaml
import logging
import os
import time
import sys

class Configuration:

    def default(self, file):
        self.defaultLogger(file)
        return self.appConfig(file)

    def appConfig(self, filename):
        try:            
            with open(filename) as file:
                logging.info('config {} loaded'.format(filename))
                return yaml.safe_load(file)
        except FileNotFoundError:
            logging.info('file {} not found, no config loaded'.format(filename))
            return

    def defaultLogger(self, filename):
        dirName = 'logs/'+os.path.basename(filename)
        if not os.path.exists(dirName):
            os.makedirs(dirName)

        filename = os.path.join(dirName, str(time.time())+'.log')
        logging.basicConfig(filename=filename)    
        
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)d - %(message)s')
        consoleHandler.setFormatter(formatter)
        root.addHandler(consoleHandler)