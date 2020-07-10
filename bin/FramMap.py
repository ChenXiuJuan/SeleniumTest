from selenium import webdriver
import time
from tools.Config import Log
from sql.FarmMap import FarmMap
from tools.Tool import Tool

farm = FarmMap()
log = Log("开始执行").logger
tool = Tool()
log.info("----------------------开始执行登录用例------------------------------")
driver = webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver')
driver.get("http://qa-flowers.zhuihuazu.com/login?from=%2Fdashboard%2Fmap")
time.sleep(5)
phone_login = driver.find_element_by_css_selector('.switchover___JHtst').click()
phone = driver.find_element_by_id('basic_mobile')
phone.send_keys('18683346691')
verifyCode = driver.find_element_by_id('basic_verifyCode')
verifyCode.send_keys('8888')
login = driver.find_element_by_css_selector('.ant-btn').click()
time.sleep(10)
driver.get('http://qa-flowers.zhuihuazu.com/dashboard/map')
log.info("--------------------开始执行蜂场统计数据看板模块----------------------")
time.sleep(5)
swarm = driver.find_element_by_xpath('/html/body/div/div/section/section/main/div[2]/div[1]/div/p[1]/span').text
sql_swarm_count = farm.query_swarm_count()[0]
for key in sql_swarm_count:
    count = sql_swarm_count[key]
    swarm_count_format = tool.parse_int(count)
sql_today_new_swarm = farm.query_today_new_swarm()[0]
for key in sql_today_new_swarm:
    count = sql_today_new_swarm[key]
    today_count_format = tool.parse_int(count)



