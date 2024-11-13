from playwright.sync_api import sync_playwright
from termcolor import colored

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.langchain.com")
    print(f"Page Title is: {colored(page.title(), 'cyan') }")
    
    ud_header = page.locator('.ud-heading-serif-xxl').all_text_contents()
    for subheader in ud_header:
        print(f"Udemy Subheader: {colored(subheader, 'cyan')}")
    
    browser.close()

with sync_playwright() as playwright:
    run(playwright)