import requests
from bs4 import BeautifulSoup
from .interfaces.manga_source import MangaSource
from urllib.parse import urlencode
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crytoaes import get_decrypted_image_urls
import re


class BatoToSource(MangaSource):
    """
    BatoTo manga source implementation with crypto support for image decryption.
    Supports search, chapter listing, and encrypted page extraction.
    """
    
    BASE_URL = "https://batotwo.com"
    
    def __init__(self):
        self.session = requests.Session()
        # Set simple headers to avoid bot detection
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def search(self, query: str) -> list:
        """
        Search for manga on BatoTo.
        Supports both text search and ID-based lookup.
        """
        if query.startswith("ID:"):
            # Direct ID lookup
            manga_id = query[3:].strip()
            url = f"{self.BASE_URL}/series/{manga_id}"
            
            try:
                response = self.session.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Extract manga title from the page
                title_element = soup.select_one("div#mainer div.container-fluid h3")
                title = title_element.text.strip() if title_element else f"Manga {manga_id}"
                
                return [{"title": title, "url": url}]
            except Exception as e:
                print(f"Error fetching manga ID {manga_id}: {e}")
                return []

        # Text search
        params = {"word": query, "page": "1"}
        search_url = f"{self.BASE_URL}/search?{urlencode(params)}"
        
        try:
            response = self.session.get(search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            # Updated selector based on actual BatoTo structure
            for item in soup.select("div#series-list div.col"):
                title_link = item.select_one("a.item-title")
                cover_link = item.select_one("a.item-cover")
                
                if title_link:
                    title = title_link.text.strip()
                    href = title_link.get("href") or (cover_link.get("href") if cover_link else None)
                    
                    if href:
                        if not href.startswith("http"):
                            href = self.BASE_URL + href
                        
                        # Get thumbnail if available
                        thumbnail = None
                        img_element = item.select_one("img")
                        if img_element:
                            thumbnail = img_element.get("src")
                            if thumbnail and not thumbnail.startswith("http"):
                                thumbnail = self.BASE_URL + thumbnail
                        
                        result = {"title": title, "url": href}
                        if thumbnail:
                            result["thumbnail"] = thumbnail
                        
                        results.append(result)

            return results
            
        except Exception as e:
            print(f"Error searching for '{query}': {e}")
            return []

    def get_chapters(self, manga_url: str) -> list:
        """
        Get list of chapters for a manga.
        Returns chapters with title, URL, and metadata.
        """
        try:
            response = self.session.get(manga_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            chapters = []
            
            # Check if chapter list is available
            warning_element = soup.select_one(".episode-list > .alert-warning")
            if warning_element and "deleted" in warning_element.text.lower():
                raise Exception("This manga has been marked as deleted and the chapter list is not available")
            
            # Extract chapters
            for row in soup.select("div.main div.p-2"):
                chapter_link = row.select_one("a.chapt")
                if not chapter_link:
                    continue
                
                title = chapter_link.text.strip()
                href = chapter_link.get("href")
                
                if href:
                    if not href.startswith("http"):
                        href = self.BASE_URL + href
                    
                    # Extract additional metadata
                    chapter_data = {"title": title, "url": href}
                    
                    # Get scanlator/group info
                    group_element = row.select_one("div.extra > a:not(.ps-3)")
                    user_element = row.select_one("div.extra > a.ps-3")
                    
                    if group_element:
                        chapter_data["scanlator"] = group_element.text.strip()
                    elif user_element:
                        chapter_data["scanlator"] = user_element.text.strip()
                    else:
                        chapter_data["scanlator"] = "Unknown"
                    
                    # Get upload time
                    time_element = row.select_one("div.extra > i.ps-3")
                    if time_element:
                        chapter_data["upload_time"] = time_element.text.strip()
                    
                    chapters.append(chapter_data)
            
            return chapters
            
        except Exception as e:
            print(f"Error getting chapters for '{manga_url}': {e}")
            return []

    def get_pages(self, chapter_url: str) -> list:
        """
        Get list of page URLs for a chapter.
        Handles encrypted image URLs using crypto decryption.
        """
        try:
            response = self.session.get(chapter_url)
            response.raise_for_status()
            
            # Try to get decrypted image URLs using crypto
            try:
                decrypted_urls = get_decrypted_image_urls(response.text)
                if decrypted_urls:
                    # Filter out history URLs
                    real_urls = [url for url in decrypted_urls if "history" not in url]
                    if real_urls:
                        return real_urls
                    else:
                        print("Warning: All decrypted URLs are history pages")
            except Exception as crypto_error:
                print(f"Crypto decryption failed: {crypto_error}")
                # Fall back to simple image extraction
            
            # Fallback: try to extract images directly from HTML
            soup = BeautifulSoup(response.text, "html.parser")
            pages = []
            
            # Look for various image selectors
            for selector in ['.page-img', 'img.page-image', '.reader-image', 'img[data-src]']:
                images = soup.select(selector)
                if images:
                    for img in images:
                        src = img.get('src') or img.get('data-src')
                        if src and "history" not in src:  # Skip history URLs
                            if not src.startswith('http'):
                                src = self.BASE_URL + src
                            pages.append(src)
                    break
            
            if not pages:
                # Last resort: look for any images in the content area
                content_area = soup.select_one('#mainer, .reader, .chapter-content')
                if content_area:
                    for img in content_area.select('img'):
                        src = img.get('src') or img.get('data-src')
                        if src and 'cover' not in src.lower() and "history" not in src:
                            if not src.startswith('http'):
                                src = self.BASE_URL + src
                            pages.append(src)
            
            # If we still only have history pages, the content might not be available
            if pages and all("history" in page for page in pages):
                print("Warning: Only history pages found - content may not be available")
            
            return pages
            
        except Exception as e:
            print(f"Error getting pages for '{chapter_url}': {e}")
            return []

    def get_manga_details(self, manga_url: str) -> dict:
        """
        Get detailed information about a manga.
        This is an additional method not in the base interface.
        """
        try:
            response = self.session.get(manga_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            info_element = soup.select_one("div#mainer div.container-fluid")
            if not info_element:
                return {}
            
            details = {}
            
            # Title
            title_element = info_element.select_one("h3")
            if title_element:
                details["title"] = title_element.text.strip()
            
            # Thumbnail
            thumbnail_element = soup.select_one("div.attr-cover img")
            if thumbnail_element:
                thumbnail = thumbnail_element.get("src")
                if thumbnail and not thumbnail.startswith("http"):
                    thumbnail = self.BASE_URL + thumbnail
                details["thumbnail"] = thumbnail
            
            # Author and Artist
            author_element = info_element.select_one("div.attr-item:contains(author) span")
            if author_element:
                details["author"] = author_element.text.strip()
            
            artist_element = info_element.select_one("div.attr-item:contains(artist) span")
            if artist_element:
                details["artist"] = artist_element.text.strip()
            
            # Status
            work_status_element = info_element.select_one("div.attr-item:contains(original work) span")
            upload_status_element = info_element.select_one("div.attr-item:contains(upload status) span")
            
            if work_status_element or upload_status_element:
                status = (work_status_element or upload_status_element).text.strip()
                details["status"] = status
            
            # Genres
            genre_elements = info_element.select(".attr-item b:contains(genres) + span")
            if genre_elements:
                genres = [elem.text.strip() for elem in genre_elements]
                details["genres"] = genres
            
            # Description
            description_element = info_element.select_one("div.limit-html")
            if description_element:
                details["description"] = description_element.text.strip()
            
            return details
            
        except Exception as e:
            print(f"Error getting manga details for '{manga_url}': {e}")
            return {}

    def get_next_chapter(self, current_chapter_url: str, manga_url: str = None) -> str:
        """
        Get the next chapter URL based on current chapter.
        Returns None if no next chapter exists.
        """
        try:
            # If manga_url is not provided, try to extract it from chapter URL
            if not manga_url:
                manga_url = self._extract_manga_url_from_chapter(current_chapter_url)
                if not manga_url:
                    return None
            
            # Get all chapters for the manga
            chapters = self.get_chapters(manga_url)
            if not chapters:
                return None
            
            # Find current chapter index
            current_index = None
            for i, chapter in enumerate(chapters):
                if chapter["url"] == current_chapter_url:
                    current_index = i
                    break
            
            if current_index is None:
                return None
            
            # Return next chapter (chapters are usually ordered newest first)
            # So next chapter is at index - 1
            if current_index > 0:
                return chapters[current_index - 1]["url"]
            
            return None
            
        except Exception as e:
            print(f"Error getting next chapter for '{current_chapter_url}': {e}")
            return None

    def get_previous_chapter(self, current_chapter_url: str, manga_url: str = None) -> str:
        """
        Get the previous chapter URL based on current chapter.
        Returns None if no previous chapter exists.
        """
        try:
            # If manga_url is not provided, try to extract it from chapter URL
            if not manga_url:
                manga_url = self._extract_manga_url_from_chapter(current_chapter_url)
                if not manga_url:
                    return None
            
            # Get all chapters for the manga
            chapters = self.get_chapters(manga_url)
            if not chapters:
                return None
            
            # Find current chapter index
            current_index = None
            for i, chapter in enumerate(chapters):
                if chapter["url"] == current_chapter_url:
                    current_index = i
                    break
            
            if current_index is None:
                return None
            
            # Return previous chapter (chapters are usually ordered newest first)
            # So previous chapter is at index + 1
            if current_index < len(chapters) - 1:
                return chapters[current_index + 1]["url"]
            
            return None
            
        except Exception as e:
            print(f"Error getting previous chapter for '{current_chapter_url}': {e}")
            return None

    def get_chapter_navigation_from_page(self, chapter_url: str) -> dict:
        """
        Extract chapter navigation directly from the chapter page.
        This method looks for navigation links on the chapter page itself.
        """
        try:
            response = self.session.get(chapter_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            navigation = {"next": None, "previous": None}
            
            # Look for navigation elements on the page
            # BatoTo typically has navigation buttons/links
            nav_selectors = [
                "a[href*='/chapter/']:contains('Next')",
                "a[href*='/chapter/']:contains('Previous')",
                "a[href*='/chapter/']:contains('Prev')",
                ".chapter-nav a[href*='/chapter/']",
                ".nav-chapter a[href*='/chapter/']",
                ".reader-nav a[href*='/chapter/']"
            ]
            
            for selector in nav_selectors:
                try:
                    links = soup.select(selector)
                    for link in links:
                        href = link.get("href")
                        text = link.text.lower().strip()
                        
                        if href:
                            if not href.startswith("http"):
                                href = self.BASE_URL + href
                            
                            if "next" in text:
                                navigation["next"] = href
                            elif "prev" in text or "previous" in text:
                                navigation["previous"] = href
                except Exception:
                    continue
            
            return navigation
            
        except Exception as e:
            print(f"Error getting chapter navigation from page '{chapter_url}': {e}")
            return {"next": None, "previous": None}

    def _extract_manga_url_from_chapter(self, chapter_url: str) -> str:
        """
        Extract manga URL from chapter URL.
        BatoTo chapter URLs typically follow pattern: /chapter/XXXXX
        We need to find the corresponding manga series URL.
        """
        try:
            # Try to get the chapter page and look for manga link
            response = self.session.get(chapter_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Look for manga/series link in breadcrumbs or navigation
            manga_link_selectors = [
                "a[href*='/series/']",
                ".breadcrumb a[href*='/series/']",
                ".nav a[href*='/series/']",
                "a[href*='/title/']"  # Alternative pattern
            ]
            
            for selector in manga_link_selectors:
                manga_link = soup.select_one(selector)
                if manga_link:
                    href = manga_link.get("href")
                    if href:
                        if not href.startswith("http"):
                            href = self.BASE_URL + href
                        return href
            
            return None
            
        except Exception as e:
            print(f"Error extracting manga URL from chapter '{chapter_url}': {e}")
            return None
