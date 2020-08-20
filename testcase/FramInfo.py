import json
import random
from selenium import webdriver
from config.Config import Log
from sql.FarmMapSql import FarmMap
from tools.Tool import Tool
import time
import unittest


class FarmInfo(unittest.TestCase):
    farm = FarmMap()
    log = Log("开始执行").logger
    tool = Tool()

    def test_farm_info(self, driver):
        canvas = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[1]/canvas[1]')
        # canvas = []
        # while not canvas != []:
        #     driver.refresh()
        #     time.sleep(10)
        #     canvas = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[1]/canvas[1]')
        # 点击地图的中心点
        canvas.click()
        if driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div') is True:
            self.log.info("--------------------已点击到蜂场信息----------------------")
            time.sleep(1)
            self.log.info("--------------------开始执行弹窗内蜂场信息校验case----------------------")
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
                i = i + 1
            m = img_list_sql.reverse()
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
            if img_list_sql == img_list:
                pass
            else:
                raise Exception('--------------------照片信息核对失败！------------------')
            # p = ActionChains(driver).move_to_element(canvas[0]).move_to_element_with_offset(256, 520).pause(2).click().perform()
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="staffMap"]/div[3]/div[2]').click()
            self.log.info("--------------------校验蜂场信息后，已重新刷新----------------------")
        else:
            self.log.info("--------------------未点击到蜂场信息----------------------")



