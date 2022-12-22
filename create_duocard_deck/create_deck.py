from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import argparse


try:
    # initialise parser
    parser = argparse.ArgumentParser(description="parse language")
    parser.add_argument("language", action="store", type=str)
    parser.add_argument("rows_set", action="store", type=int)
    parser.add_argument("filepath", action="store", type=str, default=None)
    parser.add_argument("pack_text_name", action="store",
                        type=str, default=None)
    parser.add_argument("--use_duocards_translation",
                        action="store_true")
    # get args
    args = parser.parse_args()
    language = args.language
    rows_set = args.rows_set
    filepath = args.filepath
    pack_text_name = args.pack_text_name
    use_duocards_translation = args.use_duocards_translation
    print(args)

    max_cards = 200
    min_row = (rows_set-1)*max_cards
    max_row = min_row + 200

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
    url = 'https://app.duocards.com/library/edit?kind=set'
    driver.get(url)
    # populate pack name
    if not pack_text_name:
        pack_text_name = f'Top 1000 {language} words - Words {min_row} to {max_row}'
    else:
        pack_text_name += f" Words {min_row} to {max_row}"
    pack_title_selector = "#\:r9\:"
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, pack_title_selector))).send_keys(pack_text_name)
    # press continue
    continue_selector = "#createsourceform > button"
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, continue_selector))).click()  # first click
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, continue_selector))).click()  # second click
    # open data csv
    if filepath:
        data = pd.read_csv(filepath)
    else:
        data = pd.read_csv(f"../top_{language}_1000_words")
    # filter data, as max words are 200
    data = data.iloc[min_row: max_row]

    # iterate over data rows
    for index, row in data.iterrows():
        try:
            if (index + 1) % 20 == 0:
                print(f"Reached word {index + 1}...")
            # get words
            foreign_word = row[language]
            english_word = row['in english']

            # populate english word
            english_xpath = "/html/body/div[3]/div[3]/div/div/div[2]/div/div[2]/form/div[5]/div/input"
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, english_xpath))).send_keys(english_word)
            # wait for image to auto-update
            time.sleep(2)
            if not use_duocards_translation:
                # populate foreign word
                foreign_xpath = "/html/body/div[3]/div[3]/div/div/div[2]/div/div[2]/form/div[4]/div/input"
                foreign_word_box = driver.find_element(By.XPATH, foreign_xpath)
                # This is needed to clear and update the auto-generated translation
                ActionChains(driver).move_to_element(
                    foreign_word_box).double_click().click_and_hold().send_keys(Keys.CLEAR).send_keys(foreign_word).perform()
            # click save
            save_class_selector = "#addCard"
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, save_class_selector))).click()
        except UnexpectedAlertPresentException:  # repeated words
            continue
    print("Finished uploading!")
except Exception as e:
    print(e)
