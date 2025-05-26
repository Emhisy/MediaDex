import requests
import json
import time
from typing import List, Dict, Optional, Set
from urllib.parse import urljoin, urlparse
from .interfaces.manga_source import MangaSource


class MangaDexSource(MangaSource):
    """
    Comprehensive MangaDex source implementation matching Kotlin functionality.
    Supports search, popular manga, latest updates, detailed manga info, and more.
    """
    
    BASE_URL = "https://mangadex.org"
    API_BASE_URL = "https://api.mangadex.org"
    
    # API endpoints
    API_MANGA_URL = f"{API_BASE_URL}/manga"
    API_CHAPTER_URL = f"{API_BASE_URL}/chapter"
    API_COVER_URL = f"{API_BASE_URL}/cover"
    API_AT_HOME_URL = f"{API_BASE_URL}/at-home/server"
    API_LIST_URL = f"{API_BASE_URL}/list"
    
    # Constants
    MANGA_LIMIT = 20
    LATEST_CHAPTER_LIMIT = 100
    COVER_ART = "cover_art"
    AUTHOR = "author"
    ARTIST = "artist"
    
    # Content ratings
    CONTENT_RATING_SAFE = "safe"
    CONTENT_RATING_SUGGESTIVE = "suggestive"
    CONTENT_RATING_EROTICA = "erotica"
    CONTENT_RATING_PORNOGRAPHIC = "pornographic"
    ALL_CONTENT_RATINGS = [
        CONTENT_RATING_SAFE,
        CONTENT_RATING_SUGGESTIVE,
        CONTENT_RATING_EROTICA,
        CONTENT_RATING_PORNOGRAPHIC
    ]
    
    # Original languages
    ORIGINAL_LANGUAGE_JAPANESE = "ja"
    ORIGINAL_LANGUAGE_CHINESE = "zh"
    ORIGINAL_LANGUAGE_CHINESE_HK = "zh-hk"
    ORIGINAL_LANGUAGE_KOREAN = "ko"
    
    # Search prefixes
    PREFIX_ID_SEARCH = "id:"
    PREFIX_CHAPTER_SEARCH = "ch:"
    PREFIX_USER_SEARCH = "user:"
    PREFIX_GROUP_SEARCH = "group:"
    PREFIX_AUTHOR_SEARCH = "author:"
    PREFIX_LIST_SEARCH = "list:"
    
    # Default blocked groups (spam/low quality)
    DEFAULT_BLOCKED_GROUPS = [
        "4f1de6a2-f0c5-4ac5-bce5-02c7dbb67deb",  # MangaPlus
    ]
    
    def __init__(self, language: str = "en", preferences: Optional[Dict] = None):
        """
        Initialize MangaDex source with language and preferences.
        
        Args:
            language: Target language code (e.g., 'en', 'fr', 'es')
            preferences: User preferences dict
        """
        self.language = language
        self.dex_language = language  # MangaDex language code
        self.preferences = preferences or {}
        
        # Setup session with proper headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MediaDex/1.0 (Python)',
            'Referer': f'{self.BASE_URL}/',
            'Origin': self.BASE_URL,
        })
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.34  # ~3 requests per second
    
    def _rate_limit(self):
        """Implement rate limiting to respect API limits."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    def _make_request(self, url: str, params: Optional[Dict] = None) -> requests.Response:
        """Make a rate-limited request to the API."""
        self._rate_limit()
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response
    
    def _is_valid_uuid(self, uuid_string: str) -> bool:
        """Check if string is a valid UUID."""
        import re
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        return bool(uuid_pattern.match(uuid_string))
    
    def _get_content_ratings(self) -> List[str]:
        """Get content ratings from preferences."""
        return self.preferences.get('content_ratings', [
            self.CONTENT_RATING_SAFE,
            self.CONTENT_RATING_SUGGESTIVE
        ])
    
    def _get_original_languages(self) -> List[str]:
        """Get original languages from preferences."""
        languages = self.preferences.get('original_languages', [
            self.ORIGINAL_LANGUAGE_JAPANESE
        ])
        
        # Add Chinese HK if Chinese is selected
        if self.ORIGINAL_LANGUAGE_CHINESE in languages:
            languages = list(languages) + [self.ORIGINAL_LANGUAGE_CHINESE_HK]
        
        return languages
    
    def _get_blocked_groups(self) -> List[str]:
        """Get blocked groups from preferences."""
        user_blocked = self.preferences.get('blocked_groups', [])
        if isinstance(user_blocked, str):
            user_blocked = [g.strip() for g in user_blocked.split(',') if g.strip()]
        return self.DEFAULT_BLOCKED_GROUPS + user_blocked
    
    def _get_blocked_uploaders(self) -> List[str]:
        """Get blocked uploaders from preferences."""
        blocked = self.preferences.get('blocked_uploaders', [])
        if isinstance(blocked, str):
            blocked = [u.strip() for u in blocked.split(',') if u.strip()]
        return blocked
    
    def _build_manga_url(self, manga_id: str) -> str:
        """Build manga URL from ID."""
        return f"/manga/{manga_id}"
    
    def _build_chapter_url(self, chapter_id: str) -> str:
        """Build chapter URL from ID."""
        return f"/chapter/{chapter_id}"
    
    def _extract_id_from_url(self, url: str) -> str:
        """Extract ID from manga or chapter URL."""
        if url.startswith('/manga/'):
            return url.replace('/manga/', '')
        elif url.startswith('/chapter/'):
            return url.replace('/chapter/', '')
        elif url.startswith('http'):
            # Extract from full URL
            path = urlparse(url).path
            return self._extract_id_from_url(path)
        return url
    
    def _get_cover_url(self, manga_id: str, filename: str, quality: str = "512") -> str:
        """Build cover image URL."""
        if not filename:
            return ""
        return f"https://uploads.mangadex.org/covers/{manga_id}/{filename}.{quality}.jpg"
    
    def _create_manga_from_data(self, manga_data: Dict, cover_filename: str = None) -> Dict:
        """Create manga dict from API data."""
        attributes = manga_data.get('attributes', {})
        manga_id = manga_data.get('id', '')
        
        # Get title in preferred language
        title_dict = attributes.get('title', {})
        title = (
            title_dict.get(self.language) or
            title_dict.get('en') or
            title_dict.get('ja') or
            list(title_dict.values())[0] if title_dict else
            "Unknown Title"
        )
        
        # Get description
        description_dict = attributes.get('description', {})
        description = (
            description_dict.get(self.language) or
            description_dict.get('en') or
            ""
        )
        
        # Get cover image
        cover_url = ""
        if cover_filename:
            cover_url = self._get_cover_url(manga_id, cover_filename)
        else:
            # Try to find cover in relationships
            relationships = manga_data.get('relationships', [])
            for rel in relationships:
                if rel.get('type') == self.COVER_ART:
                    filename = rel.get('attributes', {}).get('fileName')
                    if filename:
                        cover_url = self._get_cover_url(manga_id, filename)
                        break
        
        # Get author/artist
        author = ""
        artist = ""
        for rel in manga_data.get('relationships', []):
            if rel.get('type') == self.AUTHOR:
                author = rel.get('attributes', {}).get('name', '')
            elif rel.get('type') == self.ARTIST:
                artist = rel.get('attributes', {}).get('name', '')
        
        return {
            'title': title,
            'url': self._build_manga_url(manga_id),
            'description': description,
            'cover_url': cover_url,
            'author': author,
            'artist': artist,
            'status': attributes.get('status', ''),
            'tags': [tag.get('attributes', {}).get('name', {}).get('en', '') 
                    for tag in attributes.get('tags', [])],
            'year': attributes.get('year'),
            'original_language': attributes.get('originalLanguage', ''),
            'manga_id': manga_id
        }
    
    def search(self, query: str) -> List[Dict]:
        """
        Search for manga with support for various search types.
        
        Supports:
        - Regular text search
        - ID search: "id:manga-uuid"
        - Chapter search: "ch:chapter-uuid" 
        - User search: "user:user-uuid"
        - Group search: "group:group-uuid"
        - Author search: "author:author-uuid"
        - List search: "list:list-uuid"
        """
        query = query.strip()
        
        try:
            if query.startswith(self.PREFIX_CHAPTER_SEARCH):
                return self._search_by_chapter(query[len(self.PREFIX_CHAPTER_SEARCH):])
            elif query.startswith(self.PREFIX_USER_SEARCH):
                return self._search_by_user(query[len(self.PREFIX_USER_SEARCH):])
            elif query.startswith(self.PREFIX_LIST_SEARCH):
                return self._search_by_list(query[len(self.PREFIX_LIST_SEARCH):])
            elif query.startswith(self.PREFIX_ID_SEARCH):
                return self._search_by_id(query[len(self.PREFIX_ID_SEARCH):])
            elif query.startswith(self.PREFIX_GROUP_SEARCH):
                return self._search_by_group(query[len(self.PREFIX_GROUP_SEARCH):])
            elif query.startswith(self.PREFIX_AUTHOR_SEARCH):
                return self._search_by_author(query[len(self.PREFIX_AUTHOR_SEARCH):])
            else:
                return self._search_by_title(query)
        except Exception as e:
            print(f"Error searching for '{query}': {e}")
            return []
    
    def _search_by_title(self, title: str) -> List[Dict]:
        """Search manga by title."""
        params = {
            'title': title,
            'limit': self.MANGA_LIMIT,
            'offset': 0,
            'includes[]': [self.COVER_ART],
            'contentRating[]': self._get_content_ratings(),
            'originalLanguage[]': self._get_original_languages(),
            'availableTranslatedLanguage[]': [self.dex_language]
        }
        
        response = self._make_request(self.API_MANGA_URL, params)
        data = response.json()
        
        results = []
        for manga_data in data.get('data', []):
            manga = self._create_manga_from_data(manga_data)
            results.append(manga)
        
        return results
    
    def _search_by_id(self, manga_id: str) -> List[Dict]:
        """Search manga by ID."""
        if not self._is_valid_uuid(manga_id):
            raise ValueError("Invalid manga ID format")
        
        params = {
            'ids[]': [manga_id],
            'includes[]': [self.COVER_ART, self.AUTHOR, self.ARTIST],
            'contentRating[]': self.ALL_CONTENT_RATINGS
        }
        
        response = self._make_request(self.API_MANGA_URL, params)
        data = response.json()
        
        results = []
        for manga_data in data.get('data', []):
            manga = self._create_manga_from_data(manga_data)
            results.append(manga)
        
        return results
    
    def _search_by_chapter(self, chapter_id: str) -> List[Dict]:
        """Search manga by chapter ID."""
        if not self._is_valid_uuid(chapter_id):
            raise ValueError("Invalid chapter ID format")
        
        # First get chapter to find manga ID
        response = self._make_request(f"{self.API_CHAPTER_URL}/{chapter_id}")
        chapter_data = response.json()
        
        manga_id = None
        for rel in chapter_data.get('data', {}).get('relationships', []):
            if rel.get('type') == 'manga':
                manga_id = rel.get('id')
                break
        
        if not manga_id:
            return []
        
        return self._search_by_id(manga_id)
    
    def _search_by_group(self, group_id: str) -> List[Dict]:
        """Search manga by scanlation group."""
        if not self._is_valid_uuid(group_id):
            raise ValueError("Invalid group ID format")
        
        params = {
            'group': group_id,
            'limit': self.MANGA_LIMIT,
            'includes[]': [self.COVER_ART],
            'contentRating[]': self._get_content_ratings(),
            'originalLanguage[]': self._get_original_languages()
        }
        
        response = self._make_request(self.API_MANGA_URL, params)
        data = response.json()
        
        results = []
        for manga_data in data.get('data', []):
            manga = self._create_manga_from_data(manga_data)
            results.append(manga)
        
        return results
    
    def _search_by_author(self, author_id: str) -> List[Dict]:
        """Search manga by author."""
        if not self._is_valid_uuid(author_id):
            raise ValueError("Invalid author ID format")
        
        params = {
            'authorOrArtist': author_id,
            'limit': self.MANGA_LIMIT,
            'includes[]': [self.COVER_ART],
            'contentRating[]': self._get_content_ratings(),
            'originalLanguage[]': self._get_original_languages()
        }
        
        response = self._make_request(self.API_MANGA_URL, params)
        data = response.json()
        
        results = []
        for manga_data in data.get('data', []):
            manga = self._create_manga_from_data(manga_data)
            results.append(manga)
        
        return results
    
    def _search_by_user(self, user_id: str) -> List[Dict]:
        """Search manga by uploader."""
        if not self._is_valid_uuid(user_id):
            raise ValueError("Invalid user ID format")
        
        # Get chapters by user first
        params = {
            'uploader': user_id,
            'limit': self.LATEST_CHAPTER_LIMIT,
            'translatedLanguage[]': [self.dex_language],
            'order[publishAt]': 'desc',
            'contentRating[]': self._get_content_ratings(),
            'originalLanguage[]': self._get_original_languages(),
            'excludedGroups[]': self._get_blocked_groups(),
            'excludedUploaders[]': self._get_blocked_uploaders()
        }
        
        response = self._make_request(self.API_CHAPTER_URL, params)
        data = response.json()
        
        # Extract unique manga IDs
        manga_ids = set()
        for chapter in data.get('data', []):
            for rel in chapter.get('relationships', []):
                if rel.get('type') == 'manga':
                    manga_ids.add(rel.get('id'))
        
        if not manga_ids:
            return []
        
        # Get manga details
        params = {
            'ids[]': list(manga_ids),
            'includes[]': [self.COVER_ART],
            'contentRating[]': self._get_content_ratings()
        }
        
        response = self._make_request(self.API_MANGA_URL, params)
        data = response.json()
        
        results = []
        for manga_data in data.get('data', []):
            manga = self._create_manga_from_data(manga_data)
            results.append(manga)
        
        return results
    
    def _search_by_list(self, list_id: str) -> List[Dict]:
        """Search manga by custom list."""
        if not self._is_valid_uuid(list_id):
            raise ValueError("Invalid list ID format")
        
        response = self._make_request(f"{self.API_LIST_URL}/{list_id}")
        list_data = response.json()
        
        # Extract manga IDs from list
        manga_ids = []
        for rel in list_data.get('data', {}).get('relationships', []):
            if rel.get('type') == 'manga':
                manga_ids.append(rel.get('id'))
        
        if not manga_ids:
            return []
        
        # Get manga details
        params = {
            'ids[]': manga_ids,
            'includes[]': [self.COVER_ART],
            'contentRating[]': self._get_content_ratings()
        }
        
        response = self._make_request(self.API_MANGA_URL, params)
        data = response.json()
        
        results = []
        for manga_data in data.get('data', []):
            manga = self._create_manga_from_data(manga_data)
            results.append(manga)
        
        return results
    
    def get_popular_manga(self, page: int = 1) -> List[Dict]:
        """Get popular manga sorted by follow count."""
        offset = (page - 1) * self.MANGA_LIMIT
        
        params = {
            'order[followedCount]': 'desc',
            'availableTranslatedLanguage[]': [self.dex_language],
            'limit': self.MANGA_LIMIT,
            'offset': offset,
            'includes[]': [self.COVER_ART],
            'contentRating[]': self._get_content_ratings(),
            'originalLanguage[]': self._get_original_languages()
        }
        
        response = self._make_request(self.API_MANGA_URL, params)
        data = response.json()
        
        results = []
        for manga_data in data.get('data', []):
            manga = self._create_manga_from_data(manga_data)
            results.append(manga)
        
        return results
    
    def get_latest_updates(self, page: int = 1) -> List[Dict]:
        """Get latest manga updates."""
        offset = (page - 1) * self.LATEST_CHAPTER_LIMIT
        
        # Get latest chapters
        params = {
            'offset': offset,
            'limit': self.LATEST_CHAPTER_LIMIT,
            'translatedLanguage[]': [self.dex_language],
            'order[publishAt]': 'desc',
            'includeFutureUpdates': '0',
            'originalLanguage[]': self._get_original_languages(),
            'contentRating[]': self._get_content_ratings(),
            'excludedGroups[]': self._get_blocked_groups(),
            'excludedUploaders[]': self._get_blocked_uploaders(),
            'includeFuturePublishAt': '0',
            'includeEmptyPages': '0'
        }
        
        response = self._make_request(self.API_CHAPTER_URL, params)
        data = response.json()
        
        # Extract unique manga IDs
        manga_ids = set()
        for chapter in data.get('data', []):
            for rel in chapter.get('relationships', []):
                if rel.get('type') == 'manga':
                    manga_ids.add(rel.get('id'))
        
        if not manga_ids:
            return []
        
        # Get manga details
        params = {
            'ids[]': list(manga_ids),
            'includes[]': [self.COVER_ART],
            'limit': len(manga_ids),
            'contentRating[]': self._get_content_ratings()
        }
        
        response = self._make_request(self.API_MANGA_URL, params)
        data = response.json()
        
        results = []
        for manga_data in data.get('data', []):
            manga = self._create_manga_from_data(manga_data)
            results.append(manga)
        
        return results
    
    def get_manga_details(self, manga_url: str) -> Dict:
        """Get detailed manga information."""
        manga_id = self._extract_id_from_url(manga_url)
        
        if not self._is_valid_uuid(manga_id):
            raise ValueError("Invalid manga URL format")
        
        params = {
            'includes[]': [self.COVER_ART, self.AUTHOR, self.ARTIST]
        }
        
        response = self._make_request(f"{self.API_MANGA_URL}/{manga_id}", params)
        data = response.json()
        
        manga_data = data.get('data')
        if not manga_data:
            return {}
        
        return self._create_manga_from_data(manga_data)
    
    def get_chapters(self, manga_url: str) -> List[Dict]:
        """Get all chapters for a manga with pagination support."""
        manga_id = self._extract_id_from_url(manga_url)
        
        if not self._is_valid_uuid(manga_id):
            raise ValueError("Invalid manga URL format")
        
        all_chapters = []
        offset = 0
        limit = 500  # Max API limit
        
        while True:
            params = {
                'manga': manga_id,
                'limit': limit,
                'offset': offset,
                'translatedLanguage[]': [self.dex_language],
                'order[volume]': 'desc',
                'order[chapter]': 'desc',
                'contentRating[]': self.ALL_CONTENT_RATINGS,
                'excludedGroups[]': self._get_blocked_groups(),
                'excludedUploaders[]': self._get_blocked_uploaders()
            }
            
            response = self._make_request(self.API_CHAPTER_URL, params)
            data = response.json()
            
            chapters = data.get('data', [])
            if not chapters:
                break
            
            for chapter_data in chapters:
                attributes = chapter_data.get('attributes', {})
                
                # Skip invalid chapters
                if attributes.get('isInvalid', False):
                    continue
                
                chapter_id = chapter_data.get('id', '')
                title = attributes.get('title') or f"Chapter {attributes.get('chapter', '')}"
                
                # Get scanlation group
                scanlator = "Unknown"
                for rel in chapter_data.get('relationships', []):
                    if rel.get('type') == 'scanlation_group':
                        scanlator = rel.get('attributes', {}).get('name', 'Unknown')
                        break
                
                chapter = {
                    'title': title,
                    'url': self._build_chapter_url(chapter_id),
                    'chapter_number': attributes.get('chapter'),
                    'volume': attributes.get('volume'),
                    'scanlator': scanlator,
                    'publish_at': attributes.get('publishAt'),
                    'pages': attributes.get('pages', 0),
                    'chapter_id': chapter_id
                }
                
                all_chapters.append(chapter)
            
            # Check if there are more chapters
            if len(chapters) < limit:
                break
            
            offset += limit
        
        return all_chapters
    
    def get_pages(self, chapter_url: str) -> List[str]:
        """Get page URLs for a chapter using at-home server."""
        chapter_id = self._extract_id_from_url(chapter_url)
        
        if not self._is_valid_uuid(chapter_id):
            raise ValueError("Invalid chapter URL format")
        
        # Get at-home server info
        at_home_url = f"{self.API_AT_HOME_URL}/{chapter_id}"
        if self.preferences.get('force_standard_https', False):
            at_home_url += "?forcePort443=true"
        
        response = self._make_request(at_home_url)
        data = response.json()
        
        base_url = data.get('baseUrl', '')
        chapter_info = data.get('chapter', {})
        hash_value = chapter_info.get('hash', '')
        
        # Choose data or data-saver based on preferences
        if self.preferences.get('use_data_saver', False):
            files = chapter_info.get('dataSaver', [])
            data_type = 'data-saver'
        else:
            files = chapter_info.get('data', [])
            data_type = 'data'
        
        # Build page URLs
        pages = []
        for i, filename in enumerate(files):
            page_url = f"{base_url}/{data_type}/{hash_value}/{filename}"
            pages.append(page_url)
        
        return pages
    
    def get_next_chapter(self, current_chapter_url: str, manga_url: str = None) -> Optional[str]:
        """Get next chapter URL."""
        if not manga_url:
            # Try to get manga URL from chapter
            chapter_id = self._extract_id_from_url(current_chapter_url)
            response = self._make_request(f"{self.API_CHAPTER_URL}/{chapter_id}")
            data = response.json()
            
            manga_id = None
            for rel in data.get('data', {}).get('relationships', []):
                if rel.get('type') == 'manga':
                    manga_id = rel.get('id')
                    break
            
            if not manga_id:
                return None
            
            manga_url = self._build_manga_url(manga_id)
        
        chapters = self.get_chapters(manga_url)
        if not chapters:
            return None
        
        # Find current chapter
        current_index = None
        for i, chapter in enumerate(chapters):
            if chapter['url'] == current_chapter_url:
                current_index = i
                break
        
        if current_index is None or current_index == 0:
            return None
        
        # Return next chapter (chapters are sorted desc, so next is previous index)
        return chapters[current_index - 1]['url']
    
    def get_previous_chapter(self, current_chapter_url: str, manga_url: str = None) -> Optional[str]:
        """Get previous chapter URL."""
        if not manga_url:
            # Try to get manga URL from chapter
            chapter_id = self._extract_id_from_url(current_chapter_url)
            response = self._make_request(f"{self.API_CHAPTER_URL}/{chapter_id}")
            data = response.json()
            
            manga_id = None
            for rel in data.get('data', {}).get('relationships', []):
                if rel.get('type') == 'manga':
                    manga_id = rel.get('id')
                    break
            
            if not manga_id:
                return None
            
            manga_url = self._build_manga_url(manga_id)
        
        chapters = self.get_chapters(manga_url)
        if not chapters:
            return None
        
        # Find current chapter
        current_index = None
        for i, chapter in enumerate(chapters):
            if chapter['url'] == current_chapter_url:
                current_index = i
                break
        
        if current_index is None or current_index >= len(chapters) - 1:
            return None
        
        # Return previous chapter (chapters are sorted desc, so previous is next index)
        return chapters[current_index + 1]['url']
    
    def get_manga_aggregate(self, manga_url: str) -> Dict:
        """Get manga chapter aggregate for status determination."""
        manga_id = self._extract_id_from_url(manga_url)
        
        if not self._is_valid_uuid(manga_id):
            raise ValueError("Invalid manga URL format")
        
        params = {
            'translatedLanguage[]': [self.dex_language]
        }
        
        response = self._make_request(f"{self.API_MANGA_URL}/{manga_id}/aggregate", params)
        return response.json()
    
    def get_manga_statistics(self, manga_url: str) -> Dict:
        """Get manga statistics."""
        manga_id = self._extract_id_from_url(manga_url)
        
        if not self._is_valid_uuid(manga_id):
            raise ValueError("Invalid manga URL format")
        
        response = self._make_request(f"{self.API_BASE_URL}/statistics/manga/{manga_id}")
        return response.json()
    
    def get_cover_art(self, manga_url: str, volume: str = None) -> str:
        """Get cover art URL for manga."""
        manga_id = self._extract_id_from_url(manga_url)
        
        if not self._is_valid_uuid(manga_id):
            raise ValueError("Invalid manga URL format")
        
        params = {
            'manga[]': [manga_id],
            'order[volume]': 'asc',
            'limit': 10
        }
        
        if volume:
            params['volume[]'] = [volume]
        
        response = self._make_request(self.API_COVER_URL, params)
        data = response.json()
        
        covers = data.get('data', [])
        if not covers:
            return ""
        
        # Get first cover or volume-specific cover
        cover = covers[0]
        filename = cover.get('attributes', {}).get('fileName', '')
        
        if filename:
            quality = self.preferences.get('cover_quality', '512')
            return self._get_cover_url(manga_id, filename, quality)
        
        return ""
