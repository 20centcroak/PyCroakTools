import logging, sys

def error(message):
    logging.error(message)
    input('press enter to quit')
    sys.exit(message)