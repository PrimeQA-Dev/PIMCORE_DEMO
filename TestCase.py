import logging
import time
from selenium import webdriver
from utils import services_context_wrapper, Pac_Credentials, click_on_add_object
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import string, random
import time


# region:
SuccessCount = 0
FailureCount = 0
SkipCount = 0
Success_List = []
Failure_Cause = []
Execution_time = []


# endregion:

def test_demo_1():
    global SuccessCount, FailureCount
    st = time.time()
    try:
        with services_context_wrapper("test_demo_1.png") as driver:
            driver.maximize_window()
            Pac_Credentials.Login_store(driver)
            driver.implicitly_wait(10)
            logging.info("Login is successful.")
            Success_List_Append("T_1", "Test Demo 1", "Pass", "")
            Close_Driver(driver,st,"test_demo_1")

    except Exception as e:
        logging.error(e)
        logging.info("Error in - opening browser")
        Success_List_Append("T_1", "Test Demo 1", "Fail", e)
        Close_Driver(driver, st, "test_demo_1")
def test_demo_2():
    global SuccessCount, FailureCount
    st = time.time()
    driver = webdriver.Chrome()
    try:
        RANDOM_NAME = "From_Automation_" + "".join(random.choices(string.ascii_letters, k=7))
        with services_context_wrapper("test_demo_2.png") as driver:
            driver.maximize_window()
            Pac_Credentials.Login_store(driver)
            driver.implicitly_wait(10)
            logging.info("Login is successful.")

            # (WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Cars"]'))).click())
            click_on_add_object(
                driver, "Car")
            (WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '(//div[text()="Enter the name of the new item"])[1]'
                                                          '//parent::div//input'))).send_keys(RANDOM_NAME))
            (WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//span[text()="OK"]'))).click())
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "name"))).send_keys(RANDOM_NAME)
            driver.find_element(By.XPATH,'(//span[@class="x-btn-icon-el x-btn-icon-el-default-small pimcore_icon_search "])[1]').click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '(//div[@class="x-grid-cell-inner "]/../..)[1]')))
            manufacture = driver.find_element(By.XPATH, '(//div[@class="x-grid-cell-inner "]/../..)[1]')
            action = ActionChains(driver)
            action.double_click(manufacture).perform()
            time.sleep(1)
            driver.find_element(By.XPATH,'(//span[@class="x-btn-icon-el x-btn-icon-el-default-small pimcore_icon_search "])[1]').click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '(//div[@class="x-grid-cell-inner "]/../..)[1]')))
            body_style = driver.find_element(By.XPATH, '(//div[@class="x-grid-cell-inner "]/../..)[1]')
            action = ActionChains(driver)
            action.double_click(body_style).perform()
            time.sleep(1)
            driver.find_element(By.XPATH, '//input[@name="carClass"]').send_keys("City Car", Keys.TAB)
            time.sleep(2)
            driver.find_element(By.XPATH, '//input[@name="productionYear"]').send_keys("2008")
            time.sleep(2)
            driver.find_element(By.XPATH, '//li[text()="beige"]').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//input[@name="country"]').send_keys("Russia", Keys.TAB)
            time.sleep(2)
            driver.find_element(By.XPATH, '//span[text()="Save"]').click()
            saved_message = (WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//div[text()="Saved successfully!"]'))).is_displayed())
            logging.info(saved_message)
            assert saved_message
            Success_List_Append("T_2", "Test Demo 2", "Pass", "")
            time.sleep(10)
            Close_Driver(driver, st, "test_demo_1")

    except Exception as e:
        logging.error(e)
        logging.info("Error in - opening browser")
        Success_List_Append("T_2", "Test Demo 2", "Fail", e)
        Close_Driver(driver, st, "test_demo_1")

def test_demo_3():
    global SuccessCount, FailureCount
    st = time.time()
    try:
        with services_context_wrapper("test_demo_3.png") as driver:
            driver.maximize_window()
            driver.implicitly_wait(5)
            driver.get("https://demo.pimcore.com/admin/login?perspective=PIM")
            driver.find_element(By.XPATH, "//input[@name='username']").send_keys("failedcase")
            driver.find_element(By.XPATH, "//input[@name='password']").send_keys("testing")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            act_title = driver.find_element(
                By.XPATH, "//a[@id='pimcore_logout']"
            ).get_attribute("id")
            assert act_title == "pimcore_logout"
            Success_List_Append("T_3", "Test Demo 3", "Pass", "")
            Close_Driver(driver,st,"test_demo_3")

    except Exception as e:
        logging.error(e)
        logging.info("Error in - opening browser")
        Success_List_Append("T_3", "Test Demo 3", "Fail", str(e))
        Close_Driver(driver, st, "test_demo_1")

def Success_List_Append(testID, description, results, reason):
    global SuccessCount, FailureCount, SkipCount
    Success_List.append([testID, description, results, reason])
    if results == "Pass":
        SuccessCount += 1
        logging.info(testID)
        logging.info("Success Count = " + str(SuccessCount))
    elif results == "Fail":
        FailureCount += 1
        logging.info(testID)
        logging.info("Failure Count = " + str(FailureCount))
    elif results == "Skip":
        SkipCount += 1
        logging.info(testID)
        logging.info("Skipped Count = " + str(SkipCount))

def Close_Driver(driver, st, name):
    et = time.time()
    elapsed_time = round((et - st), 2)
    logging.info('Execution time:' + str(elapsed_time))
    Execution_time.append(str(elapsed_time))
