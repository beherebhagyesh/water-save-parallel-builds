from playwright.sync_api import sync_playwright

URL = 'http://localhost:36900'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1360, "height": 900})
    page.goto(URL)
    page.wait_for_load_state('networkidle')

    # Tab 0 full
    page.screenshot(path='prototypes/a2_tab0.png', full_page=True)

    # Tab 2 Field Conditions
    page.locator('.tab-btn').nth(2).click()
    page.wait_for_timeout(800)
    page.screenshot(path='prototypes/a2_tab2.png', full_page=True)

    # Tab 3 Economics - scroll to bottom
    page.locator('.tab-btn').nth(3).click()
    page.wait_for_timeout(500)
    page.screenshot(path='prototypes/a2_tab3_top.png', full_page=False)
    page.evaluate("window.scrollTo(0, 9999)")
    page.wait_for_timeout(300)
    page.screenshot(path='prototypes/a2_tab3_bottom.png', full_page=False)

    # Tab 4 System
    page.locator('.tab-btn').nth(4).click()
    page.wait_for_timeout(500)
    page.screenshot(path='prototypes/a2_tab4.png', full_page=True)

    browser.close()
print("Done")
