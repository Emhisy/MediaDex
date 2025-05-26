import re
import base64
import json
from Crypto.Cipher import AES
from hashlib import md5
from typing import List, Tuple
from bs4 import BeautifulSoup


class Deobfuscator:
    """JavaScript deobfuscation utility class"""
    
    @staticmethod
    def deobfuscate_js_password(obfuscated_js: str) -> str:
        """
        Deobfuscates JavaScript password following Kotlin implementation.
        This handles JSFuck-style obfuscation patterns.
        """
        # Remove quotes if present
        js_code = obfuscated_js.strip().strip('"').strip("'")
        
        # Handle simple string literals first
        if not any(char in js_code for char in ['[', ']', '(', ')', '!', '+']):
            return js_code
        
        # For JSFuck patterns, we need to evaluate the mathematical expressions
        # This is a simplified version that handles common patterns
        result = []
        i = 0
        
        while i < len(js_code):
            if js_code[i:i+4] == '!+[]':
                # !+[] evaluates to 1 in JavaScript
                result.append('1')
                i += 4
            elif js_code[i:i+3] == '+[]':
                # +[] evaluates to 0 in JavaScript
                result.append('0')
                i += 3
            elif js_code[i] == '[':
                # Find matching bracket and count !+[] patterns inside
                bracket_count = 1
                j = i + 1
                inner_ones = 0
                
                while j < len(js_code) and bracket_count > 0:
                    if js_code[j] == '[':
                        bracket_count += 1
                    elif js_code[j] == ']':
                        bracket_count -= 1
                    elif js_code[j:j+4] == '!+[]':
                        inner_ones += 1
                        j += 3  # Will be incremented by 1 at end of loop
                    j += 1
                
                if inner_ones > 0:
                    result.append(str(inner_ones))
                else:
                    result.append('0')
                i = j
            elif js_code[i] == '+':
                # Skip standalone + operators
                i += 1
            elif js_code[i] == '.':
                result.append('.')
                i += 1
            else:
                # For other characters, try to preserve them or skip
                if js_code[i].isalnum() or js_code[i] in '.-_':
                    result.append(js_code[i])
                i += 1
        
        return ''.join(result)


class CryptoAES:
    """AES encryption/decryption utility class following Java implementation exactly"""
    
    @staticmethod
    def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int = 32, iv_len: int = 16) -> Tuple[bytes, bytes]:
        """
        Equivalent to OpenSSL's EVP_BytesToKey function.
        Derives key and IV from password and salt.
        """
        d = b''
        while len(d) < key_len + iv_len:
            if d:
                d_i = md5(d[-16:] + password + salt).digest()
            else:
                d_i = md5(password + salt).digest()
            d += d_i
        return d[:key_len], d[key_len:key_len + iv_len]
    
    @staticmethod
    def decrypt(ciphertext: str, password: str) -> str:
        """
        Decrypts AES-encrypted data following Java CryptoAES implementation exactly.
        Returns empty string on any error (like Java version).
        """
        try:
            # Decode base64 - following Java: Base64.decode(cipherText, Base64.DEFAULT)
            ct_bytes = base64.b64decode(ciphertext)
            
            # Extract salt and cipher data - following Java implementation
            salt_bytes = ct_bytes[8:16]  # Arrays.copyOfRange(ctBytes, 8, 16)
            cipher_text_bytes = ct_bytes[16:]  # Arrays.copyOfRange(ctBytes, 16, ctBytes.size)
            
            # Generate key and IV using MD5 - following Java implementation
            key_and_iv = CryptoAES._generate_key_and_iv(
                32, 16, 1, salt_bytes, password.encode('utf-8')
            )
            
            if not key_and_iv:
                return ""
            
            key_bytes = key_and_iv[0] if key_and_iv[0] else bytes(32)
            iv_bytes = key_and_iv[1] if key_and_iv[1] else bytes(16)
            
            # Decrypt AES - following Java decryptAES method
            return CryptoAES._decrypt_aes(cipher_text_bytes, key_bytes, iv_bytes)
            
        except Exception:
            # Following Java: catch (e: Exception) { "" }
            return ""
    
    @staticmethod
    def _decrypt_aes(cipher_text_bytes: bytes, key_bytes: bytes, iv_bytes: bytes) -> str:
        """
        Decrypt AES following Java implementation exactly.
        Returns empty string on any error.
        """
        try:
            # Following Java: Cipher.getInstance(HASH_CIPHER) where HASH_CIPHER = "AES/CBC/PKCS7PADDING"
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
            
            # Decrypt
            decrypted = cipher.decrypt(cipher_text_bytes)
            
            # Convert to string - following Java: .toString(Charsets.UTF_8)
            return decrypted.decode('utf-8')
            
        except Exception:
            # Following Java: catch (e: Exception) { "" }
            return ""
    
    @staticmethod
    def _generate_key_and_iv(key_length: int, iv_length: int, iterations: int, 
                           salt: bytes, password: bytes) -> Tuple[bytes, bytes]:
        """
        Generate key and IV following Java implementation exactly.
        """
        try:
            digest_length = 16  # MD5 digest length
            required_length = ((key_length + iv_length + digest_length - 1) // digest_length) * digest_length
            generated_data = bytearray(required_length)
            generated_length = 0
            
            # Repeat process until sufficient data has been generated
            while generated_length < key_length + iv_length:
                md5_hash = md5()
                
                # Digest data (last digest if available, password data, salt if available)
                if generated_length > 0:
                    md5_hash.update(generated_data[generated_length - digest_length:generated_length])
                
                md5_hash.update(password)
                md5_hash.update(salt[:8])  # salt, 0, 8
                
                digest = md5_hash.digest()
                generated_data[generated_length:generated_length + digest_length] = digest
                
                # Additional rounds
                for i in range(1, iterations):
                    md5_hash = md5()
                    md5_hash.update(generated_data[generated_length:generated_length + digest_length])
                    digest = md5_hash.digest()
                    generated_data[generated_length:generated_length + digest_length] = digest
                
                generated_length += digest_length
            
            # Copy key and IV into separate byte arrays
            key = bytes(generated_data[:key_length])
            iv = bytes(generated_data[key_length:key_length + iv_length]) if iv_length > 0 else b''
            
            return key, iv
            
        except Exception:
            return b'', b''


def extract_script_data(html: str) -> Tuple[List[str], str, str]:
    """
    Extracts imgHttps, batoWord, and batoPass from HTML following Kotlin implementation exactly.
    Returns tuple of (image_urls, encrypted_word, obfuscated_pass)
    """
    soup = BeautifulSoup(html, "html.parser")
    
    # Find script containing all three variables - exact match to Kotlin selector
    script = None
    for s in soup.find_all("script"):
        if s.string and all(var in s.string for var in ["imgHttps", "batoWord", "batoPass"]):
            script = s.string
            break
    
    if not script:
        raise RuntimeError("Couldn't find script with image data.")
    
    # Extract variables using substring methods like Kotlin
    try:
        # imgHttps - following Kotlin: script.substringAfter("const imgHttps =").substringBefore(";").trim()
        img_https_start = script.find("const imgHttps =")
        if img_https_start == -1:
            raise ValueError("imgHttps not found")
        img_https_start += len("const imgHttps =")
        img_https_end = script.find(";", img_https_start)
        if img_https_end == -1:
            raise ValueError("imgHttps end not found")
        img_https_str = script[img_https_start:img_https_end].strip()
        img_https = json.loads(img_https_str)
        
        # batoWord - following Kotlin: script.substringAfter("const batoWord =").substringBefore(";").trim()
        bato_word_start = script.find("const batoWord =")
        if bato_word_start == -1:
            raise ValueError("batoWord not found")
        bato_word_start += len("const batoWord =")
        bato_word_end = script.find(";", bato_word_start)
        if bato_word_end == -1:
            raise ValueError("batoWord end not found")
        bato_word = script[bato_word_start:bato_word_end].strip()
        # Remove surrounding quotes like Kotlin: .removeSurrounding("\"")
        if bato_word.startswith('"') and bato_word.endswith('"'):
            bato_word = bato_word[1:-1]
        elif bato_word.startswith("'") and bato_word.endswith("'"):
            bato_word = bato_word[1:-1]
        
        # batoPass - following Kotlin: script.substringAfter("const batoPass =").substringBefore(";").trim()
        bato_pass_start = script.find("const batoPass =")
        if bato_pass_start == -1:
            raise ValueError("batoPass not found")
        bato_pass_start += len("const batoPass =")
        bato_pass_end = script.find(";", bato_pass_start)
        if bato_pass_end == -1:
            raise ValueError("batoPass end not found")
        bato_pass = script[bato_pass_start:bato_pass_end].strip()
        
        return img_https, bato_word, bato_pass
        
    except Exception as e:
        raise RuntimeError(f"Failed to extract script variables: {e}")


def get_decrypted_image_urls(html: str) -> List[str]:
    """
    Main function to extract and decrypt image URLs from BatoTo chapter page.
    Follows the exact logic from Kotlin pageListParse method.
    """
    try:
        # Extract data from script - following Kotlin implementation
        img_https, bato_word, bato_pass = extract_script_data(html)
        
        # Deobfuscate the password - following Kotlin: Deobfuscator.deobfuscateJsPassword(batoPass)
        evaluated_pass = Deobfuscator.deobfuscate_js_password(bato_pass)
        
        # Decrypt the access list - following Kotlin: CryptoAES.decrypt(batoWord, evaluatedPass)
        img_acc_list_str = CryptoAES.decrypt(bato_word, evaluated_pass)
        
        # If decryption failed (empty string), return empty list
        if not img_acc_list_str:
            return []
        
        img_acc_list = json.loads(img_acc_list_str)
        
        # Combine URLs with access parameters - following Kotlin logic
        result_urls = []
        for i, img_url in enumerate(img_https):
            acc = img_acc_list[i] if i < len(img_acc_list) else None
            if acc:
                final_url = f"{img_url}?{acc}"
            else:
                final_url = img_url
            result_urls.append(final_url)
        
        return result_urls
        
    except Exception as e:
        raise RuntimeError(f"Failed to decrypt image URLs: {str(e)}")


# Example usage
if __name__ == "__main__":
    import requests
    
    chapter_url = "https://batotwo.com/chapter/3348910"
    try:
        response = requests.get(chapter_url)
        response.raise_for_status()
        
        image_urls = get_decrypted_image_urls(response.text)
        
        print(f"Found {len(image_urls)} images:")
        for i, url in enumerate(image_urls, 1):
            print(f"{i}: {url}")
            
    except Exception as e:
        print(f"Error: {e}")
