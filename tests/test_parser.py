from pathlib import Path
import pytest
from torrent.parser import Torrent

TEST_DATA_DIR = Path(__file__).resolve().parent / 'test_config'

def test_keys():
    assert Torrent.keys() == ['name', 'announce', 'announce_list', 'comment', 'created_by',
    'creation_date', 'encoding', 'paths', 'lengths', 'publisher', 'publisher_url']

@pytest.mark.datafiles(TEST_DATA_DIR)
def test_suit1(datafiles):
    path = Path(datafiles, '0.torrent')
    torrent = Torrent.read_torrent_file(path)
    assert torrent.name == 'archlinux-2019.08.01-x86_64.iso'
    assert torrent.announce == 'http://tracker.archlinux.org:6969/announce'
    assert torrent.announce_list[0] == ['http://mirrors.evowise.com/archlinux/iso/2019.08.01/']
    assert torrent.created_by == 'mktorrent 1.1'
    assert str(torrent.creation_date) == '2019-08-01 19:31:06'
    assert torrent.encoding is None
    assert str(torrent.paths[0]) == 'archlinux-2019.08.01-x86_64.iso'
    assert torrent.lengths[0] == 652214272
    assert torrent.publisher is None
    assert torrent.publisher_url is None
    assert torrent.multiple is False
    assert torrent.total_size == 652214272

@pytest.mark.datafiles(TEST_DATA_DIR)
def test_suit2(datafiles):
    path = Path(datafiles, '4.torrent')
    torrent = Torrent.read_torrent_file(path)
    assert torrent.encoding == 'UTF-8'
    assert str(torrent.paths[0]) == 'Altered.Carbon.S01E01.1080p.NF.WEBRip.4xRus.Eng.sergiy_psp.mkv'
    assert torrent.lengths[0] == 6156344571
    assert torrent.publisher == 'rutracker.org'
    assert torrent.publisher_url == 'https://rutracker.org/forum/viewtopic.php?t=5517277'
    assert torrent.multiple is True
    assert torrent.total_size == 54962480088