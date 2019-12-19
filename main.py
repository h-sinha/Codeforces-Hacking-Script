from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup

max_pages = 100
# username = input("Enter your handle/email = ")
# password = input("Enter password = ")
# contest_id = input("Enter contest id = ")
# problem_id = input("Enter problem id = ")
contest_id = "903"
problem_id = "A"

replace = {'&quot;': '\"', '&gt;': '>', '&lt;': '<', '&amp;': '&', "&apos;": "'"}

# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=options)
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

#fetches the code corresponding to the parameter url
def getCode(submission_url):
	source = requests.get(submission_url).text
	soup = BeautifulSoup(source, "lxml")
	# find language
	language = soup.findAll('td')[3].text[6:-6]
	code = soup.findAll('pre')[0].text
	code = parse(code).replace('\r', '')
	print(code)

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
# login(username, password)
getSubmissions(contest_id, problem_id, max_pages)