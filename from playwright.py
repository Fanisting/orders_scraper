from playwright.sync_api import sync_playwright

    
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    # Read the contents of the local JavaScript file
    custom_js = 'console.log("Custom JavaScript code has been injected!");'
    # Inject the JavaScript code into the page using add_script_tag()
    page.add_script_tag(content=custom_js)
    try:
        # Navigate to the webpage where you want to inject the script
        page.goto("https://github.com")
        # Other interactions or actions on the page can be performed here

    except Exception as e:
        print("Error occurred during script execution:", e)

    finally:
        # Close the browser
        print("Error occurred)")