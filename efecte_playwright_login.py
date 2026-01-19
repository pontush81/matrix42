#!/usr/bin/env python3
"""
Efecte Community Scraper med Playwright

Hanterar JavaScript-baserad login med reCAPTCHA.

Användning:
    # Första gången (sparar cookies):
    EFECTE_EMAIL=din@email.com EFECTE_PASSWORD=xxx python3 efecte_playwright_login.py --login

    # Efterföljande körningar (använder sparade cookies):
    python3 efecte_playwright_login.py --scrape
"""

import os
import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Konfiguration
COOKIES_FILE = "efecte_cookies.json"
BASE_URL = "https://community.efecte.com"


def save_cookies(context, filepath=COOKIES_FILE):
    """Spara cookies till fil för återanvändning"""
    cookies = context.cookies()
    with open(filepath, 'w') as f:
        json.dump(cookies, f, indent=2)
    print(f"✅ Cookies sparade till {filepath}")


def load_cookies(context, filepath=COOKIES_FILE):
    """Ladda cookies från fil"""
    if not os.path.exists(filepath):
        return False
    try:
        with open(filepath, 'r') as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        print(f"✅ Cookies laddade från {filepath}")
        return True
    except Exception as e:
        print(f"⚠️ Kunde inte ladda cookies: {e}")
        return False


def login_with_playwright(email: str, password: str, headless: bool = False):
    """
    Logga in på Efecte Community med Playwright.

    Args:
        email: Inloggnings-email
        password: Lösenord
        headless: Kör utan synlig webbläsare (False = visa webbläsaren)
    """
    print("=" * 70)
    print("EFECTE COMMUNITY LOGIN MED PLAYWRIGHT")
    print("=" * 70)

    with sync_playwright() as p:
        # Starta webbläsare (headless=False för att se vad som händer)
        print(f"\n1. Startar webbläsare (headless={headless})...")
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()

        try:
            # Navigera till login-sidan
            print("\n2. Navigerar till login-sidan...")
            page.goto(f"{BASE_URL}/login", wait_until='networkidle')
            print(f"   URL: {page.url}")

            # Vänta på att formuläret laddas
            print("\n3. Väntar på login-formulär...")
            page.wait_for_selector('input[name="email"]', timeout=10000)

            # Fyll i email
            print("\n4. Fyller i inloggningsuppgifter...")
            email_input = page.locator('input[name="email"]')
            email_input.fill(email)
            print(f"   Email: {email}")

            # Fyll i lösenord
            password_input = page.locator('input[name="password"]')
            password_input.fill(password)
            print("   Lösenord: ****")

            # Ta screenshot före login
            page.screenshot(path='efecte_before_login.png')
            print("\n5. Screenshot sparad: efecte_before_login.png")

            # Klicka på login-knappen
            print("\n6. Klickar på Login-knappen...")
            login_button = page.locator('button.btn-login')
            login_button.click()

            # Vänta på navigation eller reCAPTCHA
            print("\n7. Väntar på respons...")

            # Kolla om reCAPTCHA dyker upp
            try:
                # Vänta lite för att se om vi redirectas
                page.wait_for_url(lambda url: 'login' not in url.lower(), timeout=5000)
                print("   ✅ Redirectad från login-sidan!")
            except PlaywrightTimeout:
                # Kolla om reCAPTCHA visas
                recaptcha = page.locator('iframe[src*="recaptcha"]')
                if recaptcha.count() > 0:
                    print("\n   ⚠️ reCAPTCHA detekterad!")
                    print("   Vänligen lös reCAPTCHA manuellt i webbläsaren...")
                    print("   (Väntar upp till 120 sekunder)")

                    # Vänta på att användaren löser reCAPTCHA och loggar in
                    try:
                        page.wait_for_url(lambda url: 'login' not in url.lower(), timeout=120000)
                        print("   ✅ reCAPTCHA löst, inloggning lyckades!")
                    except PlaywrightTimeout:
                        print("   ❌ Timeout - kunde inte logga in")
                        page.screenshot(path='efecte_login_failed.png')
                        return False
                else:
                    # Kolla om det finns felmeddelande
                    error = page.locator('.error-message, .alert-error, .login-error')
                    if error.count() > 0:
                        print(f"   ❌ Login-fel: {error.text_content()}")
                        return False
                    else:
                        print("   ⚠️ Okänt tillstånd - väntar lite till...")
                        time.sleep(3)

            # Verifiera inloggning
            print(f"\n8. Nuvarande URL: {page.url}")

            # Ta screenshot efter login
            page.screenshot(path='efecte_after_login.png')
            print("   Screenshot sparad: efecte_after_login.png")

            # Kolla om vi är inloggade
            if 'login' not in page.url.lower():
                print("\n✅ INLOGGNING LYCKADES!")

                # Spara cookies
                save_cookies(context)

                # Testa att hämta en skyddad sida
                print("\n9. Testar åtkomst till forum...")
                page.goto(BASE_URL)
                page.wait_for_load_state('networkidle')

                # Spara HTML för inspektion
                with open('efecte_logged_in_content.html', 'w', encoding='utf-8') as f:
                    f.write(page.content())
                print("   HTML sparad: efecte_logged_in_content.html")

                return True
            else:
                print("\n❌ INLOGGNING MISSLYCKADES")
                page.screenshot(path='efecte_login_failed.png')
                return False

        except Exception as e:
            print(f"\n❌ Fel: {e}")
            page.screenshot(path='efecte_error.png')
            return False

        finally:
            browser.close()
            print("\n" + "=" * 70)


def scrape_with_cookies():
    """Scrapa Efecte Community med sparade cookies"""
    print("=" * 70)
    print("SCRAPING MED SPARADE COOKIES")
    print("=" * 70)

    if not os.path.exists(COOKIES_FILE):
        print(f"❌ Cookies-fil saknas: {COOKIES_FILE}")
        print("   Kör först: python3 efecte_playwright_login.py --login")
        return False

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )

        # Ladda sparade cookies
        load_cookies(context)

        page = context.new_page()

        try:
            # Gå till huvudsidan
            print("\n1. Navigerar till Efecte Community...")
            page.goto(BASE_URL, wait_until='networkidle')

            # Kolla om vi är inloggade
            if 'login' in page.url.lower():
                print("❌ Cookies har gått ut - behöver logga in igen")
                return False

            print(f"   URL: {page.url}")
            print("   ✅ Session aktiv!")

            # Hitta forum-kategorier
            print("\n2. Letar efter forum-innehåll...")

            # Spara hela sidans HTML
            html = page.content()
            with open('efecte_forum_content.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("   HTML sparad: efecte_forum_content.html")

            # Hitta länkar/kategorier
            links = page.locator('a[href*="/t/"], a[href*="/c/"], a[href*="/d/"]').all()
            print(f"\n3. Hittade {len(links)} forum-länkar")

            for i, link in enumerate(links[:10]):  # Visa första 10
                href = link.get_attribute('href')
                text = link.text_content().strip()[:50]
                print(f"   {i+1}. {text} -> {href}")

            return True

        except Exception as e:
            print(f"❌ Fel: {e}")
            return False

        finally:
            browser.close()


def main():
    if '--login' in sys.argv:
        email = os.environ.get('EFECTE_EMAIL')
        password = os.environ.get('EFECTE_PASSWORD')

        if not email or not password:
            print("❌ Miljövariabler saknas!")
            print("   EFECTE_EMAIL=din@email.com EFECTE_PASSWORD=xxx python3 efecte_playwright_login.py --login")
            sys.exit(1)

        # Kör med synlig webbläsare för att kunna lösa eventuell reCAPTCHA
        success = login_with_playwright(email, password, headless=False)
        sys.exit(0 if success else 1)

    elif '--scrape' in sys.argv:
        success = scrape_with_cookies()
        sys.exit(0 if success else 1)

    else:
        print("Användning:")
        print("  --login   Logga in och spara cookies (kräver EFECTE_EMAIL och EFECTE_PASSWORD)")
        print("  --scrape  Scrapa med sparade cookies")
        sys.exit(1)


if __name__ == '__main__':
    main()
