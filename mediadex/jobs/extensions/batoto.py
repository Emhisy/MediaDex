import requests
from bs4 import BeautifulSoup
from .interfaces.manga_source import MangaSource
from urllib.parse import urlencode

class BatoToSource(MangaSource):
    BASE_URL = "https://batotwo.com"

    def search(self, query):
        if query.startswith("ID:"):
            manga_id = query.split("ID:")[1]
            url = f"{self.BASE_URL}/series/{manga_id}"
            return [{"title": f"Manga {manga_id}", "url": url}]

        params = {
            "word": query,
            "page": "1"
        }
        search_url = f"{self.BASE_URL}/search?{urlencode(params)}"
        resp = requests.get(search_url)
        
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []

        for item in soup.select("div#series-list > div.item"):
            a_tag = item.select_one("a.item-title")
            if a_tag:
                title = a_tag.text.strip()
                href = a_tag.get("href")
                if href and not href.startswith("http"):
                    href = self.BASE_URL + href
                results.append({
                    "title": title,
                    "url": href
                })

        return results

    def get_chapters(self, manga_url):
        r = requests.get(manga_url)
        soup = BeautifulSoup(r.text, "html.parser")
        chapters = []
        
        for row in soup.select("div.main div.p-2"):
            a_tag = row.select_one("a")
            title = a_tag.text.strip()
            href = a_tag.get("href")
            if href and not href.startswith("http"):
                href = self.BASE_URL + href
            chapters.append({"title": title, "url": href})
        
        return chapters

    def get_pages(self, chapter_url):
        r = requests.get(chapter_url)
        soup = BeautifulSoup(r.text, "html.parser")
        pages = [img['src'] for img in soup.select('.page-img')]
        return pages
