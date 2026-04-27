from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 1. Setup
driver = webdriver.Chrome()

try:
    # 2. opening the window (Navigate)
    driver.get("https://www.google.com")
    
    # time that indicate downloading of the window
    time.sleep(2)

    # 3. find the search field (Locate)
    # in Google search field has attribute name="q"
    search_box = driver.find_element(By.NAME, "q")

    # 4. fill the text and hit the Enter (Action)
    search_box.send_keys("Selenium Python")
    search_box.submit()

    # 5. results (Validate)
    time.sleep(2)
    assert "Selenium" in driver.title
    print("Success")

finally:
    # 6. close the browser (Close)
    # Використовуємо quit(), щоб закрити всі вікна та завершити процес драйвера
    driver.quit()