from playwright.sync_api import sync_playwright, TimeoutError
import time
import random
from fake_useragent import UserAgent
import os

class VUTPageDownloader:
    """
    VUT Login Bot Class
    """
    
    UA = UserAgent(platforms="desktop")
    USER_AGENT = UA.random
    LOGIN_URL = "https://www.vut.cz/studis/student.phtml?sn=el_index"

    def __init__(self, username=None, password=None, main_directory="data"):
        self.playwright = None
        self.username= username
        self.password = password
        self.main_directory = main_directory
        self.browser = None
        self.context = None
        self.page = None

    def random_delay(self, min_ms=56, max_ms=532):
        """Simulate human typing or thinking delay in milliseconds"""
        delay_seconds = random.uniform(min_ms / 1000, max_ms / 1000)
        time.sleep(delay_seconds)

    def launch_browser(self):
        """Launch browser with realistic settings"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        self.context = self.browser.new_context(user_agent=self.USER_AGENT)
        self.page = self.context.new_page()

    def go_to_page(self, url):
        """Navigate to a specific page"""
        print(f"Going to {url}...")
        self.page.goto(url)
        self.random_delay() 

    def go_to_login_page(self):
        """Navigate to login page"""
        self.go_to_page(self.LOGIN_URL)

    def fill_username(self):
        """Fill username field and submit"""
        print("Filling username...")
        self.page.fill("#frm-signInFormLogin-login", f"{self.username}")
        self.random_delay()
        self.page.click("button[type=submit]")
        self.random_delay(2, 4)

    def fill_password(self):
        """Wait for password field and fill it"""
        print("Waiting for password field...")
        try:
            self.page.wait_for_selector("#frm-signInFormPassword-passwd", timeout=10000)
        except TimeoutError:
            print("Timeout waiting for password field.")
            self.take_screenshot("password_timeout.png")
            raise

        print("Filling password...")
        self.page.fill("#frm-signInFormPassword-passwd", f"{self.password}")
        self.random_delay()
        self.page.click("button[type=submit]")
        self.random_delay(3, 5)

    def wait_for_navigation(self, expected_url_pattern="**/student.phtml*", timeout=15000):
        """Wait for navigation to a matching URL"""
        try:
            self.page.wait_for_url(expected_url_pattern, timeout=timeout)
            print(f"✅ Arrived at: {self.page.url}")
        except TimeoutError:
            print("❌ Timeout waiting for navigation.")
            self.take_screenshot("navigation_timeout.png")
            raise
    def save_current_page(self, filename="page.html"):
        """Save current page HTML to file relative to this script"""

        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Combine with desired save path
        full_path = os.path.join(base_dir, self.main_directory, filename)
        print(f"Saving page to {full_path}...")

        folder = os.path.dirname(full_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        # Save the file
        html = self.page.content()
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"📄 Saved: {full_path}")

    def take_screenshot(self, path="error_screenshot.png"):
        """Take a screenshot on error for debugging"""
        self.page.screenshot(path=path)
        print(f"📸 Screenshot saved at: {path}")

    def close(self):
        """Close browser and Playwright session"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    def check_credentials(self) -> bool:
        return self.username and self.password
    def authenticate(self):
        """Perform login flow"""
        self.launch_browser()
        self.go_to_login_page()
        self.fill_username()
        self.fill_password()
        self.wait_for_navigation()
        print("✅ Successfully logged in.")

    def download_page(self, url, filename):
        """Download any authenticated page and save it"""
        try:
            self.go_to_page(url)
            self.wait_for_navigation()
            self.save_current_page(filename)
        except Exception as e:
            print(f"❌ Failed to download {url}: {e}")

    def run(self, url, filename ="page.html"):
        """Main execution flow"""
        if not self.check_credentials():
            print("❌ Please provide VUT_ID and VUT_PASS")
            return
        self.authenticate()
        self.download_page(url, filename)
        self.close()

