from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1360, "height": 900})
    page.goto('http://localhost:36900')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='prototypes/check_render.png')
    browser.close()
print("Done")
