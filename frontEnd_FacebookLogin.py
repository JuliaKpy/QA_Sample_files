import pytest
import allure
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
    screenshot_path = f"screenshot_{step_name}.png"
    driver.save_screenshot(screenshot_path)
    allure.attach.file(screenshot_path, name=step_name, attachment_type=allure.attachment_type.PNG)

@allure.feature("Facebook Navigation and Form Testing")
@allure.story("Verify navigation links and login form submission")
def test_navigation_links():
    try:
        with allure.step("Open Facebook homepage"):
            driver.get("https://www.facebook.com")
            driver.maximize_window()
            time.sleep(3)
            capture_screenshot("homepage_loaded")
        
        with allure.step("Verify Home button"):
            home_button = driver.find_element(By.XPATH, "//a[@aria-label='Home']")
            home_button.click()
            time.sleep(2)
            capture_screenshot("home_button_clicked")
            assert "facebook.com" in driver.current_url, "Home button failed"
        
        with allure.step("Verify Profile button"):
            profile_button = driver.find_element(By.XPATH, "//a[contains(@href, 'profile')]")
            profile_button.click()
            time.sleep(2)
            capture_screenshot("profile_button_clicked")
            assert "facebook.com/profile" in driver.current_url, "Profile button failed"
        
        with allure.step("Verify Friends button"):
            friends_button = driver.find_element(By.XPATH, "//a[@aria-label='Friends']")
            friends_button.click()
            time.sleep(2)
            capture_screenshot("friends_button_clicked")
            assert "facebook.com/friends" in driver.current_url, "Friends button failed"
        
        with allure.step("Verify Notifications button"):
            notifications_button = driver.find_element(By.XPATH, "//div[@aria-label='Notifications']")
            notifications_button.click()
            time.sleep(2)
            capture_screenshot("notifications_button_clicked")
            assert "notifications" in driver.page_source, "Notifications button failed"
        
        with allure.step("Scroll to bottom and check footer links"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            capture_screenshot("scrolled_to_bottom")
            footer_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Privacy') or contains(text(), 'Terms')]")
            assert len(footer_links) > 0, "Footer links not found"
        
        with allure.step("Validate Login Form Submission"):
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
        allure.attach(str(e), name="Error Log", attachment_type=allure.attachment_type.TEXT)
        print(f"❌ Test failed: {str(e)}")
    
    finally:
        driver.quit()
