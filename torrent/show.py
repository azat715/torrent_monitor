from pathlib import Path
from typing import List
from torrent.parser import Torrent
from torrent.conversion_byte import human_bytes as conversion_byte


def create_torrent(path: str) -> Torrent:
    try:
        return Torrent.read_torrent_file(path)
    except ValueError as e:
        print(e)
        raise Exception from e


def make_message_files(paths: List[Path], lengths: List[int]) -> str:
    res = []
    for path, length in zip(paths, lengths):
        res.append(f"   {path} - {conversion_byte(length)}")
    return "\n".join(res)


def make_announce_list(announce_list: List[List[str]]) -> str:
    res = []
    for items in announce_list:
        for item in items:
            res.append(f"   {item}")
    return "\n".join(res)


def show(path: str, *fields: str, short=False) -> None:
    torrent = create_torrent(path)
    message = {
        "name": torrent.name,
        "announce": torrent.announce,
        "announce list": make_announce_list(torrent.announce_list),
        "comment": torrent.comment,
        "created by": torrent.created_by,
        "creation date": torrent.creation_date,
        "encoding": torrent.encoding,
        "files": make_message_files(torrent.paths, torrent.lengths),
        "publisher": torrent.publisher,
        "publisher url": torrent.publisher_url,
        "total size": conversion_byte(torrent.total_size),
        "multiple": torrent.multiple,
        "file": path,
    }
    if short:
        print(f"Name: {message.get('name')}")
        print(f"Publisher: {message.get('publisher')} - {message.get('publisher url')}")
        return None
    if not fields:
        fields = list(message.keys())
    for field in fields:
        if field in ["announce list", "files"]:
            print(f"{field}:")
            print(f"{message.get(field)}")
        else:
            print(f"{field}: {message.get(field)}")
    return None
