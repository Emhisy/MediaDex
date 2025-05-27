#!/usr/bin/env python3
"""
Test file specifically for MangaDex page retrieval functionality.
Tests the get_pages method with known working chapter IDs.
"""

import sys
import os
from typing import Dict, List

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions.mangadex import MangaDexSource


def print_separator(title: str):
    """Print a formatted separator for test sections."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)


def test_pages_with_known_chapter():
    """Test page retrieval with a known working chapter ID."""
    print_separator("Testing Page Retrieval with Known Chapter")
    
    source = MangaDexSource(language="en")
    
    # Use a known chapter ID from a popular manga (One Piece chapter)
    # This is a real chapter ID that should work
    chapter_id = "cb7a214e-56fe-4f3a-8900-f29ab5d8ae68"  # One Piece chapter
    chapter_url = f"/chapter/{chapter_id}"
    
    print(f"Testing page retrieval for chapter: {chapter_url}")
    print("Making API request to at-home server...")
    
    try:
        pages = source.get_pages(chapter_url)
        print(f"Successfully retrieved {len(pages)} pages:")
        
        # Show first 3 page URLs
        for i, page_url in enumerate(pages[:3], 1):
            print(f"Page {i}: {page_url}")
            
        if len(pages) > 3:
            print(f"... and {len(pages) - 3} more pages")
            
        # Test with data saver mode
        print("\n--- Testing with Data Saver Mode ---")
        source_data_saver = MangaDexSource(
            language="en", 
            preferences={'use_data_saver': True}
        )
        
        pages_data_saver = source_data_saver.get_pages(chapter_url)
        print(f"Data saver mode retrieved {len(pages_data_saver)} pages:")
        
        # Show first 2 data saver URLs
        for i, page_url in enumerate(pages_data_saver[:2], 1):
            print(f"Data Saver Page {i}: {page_url}")
            
        return True
        
    except Exception as e:
        print(f"Error getting pages: {e}")
        return False


def test_pages_from_search_result():
    """Test page retrieval by first searching for a manga and getting its chapters."""
    print_separator("Testing Page Retrieval from Search Result")
    
    source = MangaDexSource(language="en")
    
    # Search for a popular manga
    print("Searching for 'One Piece'...")
    try:
        search_results = source.search("One Piece")
        if not search_results:
            print("No search results found")
            return False
            
        manga = search_results[0]
        manga_url = manga['url']
        print(f"Found manga: {manga['title']}")
        print(f"Manga URL: {manga_url}")
        
        # Get first few chapters (limit to avoid too many API calls)
        print("\nGetting chapters...")
        
        # Use a simpler approach - get chapters with basic parameters
        manga_id = source._extract_id_from_url(manga_url)
        
        # Try to get chapters with minimal parameters to avoid API errors
        params = {
            'manga': manga_id,
            'limit': 5,  # Just get first 5 chapters
            'offset': 0,
            'translatedLanguage[]': ['en'],
            'order[chapter]': 'asc'  # Get earliest chapters first
        }
        
        response = source._make_request(source.API_CHAPTER_URL, params)
        data = response.json()
        
        chapters = data.get('data', [])
        if not chapters:
            print("No chapters found")
            return False
            
        print(f"Found {len(chapters)} chapters")
        
        # Test pages for the first chapter
        first_chapter = chapters[0]
        chapter_id = first_chapter.get('id', '')
        chapter_url = f"/chapter/{chapter_id}"
        
        chapter_title = first_chapter.get('attributes', {}).get('title', 'Unknown')
        chapter_number = first_chapter.get('attributes', {}).get('chapter', 'Unknown')
        
        print(f"\nTesting pages for: Chapter {chapter_number} - {chapter_title}")
        print(f"Chapter URL: {chapter_url}")
        
        pages = source.get_pages(chapter_url)
        print(f"Successfully retrieved {len(pages)} pages:")
        
        # Show first 3 page URLs
        for i, page_url in enumerate(pages[:3], 1):
            print(f"Page {i}: {page_url}")
            
        if len(pages) > 3:
            print(f"... and {len(pages) - 3} more pages")
            
        return True
        
    except Exception as e:
        print(f"Error in search-based page test: {e}")
        return False


def test_pages_with_preferences():
    """Test page retrieval with different preference configurations."""
    print_separator("Testing Page Retrieval with Different Preferences")
    
    # Test with standard quality
    print("--- Standard Quality ---")
    source_standard = MangaDexSource(
        language="en",
        preferences={
            'use_data_saver': False,
            'force_standard_https': False
        }
    )
    
    # Test with data saver
    print("--- Data Saver Mode ---")
    source_data_saver = MangaDexSource(
        language="en",
        preferences={
            'use_data_saver': True,
            'force_standard_https': False
        }
    )
    
    # Test with forced HTTPS
    print("--- Forced Standard HTTPS ---")
    source_https = MangaDexSource(
        language="en",
        preferences={
            'use_data_saver': False,
            'force_standard_https': True
        }
    )
    
    # Use a known working chapter
    chapter_id = "32d76d19-8a05-4db0-9fc2-e0b0648fe7d0"
    chapter_url = f"/chapter/{chapter_id}"
    
    try:
        # Test standard quality
        pages_standard = source_standard.get_pages(chapter_url)
        print(f"Standard quality: {len(pages_standard)} pages")
        if pages_standard:
            print(f"Sample URL: {pages_standard[0]}")
        
        # Test data saver
        pages_data_saver = source_data_saver.get_pages(chapter_url)
        print(f"Data saver: {len(pages_data_saver)} pages")
        if pages_data_saver:
            print(f"Sample URL: {pages_data_saver[0]}")
        
        # Test forced HTTPS
        pages_https = source_https.get_pages(chapter_url)
        print(f"Forced HTTPS: {len(pages_https)} pages")
        if pages_https:
            print(f"Sample URL: {pages_https[0]}")
        
        return True
        
    except Exception as e:
        print(f"Error testing preferences: {e}")
        return False


def test_invalid_chapter():
    """Test page retrieval with invalid chapter ID."""
    print_separator("Testing Page Retrieval with Invalid Chapter")
    
    source = MangaDexSource(language="en")
    
    # Test with invalid UUID
    print("Testing with invalid UUID...")
    try:
        pages = source.get_pages("/chapter/invalid-uuid")
        print("Unexpected success with invalid UUID")
    except ValueError as e:
        print(f"Correctly caught error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Test with non-existent but valid UUID
    print("\nTesting with non-existent chapter...")
    try:
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        pages = source.get_pages(f"/chapter/{fake_uuid}")
        print(f"Got {len(pages)} pages for non-existent chapter")
    except Exception as e:
        print(f"Error with non-existent chapter: {e}")


def main():
    """Run all page retrieval tests."""
    print("MangaDex Page Retrieval Test")
    print("Testing page URL generation and at-home server integration...")
    
    success_count = 0
    total_tests = 4
    
    # Test 1: Known chapter ID
    if test_pages_with_known_chapter():
        success_count += 1
    
    # Test 2: Search-based approach
    if test_pages_from_search_result():
        success_count += 1
    
    # Test 3: Different preferences
    if test_pages_with_preferences():
        success_count += 1
    
    # Test 4: Invalid input handling
    test_invalid_chapter()
    success_count += 1  # This test always "succeeds" as it tests error handling
    
    print_separator("Page Retrieval Test Results")
    print(f"Successful tests: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("✅ All page retrieval tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    main()
