import configparser
from pathlib import Path
from os import environ

env = environ

class ConfigError(Exception):
    def __init__(self, path):
        super(ConfigError, self).__init__(path)
        print(f'{str(path)} Not found')

def get_home_config_dir():
    return Path(Path.home(), '.config', 'torrent_utilite')

def get_root_path():
    try:
        root = Path(env["ROOT"])
    except KeyError:
        root = get_home_config_dir()
    return root

def get_config():
    path_config = get_root_path()
    if not path_config.exists():
        raise ConfigError(path_config)
    CONFIG_PATH = Path(path_config, 'config.ini')
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config
