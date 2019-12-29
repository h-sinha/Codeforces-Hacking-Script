from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import os
import time
from checker import Checker

max_pages = 100
username = input("Enter your handle/email = ")
password = input("Enter password = ")
contest_id = input("Enter contest id = ")
problem_id = input("Enter problem id = ")

replace = {'&quot;': '\"', '&gt;': '>', '&lt;': '<', '&amp;': '&', "&apos;": "'"}
languages = {'GNU C++14':'GNU G++14 6.4.0', 'GNU C++11':'GNU G++11 5.1.0', 'GNU C++17':'GNU G++17 7.3.0', 'Java 8':'Java 11.0.5', 'Python 3': 'Python 3.7.2', 'Python 2':'Python 2.7.15'}
options = webdriver.ChromeOptions()
options.add_argument("--headless")  
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=options)

# load input and output
with open('input.txt', 'r') as myfile: 
	test_input = myfile.read()
with open('output.txt', 'r') as myfile: 
	test_output = myfile.read()

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

def Hack(contest_id, submission_id):
	hack_url = "https://codeforces.com/contest/"+contest_id+"/challenge/"+submission_id
	driver.get(hack_url)
	driver.implicitly_wait(60)
	print(hack_url)
	# upload testcase
	file_box = driver.find_element_by_name('testcaseFromFile')
	file_box.send_keys(os.path.join(os.getcwd(), 'input.txt'))
	# press hack button to hack solution
	submit = driver.find_element_by_class_name('submit')
	submit.submit()

def runCode(language, submission_id, contest_id, code):
	driver.get('https://codeforces.com/contest/'+contest_id+'/customtest')
	# select language
	select = Select(driver.find_element_by_name('programTypeId'))
	select.select_by_visible_text(languages[language])
	# enter code in editor
	text_box = driver.find_elements_by_class_name("ace_text-input")[0]
	text_box.send_keys(code)
	driver.implicitly_wait(100)
	# removing extra characters due to autocompletion in online ide
	for _ in range(2000):
		text_box.send_keys(Keys.DELETE);
	# input test case
	text_box = driver.find_elements_by_name("input")[0]
	text_box.send_keys(test_input)
	driver.implicitly_wait(10)
	# run code
	submit_button = driver.find_elements_by_name("submit")[0]
	submit_button.submit()
	# wait for code to run
	driver.implicitly_wait(10)
	time.sleep(10)
	st = time.time()
	output = "Running..."
	while output == "Running...":
		text_box = driver.find_element_by_name('output')
		output = text_box.get_attribute('value')
		# code runs for more than 10 seconds then hack
		if time.time() - st > 10:
			output = "hack"
			break
	if Checker(test_output, output):
		Hack(contest_id, submission_id)
	
#fetches the code corresponding to the parameter url
def getCode(submission_url, submission_id, contest_id):
	source = requests.get(submission_url).text
	soup = BeautifulSoup(source, "lxml")
	# find language
	language = soup.findAll('td')[3].text[6:-6]
	if language not in languages.keys():
		return
	code = soup.findAll('pre')[0].text
	code = parse(code).replace('\r', '')
	runCode(language, submission_id, contest_id, code)

#gets all accepted submission for a problem and calls helper functions
def getSubmissions(contest_id, problem_id, max_pages):
	page = 0
	max_pages = 1
	while page < max_pages:
		# try:
			url = "http://codeforces.com/contest/"+contest_id+"/status/"+problem_id+"/page/" + str(page) + "?order=BY_ARRIVED_DESC"
			source = requests.get(url).text
			soup = BeautifulSoup(source, "lxml")
			# get submission id and url
			submissions = soup.findAll('a', {'class':'view-source'})
			for submission in submissions:
				submission_url = "http://codeforces.com" + submission['href']
				getCode(submission_url, submission['submissionid'], contest_id)
			page += 1
		# except:
			# return

login(username, password)
getSubmissions(contest_id, problem_id, max_pages)