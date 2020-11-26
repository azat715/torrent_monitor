from datetime import datetime
from pathlib import Path
from bencoder import bdecode, BTFailure


class Torrent:
    """
    docstring
    """

    def __init__(self, arg: bytes) -> None:
        try:
            self._raw = bdecode(arg)
        except BTFailure as e:
            print(e)
            raise ValueError("Некорректный файл") from e
        self.announce = self._get_field(b"announce")
        self.comment = self._get_field(b"comment")
        self.created_by = self._get_field(b"created by")
        self.encoding = self._get_field(b"encoding")
        self.publisher = self._get_field(b"publisher")
        self.publisher_url = self._get_field(b"publisher-url")

    def _get_field(self, name: str):
        if self._raw.get(name):
            return self._raw.get(name).decode("utf-8", errors="replace")
        return None

    @property
    def name(self):
        if self._raw[b"info"].get(b"name"):
            return self._raw[b"info"].get(b"name").decode("utf-8", errors="replace")
        return None

    @property
    def announce_list(self):
        if self._raw.get(b"announce-list"):
            return list(map(self.convert, self._raw.get(b"announce-list")))
        elif self._raw.get(b"url-list"):
            return list(
                map(
                    lambda x: [x.decode("utf-8", errors="replace")],
                    self._raw.get(b"url-list"),
                )
            )
        return None

    @property
    def creation_date(self):
        return datetime.fromtimestamp(self._raw.get(b"creation date"))

    @property
    def paths(self):
        paths = self._raw[b"info"].get(b"files")
        if paths:
            paths_raw = map(lambda x: x[b"path"], paths)
            paths_raw_decode = map(self.convert, paths_raw)
            return list(map(lambda x: Path(*x), paths_raw_decode))
        return [
            Path(self.name),
        ]

    @property
    def lengths(self):
        paths = self._raw[b"info"].get(b"files")
        if paths:
            return list(map(lambda x: x[b"length"], paths))
        return [
            self._raw[b"info"].get(b"length"),
        ]

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

    @staticmethod
    def keys():
        return [
            "name",
            "announce",
            "announce_list",
            "comment",
            "created_by",
            "creation_date",
            "encoding",
            "paths",
            "lengths",
            "publisher",
            "publisher_url",
        ]

    @staticmethod
    def convert(items):
        return list(map(lambda x: x.decode("utf-8", errors="replace"), items))
