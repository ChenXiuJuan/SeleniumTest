from config.Config import Log
from sql.FarmMapSql import FarmMap
from tools.Tool import Tool
import time
import unittest


class FarmInfo(unittest.TestCase):
    farm = FarmMap()
    log = Log("开始执行").logger
    tool = Tool()

    def external_farm_info(self, driver):
        self.log.info("--------------------开始执行地图上的外部蜂场信息校验case----------------------")
        address = driver.find_element_by_xpath(
            '//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[3]/span').text
        vehicle_length_get = driver.find_element_by_xpath(
            '//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[4]/div[1]/span').text
        vehicle_length = self.tool.replace(vehicle_length_get)
        expect_hive_num_get = driver.find_element_by_xpath(
            '//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[4]/div[2]/span').text
        expect_hive_num = str(self.tool.replace(expect_hive_num_get)).split('箱')[0]
        friend_name_get = driver.find_element_by_xpath(
            '//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[4]/div[3]/span').text
        friend_name = self.tool.replace(friend_name_get)
        contact_number_get = driver.find_element_by_xpath(
            '//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[4]/div[4]/span').text
        contact_number = self.tool.replace(contact_number_get)
        join_date_get = driver.find_element_by_xpath(
            '//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[4]/div[5]/span').text
        join_date = self.tool.replace(join_date_get)
        leave_date_get = driver.find_element_by_xpath(
            '//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[4]/div[6]/span').text
        leave_date = self.tool.replace(leave_date_get)
        plant_name = driver.find_element_by_xpath(
            '//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[2]/div/div').text
        creator = driver.find_element_by_xpath(
            '//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[5]/span').text
        time.sleep(5)
        while not creator != []:
            driver.refresh()
            time.sleep(10)
            creator = driver.find_element_by_xpath(
                '//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[5]/span').text
        creator_split = [x[:-1] for x in creator.split('：')[1].split('(')]
        creator_name = creator_split[0]
        creator_time = creator_split[1].replace('/', '-')
        swarm_info_list = self.farm.query_swarm_info(plant_name, creator_time, creator_name)
        address_info_sql = swarm_info_list[0].get('address')
        altitude_sql = round(swarm_info_list[0].get('altitude'), 2)
        address_sql = address_info_sql + '(海拔' + str(altitude_sql) + '米)'
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
            img = img_sql[i].get('url')
            img_split = img.split('中')
            img_list_sql = img_list_sql + list(img_split)
            i = i + 1
        img_path = driver.find_element_by_xpath(
            '//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div')
        img_path.click()
        time.sleep(3)
        img_list = []
        i = 0
        while i < 4:
            img = driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]/img').get_attribute('src').split('中')
            driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/img[3]').click()
            img_list = img_list + list(img)
            i = i + 1
        img_list.reverse()
        if img_list_sql == img_list:
            self.log.info('--------------------照片信息核对通过！------------------')
        else:
            raise Exception('--------------------照片信息核对失败！------------------')
        self.log.info("--------------------地图上的外部蜂场信息case校验通过----------------------")
        driver.refresh()
        time.sleep(5)

    def settle_farm_info(self, driver, i):
        self.log.info("--------------------开始执行地图上的待入驻/已入驻蜂场信息校验case----------------------")
        swarm_name = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[2]/div[1]/div/div').text
        address = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[2]/div[3]/span').text
        expect_hive_num_str = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[2]/div[4]/div[2]/span').text
        expect_hive_num = expect_hive_num_str.split('：')[1].split('箱')[0]
        if i == 1:
            creator = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[2]/div[6]/span').text
        else:
            creator = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[2]/div[7]/span').text
        while not creator != []:
            driver.refresh()
            time.sleep(10)
            creator = driver.find_element_by_xpath(
                '//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div/div[5]/span').text
        creator_split = [x[:-1] for x in creator.split('：')[1].split('(')]
        create_time = creator_split[1].replace('/', '-')
        swarm_sql = self.farm.query_swarm(swarm_name=swarm_name, address=address, expect_hive_num=expect_hive_num, create_time=create_time)
        if len(swarm_sql) != 0:
            self.log.info("--------------------地图上的待入驻/已入驻蜂场信息case校验通过----------------------")
        driver.refresh()
        time.sleep(5)






