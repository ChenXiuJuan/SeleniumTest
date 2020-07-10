from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver')
driver.get("http://qa-flowers.zhuihuazu.com/dashboard/map")
# element = driver.find_element_by_id('kw')
# element.send_keys('python', Keys.ARROW_DOWN)
# element.clear()
# element = driver.find_element_by_xpath('//ul//li[@class="bdsug-overflow"]')
# time.sleep(2)
# element = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[5]/div[2]/div/form/div/ul')
# select = Select(driver.find_elements_by_name('bdsug-overflow'))

# click = (select.select_by_index(index=1)).clike
# select.select_by_visible_text('')
# all_options = element.find_elements_by_class_name("bdsug-overflow")
# for option in all_options:
#     i = option
#     m = print('Value is: %s') % option.get_attribute("text")
#     option.click()
