import requests
from bs4 import BeautifulSoup
from .interfaces.manga_source import MangaSource

class MangaDemonSource(MangaSource):
    BASE_URL = "https://demonicscans.org"

    def search(self, query):
        url = f"{self.BASE_URL}/?s={query.replace(' ', '+')}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        # Le selector utilisé par l’extension est 'div.bs a' (liens mangas)
        for a in soup.select('div.bs a'):
            title = a.get('title')
            href = a.get('href')
            if title and href:
                results.append({"title": title, "url": href})
        return results

    def get_chapters(self, manga_url):
        r = requests.get(manga_url)
        soup = BeautifulSoup(r.text, "html.parser")
        chapters = []
        # Le selector Kotlin est 'li.wp-manga-chapter > a' → ici '.eph-num a' semble équivalent
        for a in soup.select('li.wp-manga-chapter > a'):
            title = a.text.strip()
            href = a.get('href')
            if title and href:
                chapters.append({"title": title, "url": href})
        return chapters

    def get_pages(self, chapter_url):
        r = requests.get(chapter_url)
        soup = BeautifulSoup(r.text, "html.parser")
        # Selector Kotlin : 'div.page-break > img' ou '.reading-content img'
        pages = [img['src'] for img in soup.select('div.page-break > img')]
        return pages
