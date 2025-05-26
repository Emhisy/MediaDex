#!/usr/bin/env python3
"""
Test file for MangaDex source implementation.
Tests various search types and functionality.
"""

import sys
import os
import json
from typing import Dict, List

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions.mangadex import MangaDexSource


def print_separator(title: str):
    """Print a formatted separator for test sections."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)


def print_manga_info(manga: Dict):
    """Print formatted manga information."""
    print(f"Title: {manga.get('title', 'N/A')}")
    print(f"URL: {manga.get('url', 'N/A')}")
    print(f"Author: {manga.get('author', 'N/A')}")
    print(f"Artist: {manga.get('artist', 'N/A')}")
    print(f"Status: {manga.get('status', 'N/A')}")
    print(f"Year: {manga.get('year', 'N/A')}")
    print(f"Original Language: {manga.get('original_language', 'N/A')}")
    print(f"Cover URL: {manga.get('cover_url', 'N/A')}")
    if manga.get('description'):
        desc = manga['description'][:200] + "..." if len(manga['description']) > 200 else manga['description']
        print(f"Description: {desc}")
    if manga.get('tags'):
        print(f"Tags: {', '.join(manga['tags'][:5])}")  # Show first 5 tags
    print("-" * 40)


def print_chapter_info(chapter: Dict):
    """Print formatted chapter information."""
    print(f"Title: {chapter.get('title', 'N/A')}")
    print(f"URL: {chapter.get('url', 'N/A')}")
    print(f"Chapter: {chapter.get('chapter_number', 'N/A')}")
    print(f"Volume: {chapter.get('volume', 'N/A')}")
    print(f"Scanlator: {chapter.get('scanlator', 'N/A')}")
    print(f"Pages: {chapter.get('pages', 'N/A')}")
    print(f"Published: {chapter.get('publish_at', 'N/A')}")
    print("-" * 40)


def test_title_search():
    """Test title-based search functionality."""
    print_separator("Testing Title Search")
    
    source = MangaDexSource(language="en")
    query = "Hametsu Flag Kaihi no Tame Yamaoku e Hikikomotteita"
    
    print(f"Searching for: '{query}'")
    print("Making API request...")
    
    try:
        results = source.search(query)
        print(f"Found {len(results)} results:")
        
        for i, manga in enumerate(results[:3], 1):  # Show first 3 results
            print(f"\n--- Result {i} ---")
            print_manga_info(manga)
            
    except Exception as e:
        print(f"Error during title search: {e}")


def test_id_search():
    """Test ID-based search functionality."""
    print_separator("Testing ID Search")
    
    source = MangaDexSource(language="en")
    manga_id = "b48a41e8-7072-49eb-a5ed-aab1d98f47af"
    query = f"id:{manga_id}"
    
    print(f"Searching by ID: '{manga_id}'")
    print("Making API request...")
    
    try:
        results = source.search(query)
        print(f"Found {len(results)} results:")
        
        for i, manga in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            print_manga_info(manga)
            
        return results[0] if results else None
            
    except Exception as e:
        print(f"Error during ID search: {e}")
        return None


def test_manga_details(manga_url: str):
    """Test detailed manga information retrieval."""
    print_separator("Testing Manga Details")
    
    source = MangaDexSource(language="en")
    
    print(f"Getting details for: {manga_url}")
    print("Making API request...")
    
    try:
        details = source.get_manga_details(manga_url)
        print("Detailed manga information:")
        print_manga_info(details)
        
        return details
        
    except Exception as e:
        print(f"Error getting manga details: {e}")
        return None


def test_chapters(manga_url: str):
    """Test chapter list retrieval."""
    print_separator("Testing Chapter List")
    
    source = MangaDexSource(language="en")
    
    print(f"Getting chapters for: {manga_url}")
    print("Making API request...")
    
    try:
        chapters = source.get_chapters(manga_url)
        print(f"Found {len(chapters)} chapters:")
        
        # Show first 5 chapters
        for i, chapter in enumerate(chapters[:5], 1):
            print(f"\n--- Chapter {i} ---")
            print_chapter_info(chapter)
            
        return chapters[0] if chapters else None
        
    except Exception as e:
        print(f"Error getting chapters: {e}")
        return None


def test_pages(chapter_url: str):
    """Test page URL retrieval."""
    print_separator("Testing Page URLs")
    
    source = MangaDexSource(language="en")
    
    print(f"Getting pages for: {chapter_url}")
    print("Making API request...")
    
    try:
        pages = source.get_pages(chapter_url)
        print(f"Found {len(pages)} pages:")
        
        # Show first 3 page URLs
        for i, page_url in enumerate(pages[:3], 1):
            print(f"Page {i}: {page_url}")
            
        if len(pages) > 3:
            print(f"... and {len(pages) - 3} more pages")
            
    except Exception as e:
        print(f"Error getting pages: {e}")


def test_popular_manga():
    """Test popular manga retrieval."""
    print_separator("Testing Popular Manga")
    
    source = MangaDexSource(language="en")
    
    print("Getting popular manga...")
    print("Making API request...")
    
    try:
        popular = source.get_popular_manga(page=1)
        print(f"Found {len(popular)} popular manga:")
        
        # Show first 3 popular manga
        for i, manga in enumerate(popular[:3], 1):
            print(f"\n--- Popular #{i} ---")
            print_manga_info(manga)
            
    except Exception as e:
        print(f"Error getting popular manga: {e}")


def test_latest_updates():
    """Test latest updates retrieval."""
    print_separator("Testing Latest Updates")
    
    source = MangaDexSource(language="en")
    
    print("Getting latest updates...")
    print("Making API request...")
    
    try:
        latest = source.get_latest_updates(page=1)
        print(f"Found {len(latest)} recently updated manga:")
        
        # Show first 3 latest updates
        for i, manga in enumerate(latest[:3], 1):
            print(f"\n--- Latest #{i} ---")
            print_manga_info(manga)
            
    except Exception as e:
        print(f"Error getting latest updates: {e}")


def test_chapter_navigation(chapter_url: str, manga_url: str):
    """Test chapter navigation functionality."""
    print_separator("Testing Chapter Navigation")
    
    source = MangaDexSource(language="en")
    
    print(f"Testing navigation for chapter: {chapter_url}")
    
    try:
        # Test next chapter
        next_chapter = source.get_next_chapter(chapter_url, manga_url)
        print(f"Next chapter: {next_chapter or 'None (this might be the latest chapter)'}")
        
        # Test previous chapter
        prev_chapter = source.get_previous_chapter(chapter_url, manga_url)
        print(f"Previous chapter: {prev_chapter or 'None (this might be the first chapter)'}")
        
        # Test navigation dict
        navigation = source.get_chapter_navigation(chapter_url, manga_url)
        print(f"Navigation info: {navigation}")
        
    except Exception as e:
        print(f"Error testing chapter navigation: {e}")


def test_preferences():
    """Test different preference configurations."""
    print_separator("Testing Preferences")
    
    # Test with custom preferences
    preferences = {
        'content_ratings': ['safe', 'suggestive'],
        'original_languages': ['ja', 'ko'],
        'use_data_saver': True,
        'cover_quality': '256'
    }
    
    source = MangaDexSource(language="en", preferences=preferences)
    
    print("Testing with custom preferences:")
    print(f"Content ratings: {preferences['content_ratings']}")
    print(f"Original languages: {preferences['original_languages']}")
    print(f"Data saver: {preferences['use_data_saver']}")
    print(f"Cover quality: {preferences['cover_quality']}")
    
    try:
        # Test search with preferences
        results = source.search("One Piece")
        print(f"Search with preferences returned {len(results)} results")
        
        if results:
            print("First result with custom preferences:")
            print_manga_info(results[0])
            
    except Exception as e:
        print(f"Error testing preferences: {e}")


def main():
    """Run all tests."""
    print("MangaDex Source Implementation Test")
    print("Testing comprehensive functionality...")
    
    # Test 1: Title search
    test_title_search()
    
    # Test 2: ID search
    manga = test_id_search()
    
    if manga:
        manga_url = manga['url']
        
        # Test 3: Manga details
        details = test_manga_details(manga_url)
        
        # Test 4: Chapter list
        first_chapter = test_chapters(manga_url)
        
        if first_chapter:
            chapter_url = first_chapter['url']
            
            # Test 5: Page URLs
            test_pages(chapter_url)
            
            # Test 6: Chapter navigation
            test_chapter_navigation(chapter_url, manga_url)
    
    # Test 7: Popular manga
    test_popular_manga()
    
    # Test 8: Latest updates
    test_latest_updates()
    
    # Test 9: Preferences
    test_preferences()
    
    print_separator("Test Completed")
    print("All tests have been executed.")
    print("Check the output above for any errors or issues.")


if __name__ == "__main__":
    main()
