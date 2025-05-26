#!/usr/bin/env python3
"""
Test script for chapter navigation functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extensions.batoto import BatoToSource


def test_chapter_navigation():
    """Test chapter navigation functionality"""
    print("=== Testing Chapter Navigation ===")
    
    source = BatoToSource()
    
    # Search for a manga with multiple chapters
    print("\n1. Searching for manga...")
    results = source.search("ID:5753")
    
    if not results:
        print("No manga found")
        return
    
    manga_url = results[0]['url']
    manga_title = results[0]['title']
    print(f"Testing with: {manga_title}")
    print(f"URL: {manga_url}")
    
    # Get chapters
    print("\n2. Getting chapters...")
    chapters = source.get_chapters(manga_url)
    
    if len(chapters) < 2:
        print(f"Not enough chapters for navigation test ({len(chapters)} chapters)")
        return
    
    print(f"Found {len(chapters)} chapters")
    
    # Test navigation with middle chapter
    if len(chapters) >= 3:
        test_chapter = chapters[1]  # Middle chapter
        print(f"\n3. Testing navigation from: {test_chapter['title']}")
        print(f"Chapter URL: {test_chapter['url']}")
        
        # Test next chapter
        print("\n4. Testing next chapter...")
        next_chapter = source.get_next_chapter(test_chapter['url'], manga_url)
        if next_chapter:
            print(f"✓ Next chapter found: {next_chapter}")
            # Verify it's actually the next chapter
            expected_next = chapters[0]['url']  # Should be newer chapter
            if next_chapter == expected_next:
                print("✓ Next chapter is correct")
            else:
                print(f"⚠ Next chapter mismatch. Expected: {expected_next}")
        else:
            print("✗ No next chapter found")
        
        # Test previous chapter
        print("\n5. Testing previous chapter...")
        prev_chapter = source.get_previous_chapter(test_chapter['url'], manga_url)
        if prev_chapter:
            print(f"✓ Previous chapter found: {prev_chapter}")
            # Verify it's actually the previous chapter
            expected_prev = chapters[2]['url']  # Should be older chapter
            if prev_chapter == expected_prev:
                print("✓ Previous chapter is correct")
            else:
                print(f"⚠ Previous chapter mismatch. Expected: {expected_prev}")
        else:
            print("✗ No previous chapter found")
        
        # Test navigation method
        print("\n6. Testing get_chapter_navigation...")
        navigation = source.get_chapter_navigation(test_chapter['url'], manga_url)
        print(f"Navigation result: {navigation}")
        
        # Test navigation from page
        print("\n7. Testing navigation from chapter page...")
        page_navigation = source.get_chapter_navigation_from_page(test_chapter['url'])
        print(f"Page navigation result: {page_navigation}")
        
        # Test edge cases
        print("\n8. Testing edge cases...")
        
        # First chapter (should have no next)
        first_chapter = chapters[0]
        print(f"Testing first chapter: {first_chapter['title']}")
        first_next = source.get_next_chapter(first_chapter['url'], manga_url)
        first_prev = source.get_previous_chapter(first_chapter['url'], manga_url)
        print(f"  Next: {first_next} (should be None)")
        print(f"  Previous: {first_prev} (should exist)")
        
        # Last chapter (should have no previous)
        last_chapter = chapters[-1]
        print(f"Testing last chapter: {last_chapter['title']}")
        last_next = source.get_next_chapter(last_chapter['url'], manga_url)
        last_prev = source.get_previous_chapter(last_chapter['url'], manga_url)
        print(f"  Next: {last_next} (should exist)")
        print(f"  Previous: {last_prev} (should be None)")
        
        # Test without manga_url (auto-extraction)
        print("\n9. Testing auto-extraction of manga URL...")
        auto_next = source.get_next_chapter(test_chapter['url'])
        auto_prev = source.get_previous_chapter(test_chapter['url'])
        print(f"  Auto next: {auto_next}")
        print(f"  Auto previous: {auto_prev}")
        
        if auto_next == next_chapter and auto_prev == prev_chapter:
            print("✓ Auto-extraction works correctly")
        else:
            print("⚠ Auto-extraction may have issues")


def test_manga_url_extraction():
    """Test manga URL extraction from chapter URL"""
    print("\n=== Testing Manga URL Extraction ===")
    
    source = BatoToSource()
    
    # Get a test chapter URL
    results = source.search("ID:5753")
    if results:
        manga_url = results[0]['url']
        chapters = source.get_chapters(manga_url)
        
        if chapters:
            chapter_url = chapters[0]['url']
            print(f"Testing extraction from: {chapter_url}")
            
            extracted_url = source._extract_manga_url_from_chapter(chapter_url)
            print(f"Extracted manga URL: {extracted_url}")
            print(f"Original manga URL: {manga_url}")
            
            if extracted_url == manga_url:
                print("✓ Manga URL extraction is correct")
            else:
                print("⚠ Manga URL extraction may need adjustment")


if __name__ == "__main__":
    print("BatoTo Chapter Navigation Test")
    print("=" * 50)
    
    try:
        test_chapter_navigation()
        test_manga_url_extraction()
        
        print("\n" + "=" * 50)
        print("Navigation test completed!")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
