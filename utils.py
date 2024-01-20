from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import os
from constants import (
    PAC_URL,
    PAC_STORE_USER_MAIL,
    PAC_STORE_USER_PASSWORD,
)

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, os, logging, time
from faker import Faker
import pandas as pd
from selenium.webdriver.common.keys import Keys
import logging



@contextmanager
def services_context_wrapper(screenshot=None):
    global driver
    try:
        testcase_id = screenshot.split(".")
        logging.info(f"Start for {testcase_id[0]}")
        c = Options()
        # c.add_argument("--headless=new")
        c.add_argument("--window-size=1920,1080")
        # c.add_argument("--no-sandbox")
        # # c.add_argument("enable-automation")
        # c.add_argument("--disable-blink-features=AutomationControlled")
        # c.add_argument("--disable-dev-shm-usage")
        # prefs={"download.default_directory":os.getcwd()+"/downloads"}
        # c.add_experimental_option("prefs",prefs)
        driver = webdriver.Chrome(options=c)
        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=c)
        # driver = webdriver.Remote(command_executor='http://selenium__standalone-chrome:4444/wd/hub',options=c)
        # driver = webdriver.Chrome()
        yield driver
    except Exception:
        logging.info(f"End for {testcase_id[0]}")
        if screenshot:
            driver.save_screenshot(screenshot)
        raise
    finally:
        logging.info(f"End for {testcase_id[0]}")
        logging.info(os.getcwd())
        driver.quit()





class Pac_Credentials:
    def Login_store(driver):
        # driver = webdriver.Chrome()
        retries = 0
        while retries < 7:
            try:
                driver.maximize_window()
                driver.implicitly_wait(10)
                driver.get(PAC_URL)
                driver.find_element(By.XPATH, "//input[@name='username']").send_keys(
                    PAC_STORE_USER_MAIL
                )
                driver.find_element(By.XPATH, "//input[@name='password']").send_keys(
                    PAC_STORE_USER_PASSWORD
                )
                driver.find_element(By.XPATH, "//button[@type='submit']").click()
                return True
            except Exception:
                driver.refresh()
                logging.info(f"Element not found. Retrying... ({retries + 1}/{7})")
                retries += 1

        raise Exception(f"Login Elements not found after {7} retries")



def click_on_add_object(driver, elm_name):
    retries = 0
    while retries < 7:
        try:
            WebDriverWait(driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, '(//span[text()="Product Data"])[1]'))
            )
            # Move to home icon
            home = driver.find_element(By.XPATH, '(//span[text()="Product Data"])[1]')
            actions = ActionChains(driver)
            actions.context_click(home).perform()
            ADD_OBJECT = driver.find_element(By.XPATH, '(//span[text()="Add Object"])[1]')
            action = ActionChains(driver)
            action.move_to_element(ADD_OBJECT).perform()
            logging.info("Clicked on Add Object")
            ADD_OBJECT = driver.find_element(By.XPATH, '(//span[text()="Product Data"])[2]')
            action = ActionChains(driver)
            action.move_to_element(ADD_OBJECT).perform()
            logging.info("Clicked on Add Object")
            time.sleep(2)
            WebDriverWait(driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, '(//span[text()="' + elm_name + '"])'))
            )
            # Click on Stores
            elm = driver.find_element(By.XPATH, '(//span[text()="' + elm_name + '"])')
            mouse_hover = ActionChains(driver)
            mouse_hover.move_to_element(elm).perform()
            time.sleep(1)
            driver.execute_script("arguments[0].click();", elm)
            logging.info(f"Clicked on {elm_name}")
            return True
        except Exception:
            driver.refresh()
            WebDriverWait(driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, '//div[text()="Data Objects"]/../../../../..//span[text()="Home"]'))
            )
            time.sleep(5)
            logging.info(f"Element not found. Retrying... ({retries + 1}/{7})")
            retries += 1

    raise Exception(f"Element {elm_name} not found after {7} retries")






