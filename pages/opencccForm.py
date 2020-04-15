import os
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.tools import Tools
from pages.useful_functions import password_Generator, random_four_digit_PIN, username_generator


class OpencccForm:

    def __init__(self, info, email):
        self.path = 'driver/chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=self.path)
        self.baseURL = 'https://www.opencccapply.net/uPortal/'
        self.driver.get(self.baseURL)

        self._firstname = info.get("firstname")
        self._lastname = info.get("lastname")
        self._ssn_number = info.get("ssn")
        self._phone_num = info.get("phone_num")
        self._alter_phone = info.get("parent_phone")
        self._emailid = email
        self._sex = info.get("sex")

        self.perform = Tools(self.driver)

        # birth_info
        #############################
        self._birth_month = None
        self._birth_day = None
        self._birth_year = None

        # address_info
        #############################
        self._street_address = None
        self._city = None
        self._state = None
        self._zipcode = None
        #############################

        # account_credentials
        ##################################
        self._username = None
        self._password = None
        self._PIN = None
        self._cccid = None

        self._security_question_1 = 'Where did your parents meet?'
        self._answer_1 = 'in Parallel universe'
        self._security_question_2 = 'What was the make and model of your first car?'
        self._answer_2 = 'Toyota Toy Car'
        self._security_question_3 = 'In what city or town was your first job?'
        self._answer_3 = 'Handjob city'

    # openccc_apply_page_2 ACTIONS
    ################################################################################

    def _set_name_stuff(self):
        self.perform.set_input_by_ID('inputFirstName', self._firstname)
        self.perform.click_button_by_ID('inputHasNoMiddleName')
        self.perform.set_input_by_ID('inputLastName', self._lastname)
        self.perform.click_button_by_ID('hasOtherNameNo')
        self.perform.click_button_by_ID('hasPreferredNameNo')

    def _set_DOB_stuff(self):

        birth_month = "3"
        birth_day = "24"
        # uncommemt next line 75 if you want random birth_year
        # birth_year = str(random.choice(range(1995, 1999)))
        birth_year = "1997"
        
        self.perform.set_date_box(birth_month, birth_day, None, 'inputBirthDateMonth', 'inputBirthDateDay', None)
        self.perform.set_input_by_ID('inputBirthDateYear', birth_year)
        self.perform.set_date_box(birth_month, birth_day, None, 'inputBirthDateMonthConfirm',
                                  'inputBirthDateDayConfirm', None)
        self.perform.set_input_by_ID('inputBirthDateYearConfirm', birth_year)

        self._birth_month = birth_month
        self._birth_day = birth_day
        self._birth_year = birth_year

    def _set_SSN_stuff(self):

        self.perform.click_button_by_ID('inputSSNTypeSSN')
        self.perform.set_input_by_ID('inputSsn', self._ssn_number)
        self.perform.set_input_by_ID('inputSsnConfirm', self._ssn_number)


    ################################################################################

    def click_continue_button(self):
        self.perform.click_button_by_ID('accountFormSubmit')

    # openccc_apply_page_2 ACTIONS
    ################################################################################

    def _set_email_stuff(self):
        self.perform.set_input_by_ID('inputEmail', self._emailid)
        self.perform.set_input_by_ID('inputEmailConfirm', self._emailid)

    def _set_telephone_stuff(self):
        self.perform.set_input_by_ID('inputSmsPhone', self._phone_num)
        self.perform.set_input_by_ID('inputAlternatePhone', self._alter_phone)

    def _set_random_address(self):

        address = {
            "street_address": ['326 5th St', '439 N Fairfax Ave', '300 E Sepulveda Blvd'],
            "city": ['Eureka', 'Los Angeles', 'Carson'],
            "zip_code": ['95501', ' 90036', '90745']
        }
        # uncomment this line if you want to try random address
        # Total_address = 3
        # index = random.choice(range(Total_address))
        index = 0
        street_address = address.get("street_address")[index]
        city = address.get("city")[index]
        zipcode = address.get("zip_code")[index]
        state = "CA"

        time.sleep(2)
        self.perform.set_input_by_ID('inputStreetAddress1', street_address)
        self.perform.set_input_by_ID('inputCity', city)
        self.perform.set_select_by_ID('inputState', state)
        self.perform.set_input_by_ID('inputPostalCode', zipcode)
        time.sleep(1)
        self._street_address = street_address
        self._city = city
        self._zipcode = zipcode
        self._state = state



    ################################################################################

    # openccc_apply_page_3 ACTIONS
    ################################################################################

    def _set_username_password(self):
        username_error_flag = True
        username = username_generator(8)
        password = password_Generator(14)
        while username_error_flag:
            try:
                username = username_generator(8)
                self.perform.set_input_by_ID('inputUserId', username)
                error = WebDriverWait(self.driver, 40).until(
                    EC.presence_of_element_located((By.ID, 'userIdStatus'))
                )
                username_error_flag = False
            except NoSuchElementException:
                username_error_flag = True

        self.perform.set_input_by_ID('inputPasswd', password)
        self.perform.set_input_by_ID('inputPasswdConfirm', password)

        self._username = username
        self._password = password

    def _set_PIN(self):
        PIN = random_four_digit_PIN()
        self.perform.set_input_by_ID('inputPin', PIN)
        self.perform.set_input_by_ID('inputPinConfirm', PIN)
        self._PIN = PIN

    def _set_security_questions(self):
        self.perform.set_select_by_ID('inputSecurityQuestion1', "1")
        self.perform.set_input_by_ID('inputSecurityAnswer1', self._answer_1)

        self.perform.set_select_by_ID('inputSecurityQuestion2', "2")
        self.perform.set_input_by_ID('inputSecurityAnswer2', self._answer_2)

        self.perform.set_select_by_ID('inputSecurityQuestion3', "16")
        self.perform.set_input_by_ID('inputSecurityAnswer3', self._answer_3)

    def solve_captha(self):
        os.system('cls')
        time.sleep(1)
        print("Psstt...I'm not smart enough to solve CAPTCHA by myself :(")
        time.sleep(2)
        print('need your Intelligence')
        time.sleep(2)
        print('Please solve captcha for me....^^,')
        time.sleep(2)
        is_solved = 'n'
        while is_solved != 'y':
            is_solved = input("Have you solved CAPTCHA (y/n) ? : ").lower()
            if is_solved != 'y':
                print("Okay solve i'm waiting....")
                time.sleep(12)
        time.sleep(1)
        print("Sshheeww....Thank you!....owe you EDU mail :D")

    def _account_created_page(self):
        waiting = True
        while waiting:
            try:
                cccid = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.ccc-id'))
                ).text
                self._cccid = cccid
                waiting = False
            except NoSuchElementException:
                waiting = True
        self.perform.click_button_by_XPATH('//*[@id="registrationSuccess"]/button')

    ################################################################################

    def _openccc_apply_page_1(self):
        self.perform.click_by_LINK_TEXT('Create an Account')
        self.perform.click_button_by_ID('accountFormSubmit')

        self._set_name_stuff()
        self._set_DOB_stuff()
        self._set_SSN_stuff()
        self.click_continue_button()

    def _openccc_apply_page_2(self):
        self._set_email_stuff()
        self._set_telephone_stuff()
        self._set_random_address()
        self.click_continue_button()

    def _openccc_apply_page_3(self):

        self._set_username_password()
        self._set_PIN()
        self._set_security_questions()
        self.solve_captha()
        self.click_continue_button()
        self._account_created_page()

    def _save_info(self):
        if int(self._birth_month) <= 9:
            birth_month = '0' + self._birth_month
        else:
            birth_month = self._birth_month
        edu_login_password = '88@' + self._firstname[0].upper() + birth_month + self._birth_day
        print("all info are saved!")

        with open("accountinfo.txt", 'a') as txtFile:
            txtFile.writelines("===================================================\n")
            txtFile.writelines("emailID ==> {}\n".format(self._emailid))
            txtFile.writelines("{}\n".format(self._cccid))
            txtFile.writelines("PIN number ==> {}\n".format(self._PIN))
            txtFile.writelines("OCC Username ==> {}\n".format(self._username))
            txtFile.writelines("OCC Password ==> {}\n".format(self._password))
            txtFile.writelines("SSN-Number ==> {}\n".format(self._ssn_number))
            txtFile.writelines("--------------EDU mail credentials-----------------\n")
            txtFile.writelines("If you got acceptance then only\n")
            txtFile.writelines("Goto this link ==> http://mycollege.laccd.edu/\n")
            txtFile.writelines("Enter Student Username==> [will be emailed to you]\n")
            txtFile.writelines("Enter Student password ==>{}\n".format(edu_login_password))
            txtFile.writelines("----------------------------------------------------\n\n")
            txtFile.writelines("_____Security Questions_____\n")
            txtFile.writelines("Q.1> {}\n".format(self._security_question_1))
            txtFile.writelines("A.1> {}\n".format(self._answer_1))
            txtFile.writelines("Q.2> {}\n".format(self._security_question_2))
            txtFile.writelines("A.2> {}\n".format(self._answer_2))
            txtFile.writelines("Q.3> {}\n".format(self._security_question_3))
            txtFile.writelines("A.3> {}\n".format(self._answer_3))
            txtFile.writelines("===================================================\n")


    # Main driver
    # ____________________________
    def fill(self):
        self._openccc_apply_page_1()
        self._openccc_apply_page_2()
        self._openccc_apply_page_3()
        self._save_info()
        self.driver.close()
        return self._username, self._password
