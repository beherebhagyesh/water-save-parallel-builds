from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1360, "height": 900})
    page.goto('http://localhost:36900')
    page.wait_for_load_state('networkidle')

    # Tab 0 - hero + Draw & Run
    page.screenshot(path='prototypes/verify_tab0.png', full_page=False)

    # Tab 1 - Results empty state
    page.locator('.tab-btn').nth(1).click()
    page.wait_for_timeout(500)
    page.screenshot(path='prototypes/verify_tab1_empty.png', full_page=False)

    # Tab 3 - Economics (mandi prices)
    page.locator('.tab-btn').nth(3).click()
    page.wait_for_timeout(500)
    page.screenshot(path='prototypes/verify_tab3.png', full_page=True)

    # Tab 4 - System (climate panel gone)
    page.locator('.tab-btn').nth(4).click()
    page.wait_for_timeout(500)
    page.screenshot(path='prototypes/verify_tab4.png', full_page=False)

    browser.close()
print("Done")
