from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver')
driver.get("http://www.baidu.com")
element = driver.find_element_by_id('kw')
element.send_keys('python', Keys.ARROW_DOWN)
element.clear()
