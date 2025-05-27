#!/usr/bin/env python3
"""
Direct test of crypto functionality with a known encrypted chapter
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
from crytoaes import get_decrypted_image_urls

def test_direct_crypto():
    """Test crypto decryption directly on a chapter URL"""
    
    # Test with a recent chapter that should have crypto
    test_urls = [
        "https://batotwo.com/chapter/3313537",  # One Piece chapter
        "https://batotwo.com/chapter/1931726",  # Previous test chapter
    ]
    
    for chapter_url in test_urls:
        print(f"\n=== Testing {chapter_url} ===")
        
        try:
            response = requests.get(chapter_url)
            response.raise_for_status()
            
            # Check if the page contains the crypto script elements
            html = response.text
            
            print("Checking for crypto elements in HTML...")
            has_img_https = "imgHttps" in html
            has_bato_word = "batoWord" in html  
            has_bato_pass = "batoPass" in html
            
            print(f"  imgHttps found: {has_img_https}")
            print(f"  batoWord found: {has_bato_word}")
            print(f"  batoPass found: {has_bato_pass}")
            
            if has_img_https and has_bato_word and has_bato_pass:
                print("  ✓ All crypto elements found - attempting decryption...")
                
                try:
                    decrypted_urls = get_decrypted_image_urls(html)
                    print(f"  ✓ Crypto decryption successful! Found {len(decrypted_urls)} images")
                    
                    if decrypted_urls:
                        print("  Sample decrypted URLs:")
                        for i, url in enumerate(decrypted_urls[:3], 1):
                            print(f"    {i}. {url}")
                        
                        # Check for access parameters
                        crypto_urls = [u for u in decrypted_urls if '?' in u]
                        print(f"  URLs with access parameters: {len(crypto_urls)}")
                        
                        return True
                        
                except Exception as e:
                    print(f"  ✗ Crypto decryption failed: {e}")
            else:
                print("  ⚠ Missing crypto elements - this chapter may not use encryption")
                
                # Try to find any script tags for debugging
                import re
                scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
                print(f"  Found {len(scripts)} script tags")
                
                for i, script in enumerate(scripts):
                    if any(keyword in script for keyword in ['img', 'image', 'page']):
                        print(f"    Script {i+1} contains image-related content")
                        if len(script) > 200:
                            print(f"      Preview: {script[:200]}...")
                        else:
                            print(f"      Content: {script}")
                        
        except Exception as e:
            print(f"  ✗ Error fetching chapter: {e}")
    
    return False

def search_for_recent_manga():
    """Search for very recent manga that might use crypto"""
    from extensions.batoto import BatoToSource
    
    source = BatoToSource()
    
    # Try searching for popular ongoing manga
    search_terms = ["chainsaw man", "jujutsu kaisen", "demon slayer", "attack on titan"]
    
    for term in search_terms:
        print(f"\n=== Searching for '{term}' ===")
        results = source.search(term)
        
        if results:
            manga_url = results[0]['url']
            print(f"Found: {results[0]['title']}")
            
            chapters = source.get_chapters(manga_url)
            if chapters:
                # Try the most recent chapter
                recent_chapter = chapters[0]['url']
                print(f"Testing recent chapter: {chapters[0]['title']}")
                print(f"URL: {recent_chapter}")
                
                # Test this chapter
                try:
                    response = requests.get(recent_chapter)
                    html = response.text
                    
                    if all(keyword in html for keyword in ["imgHttps", "batoWord", "batoPass"]):
                        print("✓ Found crypto elements! Testing decryption...")
                        try:
                            decrypted_urls = get_decrypted_image_urls(html)
                            print(f"✓ Success! Found {len(decrypted_urls)} decrypted images")
                            return recent_chapter
                        except Exception as e:
                            print(f"✗ Decryption failed: {e}")
                    else:
                        print("⚠ No crypto elements found")
                        
                except Exception as e:
                    print(f"✗ Error: {e}")
    
    return None

if __name__ == "__main__":
    print("Testing BatoTo Crypto Decryption")
    print("=" * 50)
    
    # First try direct testing
    success = test_direct_crypto()
    
    if not success:
        print("\n" + "=" * 50)
        print("Direct test failed, searching for recent manga...")
        recent_url = search_for_recent_manga()
        
        if recent_url:
            print(f"\nFound crypto-enabled chapter: {recent_url}")
        else:
            print("\nNo crypto-enabled chapters found in search")
            print("This might indicate:")
            print("1. BatoTo has changed their crypto implementation")
            print("2. The test manga don't use crypto")
            print("3. The crypto detection needs adjustment")
