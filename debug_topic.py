#!/usr/bin/env python3
"""Debug-skript för att undersöka topic-struktur"""
import json
from playwright.sync_api import sync_playwright

COOKIES_FILE = "efecte_cookies.json"
BASE_URL = "https://community.efecte.com"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()

    # Ladda cookies
    with open(COOKIES_FILE, 'r') as f:
        cookies = json.load(f)
    context.add_cookies(cookies)

    page = context.new_page()

    # Hämta en topic
    page.goto(f"{BASE_URL}/t/q5djfx/forum-rules", wait_until='networkidle')

    # Spara HTML
    with open('debug_topic.html', 'w', encoding='utf-8') as f:
        f.write(page.content())

    print("HTML sparad till debug_topic.html")

    # Testa olika selektorer för titel
    selectors = [
        'h1',
        '.topic-title',
        '.thread-title',
        '.post-title',
        '.discussion-title',
        'h1.title',
        '[class*="title"]',
        '.topic-header h1',
        '.topic-subject',
        '.subject'
    ]

    print("\nTestar titel-selektorer:")
    for sel in selectors:
        elem = page.locator(sel).first
        if elem.count() > 0:
            text = elem.text_content().strip()[:80]
            print(f"  {sel}: '{text}'")

    # Visa alla h1-h3 element
    print("\nAlla h1-h3 element:")
    for tag in ['h1', 'h2', 'h3']:
        elems = page.locator(tag).all()
        for i, elem in enumerate(elems[:3]):
            text = elem.text_content().strip()[:60]
            print(f"  {tag}[{i}]: '{text}'")

    browser.close()
