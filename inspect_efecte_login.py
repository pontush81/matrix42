#!/usr/bin/env python3
"""
Inspekterar Efecte Community login-sidan för att hitta:
- Formulärfält och deras namn
- CSRF-tokens
- Form action URL
- Cookies som sätts
"""

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'sv-SE,sv;q=0.9,en;q=0.8',
}

def inspect_login_page():
    session = requests.Session()

    print("=" * 70)
    print("INSPEKTERAR EFECTE COMMUNITY LOGIN")
    print("=" * 70)

    # Hämta login-sidan
    print("\n1. Hämtar login-sidan...")
    response = session.get('https://community.efecte.com/login', headers=HEADERS, timeout=30)
    print(f"   Status: {response.status_code}")
    print(f"   URL efter redirect: {response.url}")

    # Visa cookies
    print("\n2. Cookies som sattes:")
    for cookie in session.cookies:
        print(f"   - {cookie.name}: {cookie.value[:50]}..." if len(cookie.value) > 50 else f"   - {cookie.name}: {cookie.value}")

    # Parsa HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Hitta alla formulär
    print("\n3. Formulär på sidan:")
    forms = soup.find_all('form')

    if not forms:
        print("   Inga <form>-taggar hittades!")
        print("\n   Letar efter andra input-fält...")

    for i, form in enumerate(forms, 1):
        print(f"\n   === FORM #{i} ===")
        print(f"   Action: {form.get('action', 'INGEN')}")
        print(f"   Method: {form.get('method', 'INGEN')}")
        print(f"   ID: {form.get('id', 'INGEN')}")
        print(f"   Class: {form.get('class', 'INGEN')}")

        # Hitta alla input-fält i detta formulär
        inputs = form.find_all('input')
        print(f"\n   Input-fält ({len(inputs)} st):")
        for inp in inputs:
            inp_type = inp.get('type', 'text')
            inp_name = inp.get('name', 'INGET NAMN')
            inp_id = inp.get('id', '')
            inp_value = inp.get('value', '')
            print(f"      - name='{inp_name}' type='{inp_type}' id='{inp_id}' value='{inp_value[:30]}'" if inp_value else f"      - name='{inp_name}' type='{inp_type}' id='{inp_id}'")

    # Sök efter alla input-fält oavsett form
    print("\n4. Alla input-fält på sidan:")
    all_inputs = soup.find_all('input')
    for inp in all_inputs:
        inp_type = inp.get('type', 'text')
        inp_name = inp.get('name', 'INGET NAMN')
        inp_id = inp.get('id', '')
        inp_placeholder = inp.get('placeholder', '')
        print(f"   - name='{inp_name}' type='{inp_type}' id='{inp_id}' placeholder='{inp_placeholder}'")

    # Sök efter CSRF-tokens
    print("\n5. Potentiella CSRF-tokens:")
    csrf_patterns = ['csrf', 'token', '_token', 'authenticity', 'xsrf']
    for inp in all_inputs:
        inp_name = inp.get('name', '').lower()
        if any(pattern in inp_name for pattern in csrf_patterns):
            print(f"   HITTAT: name='{inp.get('name')}' value='{inp.get('value', '')[:50]}'")

    # Sök efter meta-csrf
    meta_csrf = soup.find_all('meta', attrs={'name': lambda x: x and 'csrf' in x.lower()})
    for meta in meta_csrf:
        print(f"   META: {meta.get('name')}: {meta.get('content', '')[:50]}")

    # Sök efter JavaScript som hanterar login
    print("\n6. JavaScript-relaterad info:")
    scripts = soup.find_all('script')
    for script in scripts:
        script_text = script.string or ''
        if any(kw in script_text.lower() for kw in ['login', 'auth', 'session', 'submit']):
            print(f"   Hittade login-relaterat script: {len(script_text)} tecken")
            # Skriv ut första 500 tecken
            if script_text:
                print(f"   Preview: {script_text[:500]}...")

    # Kolla response headers
    print("\n7. Response headers:")
    for key, value in response.headers.items():
        if any(kw in key.lower() for kw in ['cookie', 'auth', 'token', 'csrf', 'session']):
            print(f"   {key}: {value}")

    # Spara HTML för manuell inspektion
    with open('efecte_login_page.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("\n8. Fullständig HTML sparad i: efecte_login_page.html")

    print("\n" + "=" * 70)

if __name__ == '__main__':
    inspect_login_page()
