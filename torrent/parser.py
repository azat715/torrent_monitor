from datetime import datetime
from pathlib import Path
from bencoder import bdecode, BTFailure

class Torrent:
    """
    docstring
    """

    def __init__(self, arg: bytes) -> None:
        try:
            raw = bdecode(arg)
        except BTFailure as e:
            print(e)
            raise ValueError("Некорректный файл") from e
        info = raw[b"info"]
        self._data = {
            "name": info.get(b"name"),
            "announce": raw.get(b"announce"),
            "announce_list": raw.get(b"announce-list"),
            "url_list": raw.get(b"url-list"),
            "comment": raw.get(b"comment"),
            "created_by": raw.get(b"created by"),
            "creation_date": raw.get(b"creation date"),
            "encoding": raw.get(b"encoding"),
            "publisher": raw.get(b"announce"),
            "publisher_url": raw.get(b"announce"),
        }
        self._paths = info.get(b"files")
        self._lengths = info.get(b"length")

    def __getattr__(self, name: str):
        try:
            if name == "announce_list":
                if self._data["announce_list"]:
                    return list(map(self.convert, self._data[name]))
                return list(
                    map(
                        lambda x: [x.decode("utf-8", errors="replace")],
                        self._data["url_list"],
                    )
                )
            elif name == "creation_date":
                return datetime.fromtimestamp(self._data[name])
            else:
                if self._data[name]:
                    return self._data[name].decode("utf-8", errors="replace")
                return None
        except AttributeError as e:
            print(f"Field {name} - Error")
            print(e)
            raise ValueError from e

    def __repr__(self):
        return "Torrent('name':  {self.name}, 'announce': {self.announce}, 'announce_list': {self.announce_list}, \
'comment': {self.comment}, 'created_by': {self.created_by}, 'creation_date': {self.creation_date}, \
'encoding': {self.encoding}, 'paths': {self.paths}, 'lengths': {self.lengths}, \
'publisher': {self.publisher}, 'publisher_url': {self.publisher_url})".format(
            self=self
        )

    def __str__(self):
        return f"""{{name':  {self.name}, 'announce': {self.announce}, 'announce_list': {self.announce_list}, \
'comment': {self.comment}, 'created_by': {self.created_by}, 'creation_date': {self.creation_date}, \
'encoding': {self.encoding}, 'paths': {self.paths}, 'lengths': {self.lengths}, 'publisher': {self.publisher}, \
'publisher_url': {self.publisher_url},}}"""

    @property
    def paths(self):
        if self._paths:
            paths_raw = map(lambda x: x[b"path"], self._paths)
            paths_raw_decode = map(self.convert, paths_raw)
            paths = map(lambda x: Path(*x), paths_raw_decode)
            return list(paths)
        return [
            Path(self.name),
        ]

    @property
    def lengths(self):
        if self._paths:
            return list(map(lambda x: x[b"length"], self._paths))
        return [
            self._lengths,
        ]

    @staticmethod
    def keys():
        return ['name', 'announce', 'announce_list', 'comment', 'created_by', 'creation_date',
        'encoding', 'paths', 'lengths', 'publisher', 'publisher_url']
    
    @staticmethod
    def convert(items):
        return list(map(lambda x: x.decode("utf-8", errors="replace"), items))
