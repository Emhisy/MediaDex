#!/usr/bin/env python3
"""
Test with a manga that was working before
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extensions.batoto import BatoToSource


def test_working_manga():
    """Test with manga ID:5753 that was working before"""
    print("=== Testing Working Manga ===")
    
    source = BatoToSource()
    
    # Test with the manga that worked before
    print("1. Testing ID:5753...")
    results = source.search('ID:5753')
    
    if not results:
        print("❌ No results found")
        return
    
    manga_url = results[0]['url']
    manga_title = results[0]['title']
    print(f"✅ Found: {manga_title}")
    print(f"   URL: {manga_url}")
    
    # Get chapters
    print("\n2. Getting chapters...")
    chapters = source.get_chapters(manga_url)
    
    if not chapters:
        print("❌ No chapters found")
        return
    
    print(f"✅ Found {len(chapters)} chapters")
    
    # Test first chapter
    chapter = chapters[0]
    print(f"\n3. Testing chapter: {chapter['title']}")
    print(f"   URL: {chapter['url']}")
    
    pages = source.get_pages(chapter['url'])
    print(f"   Found {len(pages)} pages")
    
    if pages:
        print(f"   First page: {pages[0]}")
        print(f"   Last page: {pages[-1]}")
        
        # Check if crypto worked
        if len(pages) > 1 and 'history' not in pages[0]:
            print("✅ Crypto and page extraction working!")
            return True
        elif len(pages) > 0:
            print("⚠️ Fallback extraction working")
            return True
        else:
            print("❌ No valid pages found")
            return False
    else:
        print("❌ No pages found")
        return False


if __name__ == "__main__":
    success = test_working_manga()
    
    if success:
        print("\n🎉 Implementation is working correctly!")
    else:
        print("\n⚠️ Issues detected with page extraction")
