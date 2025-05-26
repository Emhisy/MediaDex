#!/usr/bin/env python3
"""
Debug script to analyze crypto extraction step by step
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import re
import json
from crytoaes import extract_script_data, Deobfuscator, CryptoAES

def debug_crypto_extraction(chapter_url):
    """Debug crypto extraction step by step"""
    print(f"=== Debugging {chapter_url} ===")
    
    try:
        response = requests.get(chapter_url)
        response.raise_for_status()
        html = response.text
        
        print("1. Extracting script data...")
        img_https, bato_word, bato_pass = extract_script_data(html)
        
        print(f"   imgHttps: {len(img_https)} URLs")
        print(f"   First URL: {img_https[0] if img_https else 'None'}")
        print(f"   batoWord: {bato_word[:50]}..." if len(bato_word) > 50 else f"   batoWord: {bato_word}")
        print(f"   batoPass: {bato_pass}")
        
        print("\n2. Deobfuscating password...")
        evaluated_pass = Deobfuscator.deobfuscate_js_password(bato_pass)
        print(f"   Original: {bato_pass}")
        print(f"   Deobfuscated: {evaluated_pass}")
        
        print("\n3. Attempting decryption...")
        try:
            img_acc_list_str = CryptoAES.decrypt(bato_word, evaluated_pass)
            print(f"   ✓ Decryption successful!")
            print(f"   Decrypted: {img_acc_list_str[:100]}..." if len(img_acc_list_str) > 100 else f"   Decrypted: {img_acc_list_str}")
            
            img_acc_list = json.loads(img_acc_list_str)
            print(f"   Access list length: {len(img_acc_list)}")
            print(f"   First access param: {img_acc_list[0] if img_acc_list else 'None'}")
            
            return True
            
        except Exception as decrypt_error:
            print(f"   ✗ Decryption failed: {decrypt_error}")
            
            # Try some variations of the password
            print("\n4. Trying password variations...")
            variations = [
                evaluated_pass.strip(),
                evaluated_pass.replace('.', ''),
                evaluated_pass.replace('-', ''),
                evaluated_pass + '.',
                '.' + evaluated_pass,
            ]
            
            for i, variation in enumerate(variations):
                if variation != evaluated_pass:
                    try:
                        print(f"   Trying variation {i+1}: '{variation}'")
                        result = CryptoAES.decrypt(bato_word, variation)
                        print(f"   ✓ Success with variation {i+1}!")
                        return True
                    except Exception as e:
                        print(f"   ✗ Variation {i+1} failed: {e}")
            
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def analyze_script_content(chapter_url):
    """Analyze the actual script content to understand the structure"""
    print(f"\n=== Analyzing script content for {chapter_url} ===")
    
    try:
        response = requests.get(chapter_url)
        html = response.text
        
        # Find all scripts
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
        
        for i, script in enumerate(scripts):
            if any(var in script for var in ['imgHttps', 'batoWord', 'batoPass']):
                print(f"\nScript {i+1} contains crypto variables:")
                
                # Show relevant lines
                lines = script.split('\n')
                for j, line in enumerate(lines):
                    if any(var in line for var in ['imgHttps', 'batoWord', 'batoPass']):
                        print(f"  Line {j+1}: {line.strip()}")
                
                # Try to extract each variable manually
                print("\nManual extraction:")
                
                # imgHttps
                img_match = re.search(r'imgHttps\s*=\s*(\[.*?\]);', script, re.DOTALL)
                if img_match:
                    print(f"  imgHttps found: {img_match.group(1)[:100]}...")
                
                # batoWord
                word_match = re.search(r'batoWord\s*=\s*["\']([^"\']+)["\']', script)
                if word_match:
                    print(f"  batoWord found: {word_match.group(1)[:50]}...")
                
                # batoPass
                pass_match = re.search(r'batoPass\s*=\s*([^;]+);', script)
                if pass_match:
                    print(f"  batoPass found: {pass_match.group(1)}")
                
                break
        
    except Exception as e:
        print(f"Error analyzing script: {e}")

if __name__ == "__main__":
    test_urls = [
        "https://batotwo.com/chapter/2071732",
        "https://batotwo.com/chapter/2510359",
    ]
    
    for url in test_urls:
        debug_crypto_extraction(url)
        analyze_script_content(url)
        print("\n" + "="*80 + "\n")
