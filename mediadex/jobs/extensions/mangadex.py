import requests
from .interfaces.manga_source import MangaSource

class MangaDexSource(MangaSource):
    BASE_URL = "https://api.mangadex.org"

    def search(self, query):
        params = {"title": query, "limit": 10}
        r = requests.get(f"{self.BASE_URL}/manga", params=params)
        data = r.json()
        results = []
        for manga in data.get("data", []):
            title = manga.get("attributes", {}).get("title", {}).get("en", "N/A")
            results.append({"title": title, "url": manga["id"]})
        return results

    def get_chapters(self, manga_id):
        chapters = []
        offset = 0
        limit = 100
        while True:
            params = {
                "manga": manga_id,
                "limit": limit,
                "offset": offset,
                "translatedLanguage[]": "en"
            }
            r = requests.get(f"{self.BASE_URL}/chapter", params=params)
            data = r.json()
            chap_list = data.get("data", [])
            for chap in chap_list:
                attr = chap.get("attributes", {})
                title = attr.get("title") or f"Chapter {attr.get('chapter')}"
                chapters.append({"title": title, "url": chap["id"]})
            if len(chap_list) < limit:
                break
            offset += limit
        return chapters

    def get_pages(self, chapter_id):
        r = requests.get(f"{self.BASE_URL}/at-home/server/{chapter_id}")
        data = r.json()
        base_url = data.get("baseUrl")
        chapter = data.get("chapter", {})
        hash_value = chapter.get("hash")
        files = chapter.get("data", [])
        return [f"{base_url}/data/{hash_value}/{file}" for file in files]
