from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

class MangaSource(ABC):
    @abstractmethod
    def search(self, query: str):
        """Search for manga, returns list of dict {title, url}"""
        pass

    @abstractmethod
    def get_chapters(self, manga_url: str):
        """Returns the list of chapters for a given manga"""
        pass

    @abstractmethod
    def get_pages(self, chapter_url: str):
        """Returns the list of page URLs for a chapter"""
        pass
    
    def get_next_chapter(self, current_chapter_url: str, manga_url: str = None):
        """
        Get the next chapter URL based on current chapter.
        Returns None if no next chapter exists.
        """
        return None
    
    def get_previous_chapter(self, current_chapter_url: str, manga_url: str = None):
        """
        Get the previous chapter URL based on current chapter.
        Returns None if no previous chapter exists.
        """
        return None
    
    def get_chapter_navigation(self, current_chapter_url: str, manga_url: str = None):
        """
        Get navigation information for current chapter.
        Returns dict with 'next' and 'previous' chapter URLs.
        """
        return {
            'next': self.get_next_chapter(current_chapter_url, manga_url),
            'previous': self.get_previous_chapter(current_chapter_url, manga_url)
        }

    @abstractmethod
    def get_popular_manga(self, page: int = 1):
        pass
