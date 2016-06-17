url = "https://www.bbdc.sg/bbweb/default.aspx"


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException

from pyvirtualdisplay import Display


from optparse import OptionParser


class auto_book(object):
    def __init__(self,options):
        display = Display(visible=0, size=(1024, 768))
        display.start()
        driver = webdriver.Firefox()
        driver.get(url)
        driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
        elem_nric = driver.find_element_by_name("txtNRIC")
        elem_nric.send_keys(options.username)
        elem_password = driver.find_element_by_name("txtPassword")
        elem_password.send_keys(options.password)
        elem_login = driver.find_element_by_name("btnLogin")
        elem_login.click()

    #def find_new_book(self):




if __name__ == '__main__':
    VERSION           = "1.00"
    parser = OptionParser(usage="usage: %prog --user --pwd --mail --mpwd --num --months", version="%prog "+VERSION)
    parser.add_option("--user", action="store", dest="username", help='web username')
    parser.add_option("--pwd", action="store", dest="password", help="web password")
    parser.add_option("--mail", action="store", dest="send_mail", help='mail address')
    parser.add_option("--mpwd", action="store", dest="mail_password", help='mail password')
    parser.add_option("--num", action="store", dest="booking_num", help='booking numbers')
    parser.add_option("--mon", action="store", dest="months", help='booking months')

    (options, args) = parser.parse_args()
    new_book = auto_book(options)
