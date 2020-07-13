from selenium import webdriver
import time
from config.Config import Log
from sql.FarmMapSql import FarmMap
from tools.Tool import Tool
from selenium.webdriver import Firefox, FirefoxOptions


class Farmmap(object):
    farm = FarmMap()
    log = Log("开始执行").logger
    tool = Tool()
    opt = FirefoxOptions()
    opt.headless = True        # 设置无界面浏览器模式

    def farmmap(self):
        self.log.info("----------------------开始执行登录case------------------------------")
        # 无界面浏览器
        driver = Firefox(options=self.opt)
        # 有界面浏览器
        # driver = webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver')
        driver.get("http://qa-flowers.zhuihuazu.com/login?from=%2Fdashboard%2Fmap")
        time.sleep(5)
        # 切换到手机号登录
        driver.find_element_by_css_selector('.switchover___JHtst').click()
        # 定位手机号输入框
        phone = driver.find_element_by_id('basic_mobile')
        phone.send_keys('18683346691')
        # 定位验证码输入框
        verifyCode = driver.find_element_by_id('basic_verifyCode')
        verifyCode.send_keys('8888')
        # 点击登录按钮
        driver.find_element_by_css_selector('.ant-btn').click()
        time.sleep(10)
        # 切换页面至数据看板-蜂场蜂场页面
        driver.get('http://qa-flowers.zhuihuazu.com/dashboard/map')
        self.log.info("--------------------开始执行蜂场统计数据看板模块case----------------------")
        time.sleep(5)
        self.log.info("--------------------外部蜂场统计case----------------------")
        swarm = driver.find_element_by_xpath('/html/body/div/div/section/section/main/div[2]/div[1]/div/p[1]/span').text
        swarm_count_format = None
        sql_swarm_count = self.farm.query_swarm_count()[0]
        # 累计蜂场个数
        for key in sql_swarm_count:
            count = sql_swarm_count[key]
            # 格式化数字串
            swarm_count_format = str(self.tool.parse_int(count))
        today_count_format = None
        sql_today_new_swarm = self.farm.query_today_new_swarm()[0]
        for key in sql_today_new_swarm:           # 当日新增蜂友数量
            count = sql_today_new_swarm[key]
            today_count_format = str(self.tool.parse_int(count))
        external_farm = driver.find_element_by_xpath('/html/body/div/div/section/section/main/div[2]/div[1]/div/p[1]'
                                                     '/span')
        text = external_farm.text
        if swarm_count_format in text:
            self.log.info('-----------------外部蜂场累计总个数检验通过-------------------')
            if today_count_format in text:
                self.log.info('-----------------当日新增外部蜂场数据检验通过-----------------')
            else:
                raise Exception('-----------------当日新增外部蜂场个数校验失败，请核对！-------------------')

        else:
            raise Exception('-----------------外部蜂场累计总个数校验失败，请核对！-------------------')

        driver.close()


if __name__ == '__main__':
    farmmap = Farmmap()
    farmmap.farmmap()



