import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote_plus, urljoin
from datetime import datetime
from .interfaces.manga_source import MangaSource

class MangaDemonSource(MangaSource):
    BASE_URL = "https://demonicscans.org"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Referer': f'{self.BASE_URL}/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def _make_absolute_url(self, url):
        """Convert relative URL to absolute URL"""
        if url and not url.startswith('http'):
            return urljoin(self.BASE_URL, url)
        return url

    def get_popular_manga(self, page=1):
        """Get popular manga list - equivalent to popularMangaRequest in Kotlin"""
        url = f"{self.BASE_URL}/advanced.php?list={page}&status=all&orderby=VIEWS%20DESC"
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        results = []
        # Selector from Kotlin: "div#advanced-content > div.advanced-element"
        for element in soup.select('div#advanced-content > div.advanced-element'):
            manga_link = element.select_one('a')
            title_element = element.select_one('h1')
            thumbnail_element = element.select_one('img')
            
            if manga_link and title_element:
                results.append({
                    "title": title_element.get_text(strip=True),
                    "url": self._make_absolute_url(manga_link.get('href')),
                    "thumbnail_url": self._make_absolute_url(thumbnail_element.get('src')) if thumbnail_element else None
                })
        return results

    def get_latest_updates(self, page=1):
        """Get latest updates - equivalent to latestUpdatesRequest in Kotlin"""
        url = f"{self.BASE_URL}/lastupdates.php?list={page}"
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        results = []
        # Selector from Kotlin: "div#updates-container > div.updates-element"
        for element in soup.select('div#updates-container > div.updates-element'):
            info_div = element.select_one('div.updates-element-info')
            thumbnail_element = element.select_one('div.thumb img')
            
            if info_div:
                manga_link = info_div.select_one('a')
                if manga_link:
                    results.append({
                        "title": manga_link.get_text(strip=True),
                        "url": self._make_absolute_url(manga_link.get('href')),
                        "thumbnail_url": self._make_absolute_url(thumbnail_element.get('src')) if thumbnail_element else None
                    })
        return results

    def search(self, query):
        """Search manga - equivalent to searchMangaRequest in Kotlin"""
        if not query.strip():
            return []
            
        url = f"{self.BASE_URL}/search.php"
        params = {'manga': query}
        response = self.session.get(url, params=params)
        soup = BeautifulSoup(response.text, "html.parser")
        
        results = []
        # Updated selector based on actual HTML structure
        for element in soup.select('a[href*="/manga/"]'):
            title_element = element.select_one('div.seach-right > div')
            thumbnail_element = element.select_one('img')
            
            if title_element:
                results.append({
                    "title": title_element.get_text(strip=True),
                    "url": self._make_absolute_url(element.get('href')),
                    "thumbnail_url": self._make_absolute_url(thumbnail_element.get('src')) if thumbnail_element else None
                })
        return results

    def get_manga_details(self, manga_url):
        """Get manga details - equivalent to mangaDetailsParse in Kotlin"""
        absolute_url = self._make_absolute_url(manga_url)
        response = self.session.get(absolute_url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        manga_info = soup.select_one('div#manga-info-container')
        if not manga_info:
            return None
            
        title_element = manga_info.select_one('h1.big-fat-titles')
        thumbnail_element = manga_info.select_one('div#manga-page img')
        description_element = manga_info.select_one('div#manga-info-rightColumn > div > div.white-font')
        
        # Extract genres
        genre_elements = manga_info.select('div.genres-list > li')
        genres = [genre.get_text(strip=True) for genre in genre_elements]
        
        # Extract author and status - BeautifulSoup doesn't support :has(), :eq(), :contains()
        author = None
        status_text = None
        
        # Find author and status by iterating through stats divs
        stats_divs = manga_info.select('div#manga-info-stats > div')
        for stats_div in stats_divs:
            li_elements = stats_div.select('li')
            if len(li_elements) >= 2:
                label = li_elements[0].get_text(strip=True).lower()
                value = li_elements[1].get_text(strip=True)
                
                if 'author' in label:
                    author = value
                elif 'status' in label:
                    status_text = value
        
        status = self._parse_status(status_text)
        
        return {
            "title": title_element.get_text(strip=True) if title_element else None,
            "thumbnail_url": self._make_absolute_url(thumbnail_element.get('src')) if thumbnail_element else None,
            "description": description_element.get_text(strip=True) if description_element else None,
            "genres": genres,
            "author": author,
            "status": status
        }

    def get_chapters(self, manga_url):
        """Get chapter list - equivalent to chapterFromElement in Kotlin"""
        absolute_url = self._make_absolute_url(manga_url)
        response = self.session.get(absolute_url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        chapters = []
        # Selector from Kotlin: "div#chapters-list a.chplinks"
        for element in soup.select('div#chapters-list a.chplinks'):
            title = element.get_text(strip=True)
            href = element.get('href')
            
            # Extract date from span element
            date_element = element.select_one('span')
            date_text = date_element.get_text(strip=True) if date_element else None
            upload_date = self._parse_date(date_text)
            
            if title and href:
                chapters.append({
                    "title": title,
                    "url": self._make_absolute_url(href),
                    "date_upload": upload_date
                })
        return chapters

    def get_pages(self, chapter_url):
        """Get page images - equivalent to pageListParse in Kotlin"""
        absolute_url = self._make_absolute_url(chapter_url)
        response = self.session.get(absolute_url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Selector from Kotlin: "div > img.imgholder"
        pages = []
        for img in soup.select('div > img.imgholder'):
            src = img.get('src')
            if src:
                pages.append(self._make_absolute_url(src))
        return pages

    def _parse_status(self, status_text):
        """Parse manga status - equivalent to parseStatus in Kotlin"""
        if not status_text:
            return "unknown"
        
        status_lower = status_text.lower()
        if "ongoing" in status_lower:
            return "ongoing"
        elif "completed" in status_lower:
            return "completed"
        else:
            return "unknown"

    def _parse_date(self, date_str):
        """Parse date string - equivalent to parseDate in Kotlin"""
        if not date_str:
            return None
            
        try:
            # Format: yyyy-MM-dd (as used in Kotlin DATE_FORMATTER)
            return datetime.strptime(date_str, "%Y-%m-%d").timestamp()
        except ValueError:
            return None
