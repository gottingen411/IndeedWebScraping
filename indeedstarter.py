from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import csv
# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\the\chromedriver.exe')
driver = webdriver.Firefox()
# Go to the page that we want to scrape
driver.get("https://www.indeed.com/jobs?q=data+science&explvl=mid_level&sort=date")

csv_file = open('indeedreviewmidlevel.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)



# Click review button to go to the review section
#review_button = driver.find_element_by_xpath('//a[@class="jobtitle turnstileLink"]')
#review_button.click()

# Page index used to keep track of where we are.
index = 1
# We want to start the first two pages.
# If everything works, we will change it to while True
while True:
	
                
	try:
		try:
        		close_popup1 = driver.find_element_by_xpath('//[@class="icl-CloseButton popover-x-button-close"]')
        		
        		#close_popup2 = driver.find_element_by_id('popover-background')
        		close_popup1.click()
        		#close_popup2.click()
        		time.sleep(2)
		except:
        		pass
        		
		print("Scraping Page number " + str(index))
		index = index + 1
		# Find all the reviews. The find_elements function will return a list of selenium select elements.
		# Check the documentation here: http://selenium-python.readthedocs.io/locating-elements.html
		wait_review1 = WebDriverWait(driver, 10)
		#reviews = driver.find_elements_by_xpath('//div[@class="jobsearch-SerpJobCard unifiedRow row result clickcard"]')
		reviews = wait_review1.until(EC.presence_of_all_elements_located((By.XPATH,
									'//div[@class="jobsearch-SerpJobCard unifiedRow row result clickcard"]')))
		# Iterate through the list and find the details of each review.
		for review in reviews:
			# Initialize an empty dictionary for each review
			review_dict = {}
			wait_review2 = WebDriverWait(driver, 20)
			# Use try and except to skip the review elements that are empty. 
			# Use relative xpath to locate the title.
			# Once you locate the element, you can use 'element.text' to return its string.
			# To get the attribute instead of the text of each element, use 'element.get_attribute()'
			
			try:
				title = review.find_element_by_xpath('.//h2[@class="title"]').text
			except:
				continue

			print('Title = {}'.format(title))

			# OPTIONAL: How can we deal with the "read more" button?
			
			# Use relative xpath to locate text, username, date_published, rating.
			# Your code here

			# Uncomment the following lines once you verified the xpath of different fields
			try:
				company = review.find_element_by_xpath('.//span[@class="company"]').text
			except:
				continue
			try:
				rating = review.find_element_by_xpath('.//span[@class="ratingsContent"]').text
			except:
				rating=None
			try:
				location =review.find_element_by_xpath('.//span[@class="location accessible-contrast-color-location"]').text
			except: 
				location=None
			try:	
				date = review.find_element_by_xpath('.//span[@class="date "]').text	
			except:
				pass
			try:
        			close_popup1 = driver.find_element_by_xpath('//a[@class="icl-CloseButton popover-x-button-close"]')
        		
        		#close_popup2 = driver.find_element_by_id('popover-background')
        			close_popup1.click()
        		#close_popup2.click()
        			time.sleep(2)
			except:
        			pass	
			review.click()
			desc = wait_review2.until(EC.presence_of_all_elements_located((By.XPATH,
									'//div[@id="vjs-desc"]')))
			time.sleep(1)
			try:
				n_reviews=review.find_element_by_xpath('//span[@class="slNoUnderline"]').text	
			except:
				n_reviews=None

			try:
				desc = review.find_element_by_xpath('//div[@id="vjs-desc"]').text
			except:
				desc=None

			review_dict['title'] = title
			review_dict['date'] = date
			review_dict['company'] = company
			review_dict['location']= location
			review_dict['description'] = desc
			review_dict['rating'] = rating
			review_dict['no of reviews']=n_reviews
			writer.writerow(review_dict.values())

		# We need to scroll to the bottom of the page because the button is not in the current view yet.
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Locate the next button element on the page and then call `button.click()` to click it.
		#button = driver.find_element_by_xpath('//span[@class="pn"]')
		#button.click()
		# Locate the next button on the page.
		wait_button = WebDriverWait(driver, 30)
		next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
									'//a[@aria-label="Next"]')))
		next_button.click()
		time.sleep(6)
	except Exception as e:
		print(e)
		driver.close()
		break
