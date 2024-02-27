import configparser

config= configparser.ConfigParser()

config.read('config.ini')

AZURE_OPENAI_API_KEY= config['OPENAI']['AZURE_OPENAI_API_KEY']
AZURE_OPENAI_ENDPOINT= config['OPENAI']['AZURE_OPENAI_ENDPOINT']