from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up ChromeDriver
service = Service("/home/julia/Downloads/chromedriver-linux64/chromedriver")  # Update path if needed
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

def capture_screenshot(step_name):
    driver.save_screenshot(f"screenshot_{step_name}.png")

def test_navigation_links():
    try:
        # Open Facebook homepage
        driver.get("https://www.facebook.com")
        driver.maximize_window()
        time.sleep(3)  # Allow time for page to load
        capture_screenshot("homepage_loaded")
        
        # Verify Home button
        home_button = driver.find_element(By.XPATH, "//a[@aria-label='Home']")
        home_button.click()
        time.sleep(2)
        capture_screenshot("home_button_clicked")
        assert "facebook.com" in driver.current_url, "Home button failed"
        
        # Verify Profile button
        profile_button = driver.find_element(By.XPATH, "//a[contains(@href, 'profile')]" )
        profile_button.click()
        time.sleep(2)
        capture_screenshot("profile_button_clicked")
        assert "facebook.com/profile" in driver.current_url, "Profile button failed"
        
        # Verify Friends button
        friends_button = driver.find_element(By.XPATH, "//a[@aria-label='Friends']")
        friends_button.click()
        time.sleep(2)
        capture_screenshot("friends_button_clicked")
        assert "facebook.com/friends" in driver.current_url, "Friends button failed"
        
        # Verify Notifications button
        notifications_button = driver.find_element(By.XPATH, "//div[@aria-label='Notifications']")
        notifications_button.click()
        time.sleep(2)
        capture_screenshot("notifications_button_clicked")
        assert "notifications" in driver.page_source, "Notifications button failed"
        
        # Scroll to bottom to check footer links
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        capture_screenshot("scrolled_to_bottom")
        footer_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Privacy') or contains(text(), 'Terms')]" )
        assert len(footer_links) > 0, "Footer links not found"
        
        # Validate Login Form Submission
        driver.get("https://www.facebook.com")
        time.sleep(2)
        capture_screenshot("login_page_loaded")
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "pass")
        login_button = driver.find_element(By.NAME, "login")
        
        email_input.send_keys("testuser@example.com")
        password_input.send_keys("incorrectpassword")
        capture_screenshot("credentials_entered")
        login_button.click()
        time.sleep(3)
        capture_screenshot("login_attempt")
        
        assert "incorrect" in driver.page_source.lower(), "Login validation failed"
        
        print("✅ All navigation and form validation tests passed!")
    
    except Exception as e:
        capture_screenshot("error_occurred")
        print(f"❌ Test failed: {str(e)}")
    
    finally:
        driver.quit()

# Run the test
test_navigation_links()
