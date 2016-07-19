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

from optparse import OptionParser
import time

from mail import mail

send_to = ['']

#from pyvirtualdisplay import Display# fireforx in ubuntu

def moveAndClick(elem) :
    ActionChains(driver).move_to_element(elem).perform()
    time.sleep(0.1)
    elem.click()

sessions = ['1']
days = ['1','2','3','4'] # 1 = Sun, 2 = Mon, 3 = Tue, 4 = Wed, 5 = Thu, 6 = Fri, 7 = Sat
url = "https://www.bbdc.sg/bbweb/default.aspx"



class auto_book(object):
    driver  = None;
    def __init__(self,options):
        #display = Display(visible=0, size=(1024, 768))
        #display.start()#fireforx in ubuntu
        # using chrome need driver
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.get(url)
        self.login_in_booking_system(options)


    def login_in_booking_system(self,options):
        self.driver.switch_to_frame(self.driver.find_element_by_tag_name("iframe"))
        elem_nric = self.driver.find_element_by_name("txtNRIC")
        elem_nric.send_keys(options.username)
        elem_password = self.driver.find_element_by_name("txtPassword")
        elem_password.send_keys(options.password)
        elem_login = self.driver.find_element_by_name("btnLogin")
        elem_login.click()

        #begin to book and count the times
        self.driver.switch_to_frame(self.driver.find_element_by_name("leftFrame"))
        self.driver.find_element_by_link_text('Booking without Fixed Instructor').click()
        self.driver.switch_to_default_content()

        #push "I Agree" button in the main frame
        self.driver.switch_to_frame(self.driver.find_element_by_name("mainFrame"))
        self.driver.find_element_by_xpath("//input[@value='I Agree']").click()

    def slot_set(self,options):
        self.driver.find_element_by_xpath("//input[@value='"+ options.months + "/2016']").click() #stirng example: "//input[@value='Apr/2016']"
        #choose sessions
        for session in sessions :
            opt_session = "//input[@name='Session'][@value='" + session + "']" #string example: "//input[@name='Session'][@value='1']"
            self.driver.find_element_by_xpath(opt_session).click()
        #choose days
        for day in days :
            opt_day = "//input[@name='Day'][@value='"+ day + "']" #string example: "//input[@name='Day'][@value='2']"
            self.driver.find_element_by_xpath(opt_day).click()

    def search_book(self,options):

        #push search button
        elem_link_Search = self.driver.find_element_by_xpath("//input[@value='Search']")
        elem_link_Search.click()

        #check result
        #deal with the alert when there has been already a booked session in the user account
        try:
            WebDriverWait(self.driver, 1).until(EC.alert_is_present())
            self.driver.switch_to_alert().accept()
            no_alert = False
        except TimeoutException:
            no_alert = True

    def Check_result(self,options):
        try:
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, "error")))
            print "no slot"
            elem_back = self.driver.find_element_by_xpath("//input[@value='<< Back']")
            elem_back.click()
            return 'no book'
        except UnexpectedAlertPresentException:
            print "a undefine error"
            return 'no book'
        except TimeoutException:
            #find place:
            for index in range(len(elem_slots)):
                moveAndClick(elem_slots[index])
                options.booking_num = options.booking_num - 1
                if booking_count == 0 :
                    break
            #submit
            submit = driver.find_element_by_xpath("//input[@type='button'][@value='Submit']")
            moveAndClick(submit)
            #confirm
            time.sleep(1)
            driver.find_element_by_xpath("//input[@type='submit'][@value='Confirm']").click()
            sessionInfo = driver.find_elements_by_xpath("//td[@class='txt']")
            msg_sessionInfo = ''
            for element in sessionInfo :
                msg_sessionInfo = msg_sessionInfo + element.text + '\n''
            print msg_sessionInfo
            driver.find_element_by_xpath("//input[@name='btnBooking'][@value='New Booking']").click()
            return msg_sessionInfo
        


if __name__ == '__main__':
    VERSION           = "1.00"
    parser = OptionParser(usage="usage: %prog --user --pwd --mail --mpwd --num --mon", version="%prog "+VERSION)
    parser.add_option("--user", action="store", dest="username", help='web username')
    parser.add_option("--pwd", action="store", dest="password", help="web password")
    parser.add_option("--mail", action="store", dest="send_mail", help='gmail address')
    parser.add_option("--mpwd", action="store", dest="mail_password", help='mail password')
    parser.add_option("--num", action="store", dest="booking_num", type = "int",help='booking numbers')
    parser.add_option("--mon", action="store", dest="months", help='booking months')

    (options, args) = parser.parse_args()
    if not options.username or \
       not options.password or \
       not options.send_mail or \
       not options.mail_password or \
       not options.booking_num or \
       not options.months:
        parser.print_usage()
        exit()

    new_book = auto_book(options)
    new_book.slot_set(options)

    while 1:
        try:
            new_book.search_book(options)
            result = new_book.Check_result(options)
            if result != 'no book':
                time.sleep(2)
                mail.send_mail(send_mail,mail_password,send_to,'new booking',result)
                new_book.slot_set(options)
            else:
                time.sleep(2)
        except KeyboardInterrupt:
            exit()
