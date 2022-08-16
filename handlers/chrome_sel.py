from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
import selenium
import pandas as pd

import time
import string
import datetime

# a lot of this taken from devops https://github.com/StrongMind/zendesk_ps_export_student_data
# tweaked as some items are deprecated

"""Each school has their own sub account that must be switched to. Simply find the Input button for that school and
Steal its ID, add it below and we can then reference it further in the code.
"""

def click_element(driver,element_id):
    section_to_click = driver.find_element(By.ID, element_id)
    section_to_click.click()

def wait_for_element_load(driver, element,delay = 10):
    try:
        new_element_loading = WebDriverWait(driver, timeout=delay).until(lambda d: d.find_element(By.ID, element))
    except TimeoutException:
        print(f"Error element {element} not found in requested div after {delay} seconds.")
        return False
    else:
        return new_element_loading

def set_account(browser, id):
    switch_accounts = wait_for_element_load(browser, 'switch-customer-button')
    #This is taking longer than we thought to load
    time.sleep(3)
    switch_accounts.click()
    account_input_element = wait_for_element_load_Xpath(browser, f"//input[@id = '{id}']/../div")
    account_input_element.click()
    submit_switch_accounts = browser.find_element(By.ID, "switch-customers-dialog-done")
    submit_switch_accounts.click()
    time.sleep(3)

def wait_for_element_load_Xpath(driver, path,delay = 10):
    try:
        new_element_loading = WebDriverWait(driver, timeout=delay).until(lambda d: d.find_element(By.XPATH, path))
    except TimeoutException:
        print(f"Error element {path} not found in requested div after {delay} seconds.")
        return False
    else:
        return new_element_loading