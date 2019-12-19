from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import os

max_pages = 100
username = input("Enter your handle/email = ")
password = input("Enter password = ")
# contest_id = input("Enter contest id = ")
# problem_id = input("Enter problem id = ")
contest_id = "903"
problem_id = "A"

replace = {'&quot;': '\"', '&gt;': '>', '&lt;': '<', '&amp;': '&', "&apos;": "'"}
extension = {'GNU C++14':'cpp', 'GNU C++11':'cpp', 'GNU C++17':'cpp', 'Java 8':'java', 'Python 3': 'py', 'Python 2':'py'}
languages = {'GNU C++14':'GNU G++14 6.4.0', 'GNU C++11':'GNU G++11 5.1.0', 'GNU C++17':'GNU G++17 7.3.0', 'Java 8':'Java 11.0.5', 'Python 3': 'Python 3.7.2', 'Python 2':'Python 2.7.15'}
options = webdriver.ChromeOptions()
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=options)

def login(username, password):
	driver.get('https://www.codeforces.com/enter')
	# enter username
	text_box = driver.find_element_by_id('handleOrEmail')
	text_box.send_keys(username)
	# enter password
	text_box = driver.find_element_by_id('password')
	text_box.send_keys(password)
	# click on login button
	login = driver.find_elements_by_xpath("//input[@value='Login']")[0]
	login.click()
	# wait for 60 seconds
	driver.implicitly_wait(60)

def parse(code):
	for key in replace.keys():
		code = code.replace(key, replace[key])
	return code

def runCode(language):
	driver.get('https://codeforces.com/problemset/customtest')
	driver.find_element_by_name("inputFile").send_keys(os.path.join(os.getcwd(),'./code.'+extension[language]))
	select = Select(driver.find_element_by_name('programTypeId'))
	select.select_by_visible_text(languages[language])
	text_box = driver.find_elements_by_name("input")[0]
	text_box.send_keys("sa")

#fetches the code corresponding to the parameter url
def getCode(submission_url):
	source = requests.get(submission_url).text
	soup = BeautifulSoup(source, "lxml")
	# find language
	language = soup.findAll('td')[3].text[6:-6]
	if language not in extension.keys():
		return
	code = soup.findAll('pre')[0].text
	code = parse(code).replace('\r', '')
	with open('code.' + extension[language], 'w+') as f:
		f.write(code)
	f.close()
	runCode(language)

#gets all accepted submission for a problem and calls helper functions
def getSubmissions(contest_id, problem_id, max_pages):
	page = 0
	max_pages = 1
	while page < max_pages:
		url = "http://codeforces.com/contest/"+contest_id+"/status/"+problem_id+"/page/" + str(page) + "?order=BY_ARRIVED_ASC"
		source = requests.get(url).text
		soup = BeautifulSoup(source, "lxml")
		# get submission id and url
		submissions = soup.findAll('a', {'class':'view-source'})
		for submission in submissions:
			submission_url = "http://codeforces.com" + submission['href']
			getCode(submission_url)
			return
		page += 1
login(username, password)
getSubmissions(contest_id, problem_id, max_pages)