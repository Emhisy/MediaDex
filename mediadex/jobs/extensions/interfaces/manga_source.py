from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

class MangaSource(ABC):
    @abstractmethod
    def search(self, query: str):
        """Recherche mangas, retourne liste de dict {title, url}"""
        pass

    @abstractmethod
    def get_chapters(self, manga_url: str):
        """Retourne la liste des chapitres pour un manga donné"""
        pass

    @abstractmethod
    def get_pages(self, chapter_url: str):
        """Retourne la liste des URLs des pages d'un chapitre"""
        pass
