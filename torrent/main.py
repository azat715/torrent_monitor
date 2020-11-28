import pprint
from pathlib import Path
from typing import List, Dict
import fire
from torrent.parser import Torrent
from torrent.conversion_byte import human_bytes as conversion_byte

def create_torrent(path: str) -> Torrent:
    try:
        res = Torrent.read_torrent_file(path)
    except ValueError as e:
        print(e)
        raise Exception from e
    else:
        return res

def make_message_files(paths: List[Path], lengths: List[int]):
    res = []
    for path, length in zip(paths, lengths):
        res.append(f'{path} - {conversion_byte(length)}')
    return res

def make_message(torrent: Torrent) -> Dict:
    return {
            "name": torrent.name,
            "announce": torrent.announce,
            "announce list": torrent.announce_list,
            "comment": torrent.comment,
            "created by": torrent.created_by,
            "creation date": str(torrent.creation_date),
            "encoding": torrent.encoding,
            "files": '\n'.join(make_message_files(torrent.paths, torrent.lengths)),
            "publisher": torrent.publisher,
            "publisher url": torrent.publisher_url,
            "total size": conversion_byte(torrent.total_size),
            "multiple": torrent.multiple,
        }


def show(path: str, *fields, short=False, width="1200") -> None:
    torrent = create_torrent(path)
    message = make_message(torrent)
    message['file'] = path
    if short:
        pprint.pprint(f"Name: {message.get('name')}", width=width)
        pprint.pprint(f"Publisher: {message.get('publisher')} - {message.get('publisher url')}", width=width)
        pprint.pprint(
                "____________________________________________________________________"
            )
        return None
    if fields:
        for field in fields:
            pprint.pprint(f"{field}: {message.get(field)}", width=width)
        return None
    pprint.pprint(message, width=width)
    return None

def cli():
    fire.Fire(show)
    