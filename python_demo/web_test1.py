import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.amazon.co.uk/ref=nav_logo")
    page.get_by_role("button", name="Accept").click()
    page.get_by_role("button", name="Submit").nth(1).click()
    # page.get_by_role("textbox", name="or enter a UK mainland").click()

    page.get_by_role("textbox", name="or enter a UK mainland").fill("BH21 2EY")
    page.get_by_label("Apply").click()
    page.get_by_role("button", name="Continue").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
