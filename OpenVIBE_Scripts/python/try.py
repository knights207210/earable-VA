import numpy
from selenium import webdriver
#https://sites.google.com/a/chromium.org/chromedriver/getting-started
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


# open browser first

driver = webdriver.Chrome("/Users/hanxu/Downloads/chromedriver")
#driver.fullscreen_window()
driver.get('https://developer.amazon.com/alexa/console/ask/test/amzn1.ask.skill.84d0b864-bcf0-4af5-a99b-abdc3b5b384d/development/en_US/')

username = "wangyichen5151@gmail.com"
password = "woailianlian"

elem_email=driver.find_element_by_id("ap_email")
elem_email.send_keys(username)
elem_ps = driver.find_element_by_id("ap_password")
elem_ps.send_keys(password)
elem_si = driver.find_element_by_id("signInSubmit")
elem_si.click()



command = "tell earablexuhan about to open the mouth"
elem = driver.find_element_by_class_name("askt-utterance__input")
elem.send_keys(command)
elem.send_keys(Keys.ENTER)
				