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
    # opt = FirefoxOptions()
    # opt.headless = True        # 设置无界面浏览器模式

    def farmmap(self):
        self.log.info("----------------------开始执行登录case------------------------------")
        # 无界面浏览器
        # driver = Firefox(options=self.opt)
        # 有界面浏览器
        driver = webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver')
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
        self.log.info("--------------------开始执行外部蜂场统计case----------------------")
        # swarm = driver.find_element_by_xpath('/html/body/div/div/section/section/main/div[2]/div[1]/div/p[1]/span').text
        # swarm_count_format = None
        # sql_swarm_count = self.farm.query_swarm_count()[0]
        # # 累计蜂场个数
        # for key in sql_swarm_count:
        #     count = sql_swarm_count[key]
        #     # 格式化数字串
        #     swarm_count_format = str(self.tool.parse_int(count))
        # today_count_format = None
        # sql_today_new_swarm = self.farm.query_today_new_swarm()[0]
        # for key in sql_today_new_swarm:           # 当日新增蜂友数量
        #     count = sql_today_new_swarm[key]
        #     today_count_format = str(self.tool.parse_int(count))
        # external_farm = driver.find_element_by_xpath('/html/body/div/div/section/section/main/div[2]/div[1]/div/p[1]'
        #                                              '/span')
        # text = external_farm.text
        # if swarm_count_format in text:
        #     self.log.info('-----------------外部蜂场累计总个数检验通过-------------------')
        #     if today_count_format in text:
        #         self.log.info('-----------------当日新增外部蜂场数据检验通过-----------------')
        #     else:
        #         raise Exception('-----------------当日新增外部蜂场个数检验未通过，请核对！-------------------')
        #
        # else:
        #     raise Exception('-----------------外部蜂场累计总个数检验未通过，请核对！-------------------')
        # self.log.info("--------------------开始执行蜂友数量统计case----------------------")
        # friend = driver.find_element_by_xpath('/html/body/div/div/section/section/main/div[2]/div[1]/div/p[2]/span').text
        # sql_friend_have_user_id = (self.farm.query_num_bee_friend_have_user_id())[0].get('有手机号的蜂友数量')
        # sql_friend_not_user_id = (self.farm.query_num_bee_friend_not_user_id())[0].get('无手机号的蜂友数量')
        # sql_friend_all = str(self.tool.parse_int(sql_friend_have_user_id + sql_friend_not_user_id))
        # sql_friend_today = (self.farm.query_num_bee_friend_today())[0].get('今日新增蜂友')
        # sql_friend_today = self.tool.parse_int(sql_friend_today)
        # if sql_friend_all in friend:
        #     self.log.info("--------------------累计蜂友数量统计检验通过----------------------")
        #     if sql_friend_today in friend:
        #         self.log.info("--------------------今日新增蜂友数量统计检验通过----------------------")
        #     else:
        #         raise Exception("-----------------今日新增蜂友数量统计检验未通过，请核对！-------------------")
        # else:
        #     raise Exception("-----------------累计蜂友数量统计检验未通过，请核对！-------------------")
        # self.log.info("--------------------开始执行推广人员数量统计case----------------------")
        # promotion_staff = driver.find_element_by_xpath(
        #     '/html/body/div/div/section/section/main/div[2]/div[1]/div/p[3]/span').text
        # sql_promotion_staff = str(self.tool.parse_int((self.farm.query_num_promotion_staff())[0].get('COUNT(*)')))
        # if sql_promotion_staff in promotion_staff:
        #     self.log.info("--------------------推广人员数量统计检验通过----------------------")
        # else:
        #     raise Exception("-----------------推广人员数量统计检验未通过，请核对！-------------------")
        # self.log.info("--------------------开始执行自有蜂场数量统计case----------------------")
        # nectar_num = driver.find_element_by_xpath(
        #     '/html/body/div/div/section/section/main/div/div[1]/div/p[4]/span').text
        # sql_num_nectar = str(self.tool.parse_int((self.farm.query_num_nectar())[0].get('自有蜂场总数')))
        # sql_num_nectar_settled = str(self.tool.parse_int((self.farm.query_num_nectar_settled())[0].get('自有入驻蜂场数')))
        # if sql_num_nectar in nectar_num:
        #     self.log.info("--------------------自有蜂场总数统计检验通过----------------------")
        #     if sql_num_nectar_settled in nectar_num:
        #         self.log.info("--------------------自有已入驻蜂场总数统计检验通过----------------------")
        #     else:
        #         raise Exception("-----------------自有已入驻蜂场总数统计检验未通过，请核对！-------------------")
        # else:
        #     raise Exception("-----------------自有蜂场总数统计检验未通过，请核对！-------------------")
        # self.log.info("--------------------开始执行养蜂老师数量统计case----------------------")
        # beekeeper_teacher = driver.find_element_by_xpath(
        #     '/html/body/div/div/section/section/main/div/div[1]/div/p[5]/span').text
        # sql_beekeeper_teacher = str(self.tool.parse_int((self.farm.query_num_beekeeper_teacher())[0].get('自有养蜂人')))
        # if sql_beekeeper_teacher in beekeeper_teacher:
        #     self.log.info("-------------------养蜂老师数量统计检验通过----------------------")
        # else:
        #     raise Exception("-----------------养蜂老师数量统计检验未通过，请核对！-------------------")
        self.log.info("--------------------开始执行展示地图所有数据case----------------------")
        personnel_display = driver.find_element_by_xpath('//*[@id="staffMap"]/div[1]/div/div[1]').click()
        select_teacher = driver.find_element_by_xpath('//*[@id="staffMap"]/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/span[2]/span').click()
        select_promote = driver.find_element_by_xpath('//*[@id="staffMap"]/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/span[2]/span').click()
        apiary_display = driver.find_element_by_xpath('//*[@id="staffMap"]/div[2]/div/div[1]').click()
        to_be_settled_select = driver.find_element_by_xpath('//*[@id="staffMap"]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/span[3]/span').click()
        settled_select = driver.find_element_by_xpath('//*[@id="staffMap"]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[3]/span[3]/span').click()
        time.sleep(5)

        driver.close()


if __name__ == '__main__':
    farmmap = Farmmap()
    farmmap.farmmap()

