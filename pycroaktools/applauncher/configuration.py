from yaml import safe_load
import logging, os, time, sys


class Configuration:

    def __init__(self):
        self.defaultLogger()

    def default(self, file):        
        if not file:
            return
        fileyml = self.getYml(file)
        if not fileyml:
            logging.info('config file not found, no config loaded')
            return
        return self.appConfig(fileyml)


    def getYml(self, file):
        file = self.getCorrectExtension(file)
        if os.path.isfile(file):
            return file
        filepath, file_extension = os.path.splitext(file)
        filename = os.path.basename(filepath)
        current_directory = os.path.dirname(file)
        resource = os.path.join(current_directory, 'resources', filename, filename+file_extension)
        if os.path.isfile(resource):
            return resource
        
    def getCorrectExtension(self, file):
        filename, file_extension = os.path.splitext(file)
        if file_extension in ['yml', 'yaml']:
            return file
        return filename+'.yml'

    def appConfig(self, filename):
        try:
            with open(filename, encoding='utf8') as file:
                logging.info('config {} loaded'.format(filename))
                properties = safe_load(file)
                for key in properties:
                    logging.info('{}:{}'.format(key, properties[key]))
                return properties
        except FileNotFoundError:
            logging.info(
                'file {} not found, no config loaded'.format(filename))
            return

    def defaultLogger(self):
        root = logging.getLogger()
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')
        root.setLevel(logging.DEBUG)

        # console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)       
        console_handler.setFormatter(formatter)
        root.addHandler(console_handler)

        # file
        dirName = 'logs/'
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        filename = os.path.join(dirName, str(time.time())+'.log')
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)
        
