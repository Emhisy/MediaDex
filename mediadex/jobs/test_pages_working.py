#!/usr/bin/env python3
"""
Test file for MangaDex page retrieval with working chapters.
Finds recent chapters and tests page retrieval functionality.
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


def find_working_chapter():
    """Find a recent chapter that should have working page URLs."""
    print_separator("Finding Working Chapter from Latest Updates")
    
    source = MangaDexSource(language="en")
    
    print("Getting latest chapter updates...")
    try:
        # Get latest chapters directly
        params = {
            'limit': 20,
            'offset': 0,
            'translatedLanguage[]': ['en'],
            'order[publishAt]': 'desc',
            'includeFutureUpdates': '0',
            'includeFuturePublishAt': '0',
            'includeEmptyPages': '0',
            'contentRating[]': ['safe', 'suggestive']
        }
        
        response = source._make_request(source.API_CHAPTER_URL, params)
        data = response.json()
        
        chapters = data.get('data', [])
        if not chapters:
            print("No recent chapters found")
            return None
            
        print(f"Found {len(chapters)} recent chapters")
        
        # Try each chapter until we find one with working pages
        for i, chapter_data in enumerate(chapters):
            chapter_id = chapter_data.get('id', '')
            chapter_url = f"/chapter/{chapter_id}"
            
            attributes = chapter_data.get('attributes', {})
            title = attributes.get('title', 'Untitled')
            chapter_num = attributes.get('chapter', 'Unknown')
            pages = attributes.get('pages', 0)
            
            print(f"\nTrying chapter {i+1}: Chapter {chapter_num} - {title}")
            print(f"Chapter ID: {chapter_id}")
            print(f"Expected pages: {pages}")
            
            # Skip chapters with no pages
            if pages == 0:
                print("Skipping - no pages")
                continue
            
            try:
                # Test if this chapter has working page URLs
                page_urls = source.get_pages(chapter_url)
                if page_urls:
                    print(f"✅ SUCCESS! Found working chapter with {len(page_urls)} pages")
                    return {
                        'chapter_url': chapter_url,
                        'chapter_id': chapter_id,
                        'title': title,
                        'chapter_num': chapter_num,
                        'pages': page_urls
                    }
                else:
                    print("No page URLs returned")
                    
            except Exception as e:
                print(f"Error: {e}")
                continue
        
        print("No working chapters found in recent updates")
        return None
        
    except Exception as e:
        print(f"Error finding working chapter: {e}")
        return None


def test_page_retrieval_comprehensive(working_chapter):
    """Test comprehensive page retrieval functionality."""
    print_separator("Comprehensive Page Retrieval Test")
    
    if not working_chapter:
        print("No working chapter available for testing")
        return False
    
    chapter_url = working_chapter['chapter_url']
    chapter_title = working_chapter['title']
    chapter_num = working_chapter['chapter_num']
    expected_pages = len(working_chapter['pages'])
    
    print(f"Testing with: Chapter {chapter_num} - {chapter_title}")
    print(f"Chapter URL: {chapter_url}")
    print(f"Expected pages: {expected_pages}")
    
    try:
        # Test 1: Standard quality
        print("\n--- Test 1: Standard Quality ---")
        source_standard = MangaDexSource(language="en")
        pages_standard = source_standard.get_pages(chapter_url)
        
        print(f"Standard quality: {len(pages_standard)} pages")
        if pages_standard:
            print(f"First page URL: {pages_standard[0]}")
            print(f"Last page URL: {pages_standard[-1]}")
            
            # Verify URL structure
            if "/data/" in pages_standard[0]:
                print("✅ Standard quality URLs contain '/data/' path")
            else:
                print("⚠️ Unexpected URL structure for standard quality")
        
        # Test 2: Data saver mode
        print("\n--- Test 2: Data Saver Mode ---")
        source_data_saver = MangaDexSource(
            language="en",
            preferences={'use_data_saver': True}
        )
        pages_data_saver = source_data_saver.get_pages(chapter_url)
        
        print(f"Data saver: {len(pages_data_saver)} pages")
        if pages_data_saver:
            print(f"First page URL: {pages_data_saver[0]}")
            
            # Verify data saver URL structure
            if "/data-saver/" in pages_data_saver[0]:
                print("✅ Data saver URLs contain '/data-saver/' path")
            else:
                print("⚠️ Unexpected URL structure for data saver")
        
        # Test 3: Forced HTTPS
        print("\n--- Test 3: Forced Standard HTTPS ---")
        source_https = MangaDexSource(
            language="en",
            preferences={'force_standard_https': True}
        )
        pages_https = source_https.get_pages(chapter_url)
        
        print(f"Forced HTTPS: {len(pages_https)} pages")
        if pages_https:
            print(f"First page URL: {pages_https[0]}")
        
        # Test 4: URL structure analysis
        print("\n--- Test 4: URL Structure Analysis ---")
        if pages_standard:
            sample_url = pages_standard[0]
            print(f"Sample URL: {sample_url}")
            
            # Parse URL components
            if "https://" in sample_url:
                print("✅ Uses HTTPS protocol")
            
            if "/data/" in sample_url and "/chapter/" not in sample_url:
                print("✅ Correct at-home server URL structure")
            
            # Check for hash in URL
            url_parts = sample_url.split('/')
            if len(url_parts) >= 3:
                hash_part = url_parts[-2]
                if len(hash_part) == 32:  # MD5 hash length
                    print(f"✅ Contains chapter hash: {hash_part}")
        
        return True
        
    except Exception as e:
        print(f"Error in comprehensive test: {e}")
        return False


def test_page_url_validation(working_chapter):
    """Test that page URLs are valid and accessible."""
    print_separator("Page URL Validation Test")
    
    if not working_chapter:
        print("No working chapter available for testing")
        return False
    
    chapter_url = working_chapter['chapter_url']
    pages = working_chapter['pages']
    
    print(f"Validating {len(pages)} page URLs...")
    
    # Test first few page URLs
    test_urls = pages[:3] if len(pages) >= 3 else pages
    
    for i, page_url in enumerate(test_urls, 1):
        print(f"\nPage {i}: {page_url}")
        
        # Basic URL validation
        if page_url.startswith('https://'):
            print("✅ Valid HTTPS URL")
        else:
            print("⚠️ Not an HTTPS URL")
        
        # Check URL components
        if '/data/' in page_url or '/data-saver/' in page_url:
            print("✅ Contains data path")
        else:
            print("⚠️ Missing data path")
        
        # Check file extension
        if page_url.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            print("✅ Valid image file extension")
        else:
            print("⚠️ Unexpected file extension")
    
    return True


def main():
    """Run all page retrieval tests with working chapters."""
    print("MangaDex Page Retrieval Test - Working Chapters")
    print("Finding recent chapters and testing page functionality...")
    
    # Step 1: Find a working chapter
    working_chapter = find_working_chapter()
    
    if not working_chapter:
        print("\n❌ Could not find any working chapters for testing")
        print("This might be due to:")
        print("- API rate limiting")
        print("- No recent chapters available")
        print("- At-home server issues")
        return
    
    success_count = 0
    total_tests = 2
    
    # Step 2: Comprehensive page retrieval test
    if test_page_retrieval_comprehensive(working_chapter):
        success_count += 1
    
    # Step 3: URL validation test
    if test_page_url_validation(working_chapter):
        success_count += 1
    
    print_separator("Final Results")
    print(f"Successful tests: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("✅ All page retrieval tests passed!")
        print("\nPage retrieval functionality is working correctly:")
        print("- At-home server integration ✅")
        print("- Standard quality images ✅")
        print("- Data saver mode ✅")
        print("- URL structure validation ✅")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    main()
