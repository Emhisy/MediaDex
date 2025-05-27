
from typing import Dict

from ..jobs.extensions.interfaces.manga_source import MangaSource
from ..jobs.extensions.demoniscans import MangaDemonSource
from ..jobs.extensions.mangadex import MangaDexSource
from ..jobs.extensions.mock.mangadex_mock import MangaDexSourceMock


SOURCES: Dict[str, MangaSource] = {
    "MangaDex": MangaDexSourceMock,
    "Manga Demon": MangaDemonSource
}