import re
import base64
import json
import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from hashlib import md5
from typing import List


def extract_script_constants(html: str):
    soup = BeautifulSoup(html, "html.parser")
    script = next(
        (s.text for s in soup.find_all("script")
         if "imgHttps" in s.text and "batoWord" in s.text and "batoPass" in s.text),
        None
    )
    if not script:
        raise RuntimeError("Couldn't find script with required constants.")

    def extract_var(name):
        match = re.search(rf'const {name}\s*=\s*(.*?);', script)
        if not match:
            raise ValueError(f"{name} not found in script")
        return match.group(1).strip().strip('"')

    img_https = json.loads(extract_var("imgHttps"))
    bato_word = extract_var("batoWord")
    bato_pass = extract_var("batoPass")
    return img_https, bato_word, bato_pass


def deobfuscate_jsfuck(pass_str: str) -> str:
    result = []
    i = 0
    while i < len(pass_str):
        if pass_str[i] not in ['[', '(']:
            i += 1
            continue

        opening = pass_str[i]
        closing = ']' if opening == '[' else ')'
        count = 1
        j = i + 1
        while j < len(pass_str):
            if pass_str[j] == opening:
                count += 1
            elif pass_str[j] == closing:
                count -= 1
                if count == 0:
                    break
            j += 1
        chunk = pass_str[i:j + 1]

        if opening == '(':
            result.append('.')
        else:
            digit = chunk.count('!+[]')
            if digit > 0:
                result.append(str(digit))
            elif '+[]' in chunk:
                result.append('0')
            else:
                result.append('-')  # fallback
        i = j + 1
    return ''.join(result)


def evp_bytes_to_key(password: bytes, salt: bytes, key_len=32, iv_len=16) -> (bytes, bytes):
    d = b''
    while len(d) < key_len + iv_len:
        d_i = md5(d[-16:] + password + salt).digest() if d else md5(password + salt).digest()
        d += d_i
    return d[:key_len], d[key_len:key_len + iv_len]


def decrypt_bato_word(ciphertext: str, password: str) -> List[str]:
    raw = base64.b64decode(ciphertext)
    assert raw[:8] == b"Salted__"
    salt = raw[8:16]
    cipher_data = raw[16:]
    key, iv = evp_bytes_to_key(password.encode('utf-8'), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(cipher_data)

    # Remove PKCS#7 padding safely
    pad_len = plaintext[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError(f"Invalid padding length: {pad_len}")
    plaintext = plaintext[:-pad_len]

    decoded = plaintext.decode('utf-8')

    if not decoded.strip():
        raise ValueError("Decrypted string is empty.")

    return json.loads(decoded)

def get_bato_image_urls(chapter_url: str) -> List[str]:
    html = requests.get(chapter_url).text
    img_https, bato_word, bato_pass = extract_script_constants(html)
    password = deobfuscate_jsfuck(bato_pass)
    img_accs = decrypt_bato_word(bato_word, password)

    return [f"{img}?{acc}" if acc else img for img, acc in zip(img_https, img_accs)]


# 🔍 Exemple d'utilisation :
if __name__ == "__main__":
    chapter_url = "https://batotwo.com/chapter/3348910"  # <-- mets ici l’URL du chapitre
    for url in get_bato_image_urls(chapter_url):
        print(url)
