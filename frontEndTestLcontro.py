
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Set up ChromeDriver
service = Service("/home/julia/Downloads/chromedriver-linux64/chromedriver")  # Update path if necessary
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open Facebook homepage
    driver.get("https://www.facebook.com")

    # Verify the title
    assert "Facebook" in driver.title, "Facebook homepage did not load successfully"

    # (Optional) Verify login form exists
    login_box = driver.find_element(By.NAME, "email")  # Finds the email input box
    assert login_box is not None, "Login input box not found!"

    print("✅ Facebook homepage loaded successfully!")
    
finally:
    driver.quit()  # Close the browser

