from selenium.webdriver import ActionChains
from config.Config import Log


class Tool(object):
    L = Log('Tool')

    @staticmethod
    def parse_int(num):
        """
        数字串从后往前每隔三个数字加一个逗号， 例如:1234567 ---> 1,234,567
        :param num:数字串
        :return:
        """
        to_str = str(num)
        count = 0
        sumstr = ''
        for one_str in to_str[::-1]:
            count += 1
            if count % 3 == 0 and count != len(to_str):
                one_str = ',' + one_str
                sumstr = one_str + sumstr
            else:
                sumstr = one_str + sumstr
        return sumstr

    @staticmethod
    def replace(value):
        """
        将前端默认填充的“--”转换为None
        :param value:需要转换的字符
        :return:
        """
        value_split = str(value).split('：')
        value_split_1 = value_split[1]
        if value_split_1 == '--':
            value = None
        else:
            value = value_split_1
        return value

    @staticmethod
    def get_point(driver):
        """
        随机点击canvas画布，知道点到元素点
        :param driver: 驱动
        :return:
        """
        canvas = driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[1]/canvas[1]')
        canvas_style = driver.find_element_by_xpath(
            '//*[@id="staffMap"]/div[5]/div/div[1]/canvas[1]').get_attribute('style')
        canvas_split = canvas_style.split(';')
        height = ((canvas_split[2].split(':'))[1].split('px'))[0]
        width = ((canvas_split[3].split(':'))[1].split('px'))[0]
        hw_split = [{'height': int(height) / 2, 'width': int(width) / 2}, {'height': int(height), 'width': int(width)},
                    {'height': int(height), 'width': int(width) / 2}, {'height': int(height) / 2, 'width': int(width)}]
        for i in range(len(hw_split)):
            height = hw_split[i].get('height')
            width = hw_split[i].get('width')
            try:
                if driver.find_element_by_xpath('//*[@id="staffMap"]/div[5]/div/div[2]/div/div/div/div'):
                    print('------------------------已定位到canvas上的数据------------------------')
                    break
            except Exception as e:
                print('---------------循环点击暂未点击到元素---------------', e)
            finally:
                for x in range(int(height)):
                    for y in range(int(width)):
                        action_chains = ActionChains(driver)
                        action_chains.move_to_element(canvas)
                        action_chains.move_by_offset(x, y).click().perform()
                        y = y + 1
                        break
                    x = x + 1
                    break






