#!/usr/bin/env python3
"""
Testar inloggning till Efecte Community.

OBS: Kräver miljövariabler:
  EFECTE_EMAIL - din email
  EFECTE_PASSWORD - ditt lösenord

Kör: EFECTE_EMAIL=din@email.com EFECTE_PASSWORD=dittlösenord python3 test_efecte_login.py
"""

import os
import sys
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'sv-SE,sv;q=0.9,en;q=0.8',
}

def test_login():
    email = os.environ.get('EFECTE_EMAIL')
    password = os.environ.get('EFECTE_PASSWORD')

    if not email or not password:
        print("❌ Miljövariabler saknas!")
        print("   Kör: EFECTE_EMAIL=din@email.com EFECTE_PASSWORD=xxx python3 test_efecte_login.py")
        sys.exit(1)

    session = requests.Session()

    print("=" * 70)
    print("TESTAR EFECTE COMMUNITY LOGIN")
    print("=" * 70)

    # Steg 1: Hämta login-sidan för att få cookies och verifyKey
    print("\n1. Hämtar login-sidan...")
    response = session.get('https://community.efecte.com/login', headers=HEADERS, timeout=30)
    print(f"   Status: {response.status_code}")

    # Parsa för att hitta verifyKey
    soup = BeautifulSoup(response.content, 'html.parser')
    verify_key_input = soup.find('input', {'name': 'verifyKey'})
    verify_key = verify_key_input.get('value', '') if verify_key_input else ''
    print(f"   verifyKey: '{verify_key}' (tom är OK)")

    # Visa cookies
    print(f"   Cookies: {[c.name for c in session.cookies]}")

    # Steg 2: Skicka login POST
    print("\n2. Skickar login POST till /login/go...")
    login_data = {
        'email': email,
        'password': password,
        'verifyKey': verify_key
    }

    # Lägg till Referer header
    headers = HEADERS.copy()
    headers['Referer'] = 'https://community.efecte.com/login'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Origin'] = 'https://community.efecte.com'

    response = session.post(
        'https://community.efecte.com/login/go',
        data=login_data,
        headers=headers,
        timeout=30,
        allow_redirects=True
    )

    print(f"   Status: {response.status_code}")
    print(f"   Slutlig URL: {response.url}")
    print(f"   Cookies efter login: {[c.name for c in session.cookies]}")

    # Steg 3: Verifiera att vi är inloggade
    print("\n3. Verifierar inloggning...")

    # Kolla om vi redirectades till huvudsidan
    if response.url == 'https://community.efecte.com/' or 'login' not in response.url.lower():
        print("   ✅ Troligtvis inloggad (redirectad från login)")
    else:
        print("   ⚠️  Fortfarande på login-sidan - kan indikera fel")

    # Testa att hämta en skyddad sida
    print("\n4. Testar åtkomst till profil/skyddad sida...")
    test_response = session.get('https://community.efecte.com/profile', headers=HEADERS, timeout=30)
    print(f"   Status: {test_response.status_code}")
    print(f"   URL: {test_response.url}")

    # Kolla om vi får se innehåll
    soup = BeautifulSoup(test_response.content, 'html.parser')

    # Leta efter tecken på inloggning
    logout_link = soup.find('a', href=lambda x: x and 'logout' in x.lower())
    if logout_link:
        print("   ✅ Hittade logout-länk - vi är inloggade!")

    # Leta efter användarnamn eller profil
    username_elem = soup.find(class_=lambda x: x and 'username' in str(x).lower())
    if username_elem:
        print(f"   ✅ Hittade användarnamn: {username_elem.get_text(strip=True)}")

    # Testa att hämta forum-innehåll
    print("\n5. Testar att hämta forum-innehåll...")
    forum_response = session.get('https://community.efecte.com/', headers=HEADERS, timeout=30)
    soup = BeautifulSoup(forum_response.content, 'html.parser')

    # Hitta forum-kategorier eller inlägg
    topics = soup.find_all(class_=lambda x: x and ('topic' in str(x).lower() or 'post' in str(x).lower() or 'thread' in str(x).lower()))
    categories = soup.find_all(class_=lambda x: x and 'category' in str(x).lower())

    print(f"   Hittade {len(topics)} topic-element")
    print(f"   Hittade {len(categories)} kategori-element")

    # Spara HTML för inspektion
    with open('efecte_after_login.html', 'w', encoding='utf-8') as f:
        f.write(forum_response.text)
    print("\n6. Sparade innehåll till: efecte_after_login.html")

    print("\n" + "=" * 70)
    print("TEST KLART")
    print("=" * 70)

    return session

if __name__ == '__main__':
    test_login()
