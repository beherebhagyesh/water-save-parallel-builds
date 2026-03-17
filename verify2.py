from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1360, "height": 900})
    page.goto('http://localhost:36900')
    page.wait_for_load_state('networkidle')

    page.screenshot(path='prototypes/v2_tab0.png', full_page=False)

    page.locator('.tab-btn').nth(2).click()
    page.wait_for_timeout(500)
    page.screenshot(path='prototypes/v2_tab2.png', full_page=False)

    browser.close()
print("Done")
