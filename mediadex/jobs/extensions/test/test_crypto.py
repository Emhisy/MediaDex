#!/usr/bin/env python3
"""
Simple test for crypto decryption on a recent chapter
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extensions.batoto import BatoToSource
import requests

def test_recent_chapter():
    """Test crypto decryption on a recent chapter"""
    source = BatoToSource()
    
    # Search for a popular manga
    print("Searching for 'one piece'...")
    results = source.search("one piece")
    
    if not results:
        print("No search results found")
        return
    
    # Try the second result (One Piece: Road to Laugh Tale)
    manga_url = results[1]['url']
    print(f"Testing manga: {results[1]['title']}")
    print(f"URL: {manga_url}")
    
    # Get chapters
    chapters = source.get_chapters(manga_url)
    if not chapters:
        print("No chapters found")
        return
    
    print(f"Found {len(chapters)} chapters")
    
    # Test the first chapter
    chapter_url = chapters[0]['url']
    print(f"Testing chapter: {chapters[0]['title']}")
    print(f"Chapter URL: {chapter_url}")
    
    # Get pages
    pages = source.get_pages(chapter_url)
    print(f"Found {len(pages)} pages")
    
    if pages:
        print("Sample pages:")
        for i, page in enumerate(pages[:3], 1):
            print(f"  {i}. {page}")
        
        # Check if URLs contain access parameters (sign of successful crypto)
        crypto_urls = [p for p in pages if '?' in p and ('acc=' in p or len(p.split('?')[1]) > 10)]
        print(f"Pages with crypto parameters: {len(crypto_urls)}")
        
        if crypto_urls:
            print("✓ Crypto decryption appears to be working!")
            print(f"Example crypto URL: {crypto_urls[0]}")
        else:
            print("⚠ No crypto parameters detected - may be fallback extraction")
    else:
        print("No pages found")

if __name__ == "__main__":
    test_recent_chapter()
