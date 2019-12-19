from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=options)
def login():
	driver.get('https://www.codeforces.com/enter')
	username = ""
	password = ""
	# enter username
	text_box = driver.find_element_by_id('handleOrEmail')
	text_box.send_keys(username)
	# enter password
	text_box = driver.find_element_by_id('password')
	text_box.send_keys(password)
	# click on login button
	login = driver.find_elements_by_xpath("//input[@value='Login']")[0]
	login.click()

login()