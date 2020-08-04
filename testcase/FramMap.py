from selenium import webdriver
from config.Config import Log
from sql.FarmMapSql import FarmMap
from tools.Tool import Tool
import time
import unittest
from selenium.webdriver import Firefox, FirefoxOptions, ActionChains


class Farmmap(unittest.TestCase):
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
        time.sleep(10)
        self.log.info("--------------------开始执行蜂场统计数据看板模块case----------------------")
        time.sleep(10)
        self.log.info("--------------------开始执行外部蜂场统计case----------------------")
        swarm = driver.find_element_by_xpath('/html/body/div/div/section/section/main/div/div[1]/div/p[2]/span').text
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
        time.sleep(5)
        external_farm = driver.find_element_by_xpath('//*[@id="countTotal"]/div/p[1]/span')
        text = external_farm.text
        if swarm_count_format in text:
            self.log.info('-----------------外部蜂场累计总个数检验通过-------------------')
            if today_count_format in text:
                self.log.info('-----------------当日新增外部蜂场数据检验通过-----------------')
            else:
                raise Exception('-----------------当日新增外部蜂场个数检验未通过，请核对！-------------------')

        else:
            raise Exception('-----------------外部蜂场累计总个数检验未通过，请核对！-------------------')
        self.log.info("--------------------开始执行蜂友数量统计case----------------------")
        friend = driver.find_element_by_xpath('//*[@id="countTotal"]/div/p[2]/span').text
        sql_friend_have_user_id = (self.farm.query_num_bee_friend_have_user_id())[0].get('有手机号的蜂友数量')
        sql_friend_not_user_id = (self.farm.query_num_bee_friend_not_user_id())[0].get('无手机号的蜂友数量')
        sql_friend_all = str(self.tool.parse_int(sql_friend_have_user_id + sql_friend_not_user_id))
        sql_friend_today = (self.farm.query_num_bee_friend_today())[0].get('今日新增蜂友')
        sql_friend_today = self.tool.parse_int(sql_friend_today)
        if sql_friend_all in friend:
            self.log.info("--------------------累计蜂友数量统计检验通过----------------------")
            if sql_friend_today in friend:
                self.log.info("--------------------今日新增蜂友数量统计检验通过----------------------")
            else:
                raise Exception("-----------------今日新增蜂友数量统计检验未通过，请核对！-------------------")
        else:
            raise Exception("-----------------累计蜂友数量统计检验未通过，请核对！-------------------")
        self.log.info("--------------------开始执行推广人员数量统计case----------------------")
        promotion_staff = driver.find_element_by_xpath(
            '//*[@id="countTotal"]/div/p[3]/span').text
        sql_promotion_staff = str(self.tool.parse_int((self.farm.query_num_promotion_staff())[0].get('COUNT(*)')))
        if sql_promotion_staff in promotion_staff:
            self.log.info("--------------------推广人员数量统计检验通过----------------------")
        else:
            raise Exception("-----------------推广人员数量统计检验未通过，请核对！-------------------")
        self.log.info("--------------------开始执行自有蜂场数量统计case----------------------")
        nectar_num = driver.find_element_by_xpath(
            '//*[@id="countTotal"]/div/p[4]/span').text
        sql_num_nectar = str(self.tool.parse_int((self.farm.query_num_nectar())[0].get('自有蜂场总数')))
        sql_num_nectar_settled = str(self.tool.parse_int((self.farm.query_num_nectar_settled())[0].get('自有入驻蜂场数')))
        if sql_num_nectar in nectar_num:
            self.log.info("--------------------自有蜂场总数统计检验通过----------------------")
            if sql_num_nectar_settled in nectar_num:
                self.log.info("--------------------自有已入驻蜂场总数统计检验通过----------------------")
            else:
                raise Exception("-----------------自有已入驻蜂场总数统计检验未通过，请核对！-------------------")
        else:
            raise Exception("-----------------自有蜂场总数统计检验未通过，请核对！-------------------")
        self.log.info("--------------------开始执行养蜂老师数量统计case----------------------")
        beekeeper_teacher = driver.find_element_by_xpath(
            '//*[@id="countTotal"]/div/p[5]/span').text
        sql_beekeeper_teacher = str(self.tool.parse_int((self.farm.query_num_beekeeper_teacher())[0].get('自有养蜂人')))
        if sql_beekeeper_teacher in beekeeper_teacher:
            self.log.info("-------------------养蜂老师数量统计检验通过----------------------")
        else:
            raise Exception("-----------------养蜂老师数量统计检验未通过，请核对！-------------------")
        self.log.info("--------------------开始执行展示地图所有数据case----------------------")
        driver.find_element_by_xpath('//*[@id="staffMap"]/div[1]/div/div[1]').click()
        driver.find_element_by_xpath('//*[@id="staffMap"]/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/span[2]/span').click()
        driver.find_element_by_xpath('//*[@id="staffMap"]/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/span[2]/span').click()
        driver.find_element_by_xpath('//*[@id="staffMap"]/div[2]/div/div[1]').click()
        driver.find_element_by_xpath('//*[@id="staffMap"]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/span[3]/span').click()
        driver.find_element_by_xpath('//*[@id="staffMap"]/div[2]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[3]/span[3]/span').click()
        # 页面刷新
        canvas = []
        while not canvas != []:
            driver.refresh()
            time.sleep(10)
            canvas = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[1]/canvas[1]')
        canvas.click()
        time.sleep(5)
        address = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[3]/span').text
        vehicle_length_get = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[4]/div[1]/span').text
        vehicle_length = self.tool.replace(vehicle_length_get)
        expect_hive_num_get = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[4]/div[2]/span').text
        expect_hive_num = str(self.tool.replace(expect_hive_num_get)).split('箱')[0]
        friend_name_get = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[4]/div[3]/span').text
        friend_name = self.tool.replace(friend_name_get)
        contact_number_get = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[4]/div[4]/span').text
        contact_number = self.tool.replace(contact_number_get)
        join_date_get = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[4]/div[5]/span').text
        join_date = self.tool.replace(join_date_get)
        leave_date_get = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[4]/div[6]/span').text
        leave_date = self.tool.replace(leave_date_get)
        plant_name = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[2]/div/div').text
        creator = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[5]/span').text
        time.sleep(5)
        creator_split =[x[:-1] for x in creator.split('：')[1].split('(')]
        creator_name = creator_split[0]
        creator_time = creator_split[1].replace('/', '-')
        swarm_info_list = self.farm.query_swarm_info(plant_name, creator_time, creator_name)
        address_sql = swarm_info_list[0].get('address')
        vehicle_length_sql_key = swarm_info_list[0].get('vehicle_length')
        vehicle_length_get_sql = self.farm.query_config_value(10003, vehicle_length_sql_key)[0].get('value')
        expect_hive_num_sql = swarm_info_list[0].get('expect_hive_num')
        friend_name_sql = swarm_info_list[0].get('user_name')
        contact_number_sql = swarm_info_list[0].get('contact_number')
        join_date_sql = swarm_info_list[0].get('join_date')
        leave_date_sql = swarm_info_list[0].get('leave_date')
        self.assertEqual(address, address_sql)
        self.assertEqual(vehicle_length, vehicle_length_get_sql)
        self.assertEqual(int(expect_hive_num), expect_hive_num_sql)
        self.assertEqual(friend_name, friend_name_sql)
        self.assertEqual(contact_number, contact_number_sql)
        self.assertEqual(join_date, join_date_sql)
        self.assertEqual(leave_date, leave_date_sql)
        swarm_id = swarm_info_list[0].get('id')
        img_sql = self.farm.query_swarm_info_img(swarm_id)
        img_list_sql = []
        i = 0
        while i < 4:
            img = img_sql[0].get('url')
            img_split = img.split('中')
            img_list_sql = img_list_sql + list(img_split)
            i = i +1
        img_path = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div')
        img_path.click()
        time.sleep(3)
        img_list = []
        i = 0
        while i < 4:
            img = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]/img').get_attribute('src').split('中')
            driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/img[3]').click()
            img_list = img_list + list(img)
            i = i + 1
        if img_list_sql == img_list:
            pass
        else:
            raise Exception('--------------------照片信息核对失败！------------------')
        time.sleep(5)
        # p = ActionChains(driver).move_to_element(canvas[0]).move_to_element_with_offset(256, 520).pause(2).click().perform()
        time.sleep(5)
        driver.close()


if __name__ == '__main__':
    farmmap = Farmmap()
    farmmap.farmmap()

