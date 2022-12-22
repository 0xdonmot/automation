from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import argparse


try:

    # set options
    options = Options()
    options.add_argument(
        "user-data-dir=/Users/miz/Library/Application Support/Google/Chrome/")
    options.add_argument(r"--profile-directory=Profile 1")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # start driver
    driver = webdriver.Chrome(
        "/Users/miz/Downloads/chromedriver", options=options)
    driver.maximize_window()
    url = 'https://app.duocards.com/library/edit?id=U291cmNlOjFlZDJiZWU3LWFlNWEtNGMyMi1hZDlkLTM5YzhiM2UzMjQxYw%3D%3D&action=cards'
    driver.get(url)

    # get words
    foreign_word = "mtihani"
    english_word = "to test"

    print("populate english word")
    # populate english word
    english_xpath = "/html/body/div[3]/div[3]/div/div/div[2]/div/div[2]/form/div[5]/div/input"
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, english_xpath))).send_keys(english_word)
    # wait for image to auto-update
    time.sleep(3)
    print("click image")
    # populate foreign word
    print("populate foreign word")
    foreign_xpath = "/html/body/div[3]/div[3]/div/div/div[2]/div/div[2]/form/div[4]/div/input"
    foreign_word_box = driver.find_element(By.XPATH, foreign_xpath)
    # This is needed to clear and update the auto-generated translation
    ActionChains(driver).move_to_element(
        foreign_word_box).double_click().click_and_hold().send_keys(Keys.CLEAR).send_keys(foreign_word).perform()
    print("click save")
    # click save
    save_class_selector = "#addCard"
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, save_class_selector))).click()
except Exception as e:
    print(e)
