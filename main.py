import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(options=options)

driver.get("https://www.wildberries.ru/")

time.sleep(2)
# input = driver.find_element(By.XPATH, "//input[@id='searchInput']")
input = driver.find_element(By.ID, "searchInput")
input.send_keys("телевизор dexp")
input.send_keys(Keys.ENTER)
time.sleep(2)

tv_info = list()

while True:
    while True:
        wait = WebDriverWait(driver, 30)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@id]")))

        # cards = driver.find_elements(By.XPATH, "//article[@id]")
        print(len(cards))
        count = len(cards)
        driver.execute_script("window.scrollBy(0,3000)")
        time.sleep(2)
        cards = driver.find_elements(By.XPATH, "//article[@id]")
        if len(cards) == count:
            break

        tv_page = dict()
        for card in cards:
            price = card.find_element(By.CLASS_NAME, "price__lower-price").text
            name = card.find_element(By.XPATH, "./div/a").get_attribute('aria-label')
            url = card.find_element(By.XPATH, "./div/a").get_attribute('href')
            print(price, name, url)

            tv_page['price'] = price
            tv_page['name'] = name
            tv_page['url'] = url

            tv_info.append(tv_page)
            df = pd.DataFrame(tv_info)
            df.to_csv("tv_info.csv", index=False)


        try:
            button = driver.find_element(By.CLASS_NAME, "pagination-next")
            actions = ActionChains(driver)
            actions.move_to_element(button).click()
            actions.perform()
        except:
            break


