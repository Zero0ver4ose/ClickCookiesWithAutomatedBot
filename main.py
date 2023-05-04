from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_driver_path = "C:\Development\chromedriver_win32\chromedriver"
driver = webdriver.Chrome(service=Service(chrome_driver_path))
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")
cookie.click()

#Get upgrade time ids.
items = driver.find_elements(By.CSS_SELECTOR, "div[id='store']")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 60
five_min= time.time() + 20*60

while True:
    cookie.click()

    #every 5 second:
    if time.time() > timeout:

        #Get all upgrade <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, "div[id='store'] b")
        item_prices = []

        #Convent <b> text into an integer price.
        for price in all_prices:
            element_text = price.get_attribute("innerHTML")
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        #Create dictionary of store items and prices
        cookie_upgrade = {}
        for n in range(len(item_prices)):
            cookie_upgrade[item_prices[n]] = item_ids[n]

        #Get current cookie count
        money_element =  driver.find_element(By.ID, "money").get_attribute("innerHTML")
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        #Find Upgrades that we can currently afford
        affordable_upgrade = {}
        for cost, id in cookie_upgrade.items():
            if cookie_count > cost:
                affordable_upgrade[cost] = id

        #Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrade)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrade[highest_price_affordable_upgrade]

        driver.find_element(By.ID, to_purchase_id.click())

        #ADD another 5 second until the next check
        timeout = time.time() + 5

    #after 5 minutes stop the bot and check the cookie per second count.
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").get_attribute("innerHTML")
        print(cookie_per_s)
        break





input("click ENTER to exits\n")



