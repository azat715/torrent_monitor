from pathlib import Path
import pytest
from torrent.conf import get_config, get_home_config_dir, ConfigError

TEST_DATA_DIR = Path(__file__).resolve().parent / 'test_config'

test_config_ini = Path(TEST_DATA_DIR, 'config.ini')
 
@pytest.mark.datafiles(test_config_ini)
def test_config_env(datafiles, monkeypatch):
    monkeypatch.setenv("ROOT", str(datafiles))
    config = get_config()
    assert config['DEFAULT']['db'] == 'db'
    assert config['PROXY']['http'] == 'http://localhost:8118'
    assert config['Rutracker.org']['user'] == 'user'
    assert config['Rutracker.org']['password'] == 'password'

def test_home(monkeypatch):
    monkeypatch.setenv("HOME", "TEST_HOME")
    assert str(get_home_config_dir()) == "TEST_HOME/.config/torrent_utilite"
    with pytest.raises(ConfigError):
        get_config()