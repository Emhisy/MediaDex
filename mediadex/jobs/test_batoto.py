#!/usr/bin/env python3
"""
Test script for BatoTo source implementation.
Tests search, chapter listing, and page extraction with crypto decryption.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extensions.batoto import BatoToSource
from crytoaes import get_decrypted_image_urls
import requests


def test_search():
    """Test manga search functionality"""
    print("=== Testing Search Functionality ===")
    source = BatoToSource()
    
    # Test text search
    print("\n1. Testing text search for 'one piece':")
    results = source.search("one piece official")
    print(f"Found {len(results)} results")
    for i, result in enumerate(results[:3], 1):
        print(f"  {i}. {result['title']}")
        print(f"     URL: {result['url']}")
        if 'thumbnail' in result:
            print(f"     Thumbnail: {result['thumbnail']}")
    
    # Test ID search
    print("\n2. Testing ID search:")
    id_results = source.search("ID:5753")
    if id_results:
        print(f"Found: {id_results[0]['title']}")
        print(f"URL: {id_results[0]['url']}")
        return id_results[0]['url']
    else:
        print("No results for ID search")
        return results[0]['url'] if results else None


def test_chapters(manga_url):
    """Test chapter listing functionality"""
    print(f"\n=== Testing Chapter Listing ===")
    print(f"Manga URL: {manga_url}")
    
    source = BatoToSource()
    chapters = source.get_chapters(manga_url)
    
    print(f"Found {len(chapters)} chapters")
    for i, chapter in enumerate(chapters[:5], 1):
        print(f"  {i}. {chapter['title']}")
        print(f"     URL: {chapter['url']}")
        if 'scanlator' in chapter:
            print(f"     Scanlator: {chapter['scanlator']}")
        if 'upload_time' in chapter:
            print(f"     Upload time: {chapter['upload_time']}")
    
    return chapters[0]['url'] if chapters else None


def test_pages(chapter_url):
    """Test page extraction with crypto decryption"""
    print(f"\n=== Testing Page Extraction ===")
    print(f"Chapter URL: {chapter_url}")
    
    source = BatoToSource()
    pages = source.get_pages(chapter_url)
    
    print(f"Found {len(pages)} pages")
    for i, page_url in enumerate(pages[:3], 1):
        print(f"  {i}. {page_url}")
    
    if pages:
        print(f"\nFirst page URL: {pages[0]}")
        print(f"Last page URL: {pages[-1]}")
    
    return pages


def test_crypto_directly(chapter_url):
    """Test crypto decryption directly"""
    print(f"\n=== Testing Crypto Decryption Directly ===")
    print(f"Chapter URL: {chapter_url}")
    
    try:
        response = requests.get(chapter_url)
        response.raise_for_status()
        
        decrypted_urls = get_decrypted_image_urls(response.text)
        print(f"Crypto decryption successful! Found {len(decrypted_urls)} images")
        
        for i, url in enumerate(decrypted_urls[:3], 1):
            print(f"  {i}. {url}")
        
        return True
        
    except Exception as e:
        print(f"Crypto decryption failed: {e}")
        return False


def test_manga_details(manga_url):
    """Test manga details extraction"""
    print(f"\n=== Testing Manga Details ===")
    
    source = BatoToSource()
    details = source.get_manga_details(manga_url)
    
    if details:
        print("Manga details:")
        for key, value in details.items():
            if isinstance(value, list):
                print(f"  {key}: {', '.join(value)}")
            else:
                print(f"  {key}: {value}")
    else:
        print("No details found")
    
    return details


def test_navigation(chapter_url, manga_url):
    """Test chapter navigation functionality"""
    print(f"\n=== Testing Chapter Navigation ===")
    print(f"Chapter URL: {chapter_url}")
    
    source = BatoToSource()
    
    try:
        # Test next chapter
        next_chapter = source.get_next_chapter(chapter_url, manga_url)
        print(f"Next chapter: {next_chapter}")
        
        # Test previous chapter
        prev_chapter = source.get_previous_chapter(chapter_url, manga_url)
        print(f"Previous chapter: {prev_chapter}")
        
        # Test navigation method
        navigation = source.get_chapter_navigation(chapter_url, manga_url)
        print(f"Navigation result: {navigation}")
        
        # Test auto-extraction
        auto_next = source.get_next_chapter(chapter_url)
        auto_prev = source.get_previous_chapter(chapter_url)
        print(f"Auto-extracted next: {auto_next}")
        print(f"Auto-extracted previous: {auto_prev}")
        
        # Consider successful if we can get at least one navigation direction
        success = next_chapter is not None or prev_chapter is not None
        
        if success:
            print("✓ Chapter navigation working")
        else:
            print("⚠ Chapter navigation may need adjustment")
        
        return success
        
    except Exception as e:
        print(f"Navigation test failed: {e}")
        return False


def main():
    """Main test function"""
    print("BatoTo Source Implementation Test")
    print("=" * 50)
    
    try:
        # Test search
        manga_url = test_search()
        if not manga_url:
            print("Search test failed, cannot continue")
            return
        
        # Test manga details
        test_manga_details(manga_url)
        
        # Test chapters
        chapter_url = test_chapters(manga_url)
        if not chapter_url:
            print("Chapter listing test failed, cannot continue")
            return
        
        # Test crypto decryption directly
        crypto_success = test_crypto_directly(chapter_url)
        
        # Test page extraction
        pages = test_pages(chapter_url)
        
        # Test navigation
        navigation_success = test_navigation(chapter_url, manga_url)
        
        # Summary
        print(f"\n=== Test Summary ===")
        print(f"✓ Search: Working")
        print(f"✓ Chapters: Working")
        print(f"{'✓' if crypto_success else '✗'} Crypto decryption: {'Working' if crypto_success else 'Failed'}")
        print(f"{'✓' if pages else '✗'} Page extraction: {'Working' if pages else 'Failed'}")
        print(f"{'✓' if navigation_success else '✗'} Chapter navigation: {'Working' if navigation_success else 'Failed'}")
        
        if pages and navigation_success:
            print("\n🎉 All core tests passed! BatoTo implementation is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Check the error messages above.")
    
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
