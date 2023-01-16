from configparser import ConfigParser
from distutils.command.config import config

config = ConfigParser()
# config.sections()
config.add_section('ID')
# config.set('ID', 'LOKASI', 'test bla')
config['ID']['LOKASI'] = "test 123"                                
                                                                
config.add_section('KARCIS')
config['KARCIS']['FOOTER1'] = "footer test 123"                                
# config['KARCIS']['FOOTER2'] = message['footer2']                                
# config['KARCIS']['FOOTER3'] = message['footer3']

with open('config.cfg', 'w') as configfile:
    config.write(configfile)