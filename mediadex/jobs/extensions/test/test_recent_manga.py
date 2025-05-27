#!/usr/bin/env python3
"""
Test with a recent manga to verify our implementation works
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extensions.batoto import BatoToSource


def test_recent_manga():
    """Test with One Piece (recent manga)"""
    print("=== Testing Recent Manga ===")
    
    source = BatoToSource()
    
    # Search for One Piece
    print("1. Searching for 'one piece'...")
    results = source.search('one piece')
    
    if not results:
        print("❌ No search results")
        return False
    
    # Use first result
    manga = results[0]
    print(f"✅ Found: {manga['title']}")
    print(f"   URL: {manga['url']}")
    
    # Get chapters
    print("\n2. Getting chapters...")
    chapters = source.get_chapters(manga['url'])
    
    if not chapters:
        print("❌ No chapters found")
        return False
    
    print(f"✅ Found {len(chapters)} chapters")
    
    # Test first chapter (most recent)
    chapter = chapters[0]
    print(f"\n3. Testing chapter: {chapter['title']}")
    print(f"   URL: {chapter['url']}")
    
    pages = source.get_pages(chapter['url'])
    print(f"   Found {len(pages)} pages")
    
    if pages:
        print(f"   First page: {pages[0]}")
        if len(pages) > 1:
            print(f"   Last page: {pages[-1]}")
        
        # Check if pages look valid
        valid_pages = [p for p in pages if 'http' in p and 'history' not in p]
        print(f"   Valid pages: {len(valid_pages)}")
        
        if valid_pages:
            print("✅ Page extraction working!")
            return True
        else:
            print("⚠️ Pages found but may not be valid")
            return False
    else:
        print("❌ No pages found")
        return False


if __name__ == "__main__":
    success = test_recent_manga()
    
    if success:
        print("\n🎉 Recent manga test successful!")
    else:
        print("\n⚠️ Recent manga test failed")
