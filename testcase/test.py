import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import unittest

caps = {
    'browserName': 'chrome',
    'loggingPrefs': {
        'browser': 'ALL',
        'driver': 'ALL',
        'performance': 'ALL',
    },
    'goog:chromeOptions': {
        'perfLoggingPrefs': {
            'enableNetwork': True,
        },
        'w3c': False,
    },
}


class test(unittest.TestCase):
    def test_01(self):
        driver = webdriver.Firefox(desired_capabilities=caps)

        driver.get('http://qa-gateway.worldfarm.com/fc-bee/admin/index/position-data')
        # 必须等待一定的时间，不然会报错提示获取不到日志信息，因为絮叨等所有请求结束才能获取日志信息
        time.sleep(3)

        request_log = driver.get_log('performance')
        print(request_log)

        for i in range(len(request_log)):
            message = json.loads(request_log[i]['message'])
            message = message['message']['params']
            # .get() 方式获取是了避免字段不存在时报错
            request = message.get('request')
            if(request is None):
                continue

            url = request.get('url')
            if(url == "http://qa-gateway.worldfarm.com/fc-bee/admin/index/position-data"):
                # 得到requestId
                print(message['requestId'])
                # 通过requestId获取接口内容
                content = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': message['requestId']})
                print(content)
                break

