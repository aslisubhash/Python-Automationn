import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from pages.tools import Tools
from pages.useful_functions import new_tab, switch_to


class AccountDetail:

    def __init__(self):
        self.path = 'driver/chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=self.path)

        self._firstname = None
        self._fatherName = None
        self._lastname = None
        self._sex = None
        self._ssn = None
        self._phone_num = None
        self._parent_phone_num = None

    def _generate_names(self):
        print("Generating names......")
        perform = Tools(self.driver)
        baseURL = 'https://www.fakenamegenerator.com/'
        self.driver.get(baseURL)

        name_XPATH = '//*[@id="details"]/div[2]/div[2]/div/div[1]/h3'
        sex_value = random.choice(['male', 'female'])
        perform.set_select_by_ID('gen', sex_value)
        perform.click_button_by_ID('genbtn')
        time.sleep(5)
        name = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, name_XPATH))).text
        time.sleep(2)
        perform.set_select_by_ID('gen', 'male')
        perform.click_button_by_ID('genbtn')
        time.sleep(2)
        father_fullname = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, name_XPATH))).text
        father_fullname = father_fullname.split()

        self._firstname = name.split()[0]
        self._fatherName = father_fullname[0]
        self._lastname = father_fullname[2]
        if sex_value == 'male':
            self._sex = 'M'
        else:
            self._sex = 'F'

    def _generate_ssn(self):
        print("Generating SSN....")
        baseURL = 'https://www.ssn-verify.com/generate'
        perform = Tools(self.driver)
        state_control_ID = 'state'
        year_control_ID = 'year'
        btn_submit_ID = 'ssn-submit'
        result_ssn_CLASS_NAME = 'result-ssn'

        new_tab(self.driver, baseURL)
        switch_to(self.driver, 'generate')

        perform.set_select_by_ID(state_control_ID, "california")

        perform.set_select_by_ID(year_control_ID, "1997")

        perform.click_button_by_ID(btn_submit_ID)

        time.sleep(3)

        ssn_number = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, result_ssn_CLASS_NAME))).text

        self._ssn = ssn_number

    def _generate_phone_number(self):
        print("Generating phone numbers....")

        baseURL = 'https://www.fakephonenumber.org/UnitedStates/phone_number_generator?state=CA'

        new_tab(self.driver, baseURL)
        switch_to(self.driver, 'fakephonenumber')

        self._phone_num = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div/ul[1]/li[1]/p[1]/a'))).text
        self._parent_phone_num = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div/ul[1]/li[2]/p[1]/a'))).text

    def getInfo(self):
        info = {}
        self._generate_names()
        self._generate_ssn()
        self._generate_phone_number()
        print("Done!")
        info["firstname"] = self._firstname
        info["lastname"] = self._lastname
        info["sex"] = self._sex
        info["ssn"] = self._ssn
        info["fathername"] = self._fatherName
        info["phone_num"] = self._phone_num
        info["parent_phone"] = self._parent_phone_num

        self.driver.quit()
        return info
