import configparser
from pathlib import Path
from os import environ

env = environ

class ConfigError(Exception):
    def __init__(self, path):
        print(f'{str(path)} Not found')

def get_home_config_dir():
    return Path(Path.home(), '.config', 'torrent_utilite')

def get_root_path():
    try:
        ROOT = Path(env["ROOT"])
    except KeyError:
        ROOT = get_home_config_dir()
    return ROOT

def get_config():
    path_config = get_root_path()
    if not path_config.exists():
        raise ConfigError(path_config)
    CONFIG_PATH = Path(path_config, 'config.ini')
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config
