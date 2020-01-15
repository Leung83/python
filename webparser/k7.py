#!/usr/bin/python
  
import time
import commands   # Module to execute Linux commands  
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

driver.get("https://www.jm.se/stockholm-lan/stockholm-kommun/liljeholmskajen/k7/41103")
time.sleep(2)

# Print all ids on page, used for developing
#ids = driver.find_elements_by_xpath('//*[@id]')
#for i in ids:
#    # print i.tag_name
#    print(i.get_attribute('id'))

status = driver.find_element_by_xpath('//*[@id="main-page"]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/span')

if "Reserverad" in str(status.get_attribute("innerHTML")):
        print str(status.get_attribute("innerHTML"))
else:
        print 'Send mail'
        # Need to have postfix configured with Gmail 
        # https://www.linode.com/docs/email/postfix/configure-postfix-to-send-mail-using-gmail-and-google-apps-on-debian-or-ubuntu/
        commands.getoutput('echo "https://www.jm.se/stockholm-lan/stockholm-kommun/liljeholmskajen/k7/41103" | mail -s "Apartment Status Changed" YOURMAIL@gmail.com')
