#!/usr/bin/env python3
"""
Diagnostic script for problematic chapters
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
from bs4 import BeautifulSoup
from extensions.batoto import BatoToSource


def diagnose_chapter(chapter_url):
    """Diagnose a problematic chapter"""
    print(f"=== Diagnosing Chapter ===")
    print(f"URL: {chapter_url}")
    
    try:
        response = requests.get(chapter_url)
        response.raise_for_status()
        
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)}")
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Check for error messages
        print("\n--- Checking for error messages ---")
        error_selectors = [
            ".alert-danger",
            ".alert-warning", 
            ".error",
            ".message",
            "div:contains('deleted')",
            "div:contains('removed')",
            "div:contains('not available')"
        ]
        
        for selector in error_selectors:
            elements = soup.select(selector)
            if elements:
                for elem in elements:
                    print(f"Found error/warning: {elem.text.strip()}")
        
        # Check for crypto elements
        print("\n--- Checking for crypto elements ---")
        has_img_https = "imgHttps" in response.text
        has_bato_word = "batoWord" in response.text
        has_bato_pass = "batoPass" in response.text
        
        print(f"imgHttps found: {has_img_https}")
        print(f"batoWord found: {has_bato_word}")
        print(f"batoPass found: {has_bato_pass}")
        
        # Look for images
        print("\n--- Looking for images ---")
        img_selectors = [
            "img",
            ".page-img",
            ".reader-image",
            "img[data-src]"
        ]
        
        all_images = []
        for selector in img_selectors:
            images = soup.select(selector)
            print(f"Selector '{selector}': {len(images)} images")
            for img in images[:3]:  # Show first 3
                src = img.get('src') or img.get('data-src')
                if src:
                    all_images.append(src)
                    print(f"  - {src}")
        
        # Check page structure
        print("\n--- Page structure analysis ---")
        main_content = soup.select_one("#mainer, .main, .content, .reader")
        if main_content:
            print(f"Main content area found: {main_content.name}")
            print(f"Content length: {len(main_content.text)}")
        else:
            print("No main content area found")
        
        # Look for navigation
        print("\n--- Navigation elements ---")
        nav_selectors = [
            "a[href*='/chapter/']",
            ".nav a",
            ".chapter-nav a",
            ".pagination a"
        ]
        
        for selector in nav_selectors:
            links = soup.select(selector)
            if links:
                print(f"Selector '{selector}': {len(links)} links")
                for link in links[:3]:
                    href = link.get('href')
                    text = link.text.strip()
                    if href and text:
                        print(f"  - {text}: {href}")
        
        # Check for scripts
        print("\n--- Script analysis ---")
        scripts = soup.find_all("script")
        print(f"Found {len(scripts)} script tags")
        
        for i, script in enumerate(scripts):
            if script.string and any(keyword in script.string for keyword in ['img', 'page', 'chapter']):
                print(f"Script {i+1} contains relevant keywords")
                content = script.string[:200] + "..." if len(script.string) > 200 else script.string
                print(f"  Content preview: {content}")
        
        return all_images
        
    except Exception as e:
        print(f"Error diagnosing chapter: {e}")
        return []


def test_different_chapters():
    """Test different chapters to find working ones"""
    print("\n=== Testing Different Chapters ===")
    
    source = BatoToSource()
    
    # Get Bleach chapters
    manga_url = "https://batotwo.com/series/5753"
    chapters = source.get_chapters(manga_url)
    
    print(f"Found {len(chapters)} chapters")
    
    # Test a few different chapters
    test_chapters = chapters[:5] + chapters[-5:]  # First 5 and last 5
    
    for i, chapter in enumerate(test_chapters):
        print(f"\n--- Testing Chapter {i+1}: {chapter['title']} ---")
        print(f"URL: {chapter['url']}")
        
        try:
            pages = source.get_pages(chapter['url'])
            print(f"Found {len(pages)} pages")
            
            if pages:
                print(f"First page: {pages[0]}")
                # Check if it's a real image URL or history page
                if "history" in pages[0]:
                    print("⚠ This appears to be a history page, not actual content")
                else:
                    print("✓ This appears to be actual content")
                    return chapter['url']  # Return first working chapter
            else:
                print("✗ No pages found")
                
        except Exception as e:
            print(f"✗ Error: {e}")
    
    return None


if __name__ == "__main__":
    print("BatoTo Chapter Diagnostic Tool")
    print("=" * 50)
    
    # Test the problematic chapter
    chapter_url = "https://batotwo.com/chapter/107355"
    images = diagnose_chapter(chapter_url)
    
    # Test different chapters
    working_chapter = test_different_chapters()
    
    if working_chapter:
        print(f"\n=== Found working chapter: {working_chapter} ===")
        diagnose_chapter(working_chapter)
    else:
        print("\n⚠ No working chapters found for this manga")
