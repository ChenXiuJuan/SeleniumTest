import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path='C:\Program Files\Mozilla Firefox\geckodriver')

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get('https://www.python.org/')
        assert 'Python' in driver.title
        elem = driver.find_element_by_name('q')  # 元素定位
        elem.send_keys('pycon')  # 输入关键字
        elem.send_keys(Keys.RETURN)  # 输入RETURN
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
