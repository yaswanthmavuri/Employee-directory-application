from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_add_employee():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    driver.get("http://20.219.133.124:5000")

    driver.find_element(By.NAME, "name").send_keys("Raju")
    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(2)

    assert "Raju" in driver.page_source

    driver.quit()
