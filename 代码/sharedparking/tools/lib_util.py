from pymouse import PyMouse
from pykeyboard import PyKeyboard
import os
from selenium.webdriver.common.by import By

from sharedparking.start.test_report import TestReport
from sharedparking.tools.util import LogUtil, FileUtil
import requests


class APIUtil:
    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'lib_util.UiUtil'))
    session = requests.Session()

    @classmethod
    def get_session(cls):
        """
        获取具有权限的session
        :return: 带登录cookie的session
        """
        try:
            image_url = FileUtil.get_ini_value('..\\conf\\base.ini', 'api', 'login_cookie_uri')
            cls.session.get(image_url)
        except:
            cls.logger.error(f'..\\conf\\base.ini路径下api配置文件错误,session生成错误')
        return cls.session

    @classmethod
    def request(cls, method, url, data=None):
        """
        发送请求获得响应
        :param method: 请求方式
        :param url: 请求url
        :param data: 请求数据
        :return: 响应结果
        """
        session = cls.get_session()
        main_url = 'http://172.16.13.223:8080'
        resp = getattr(session, method)(main_url + url, params=data)
        return resp

    @classmethod
    def assert_api(cls, test_info):
        for info in test_info:
            try:
                resp = APIUtil.request(info['request_method'], info['uri'], info['params'])
                Assert.assert_equal(resp.text, info['expect'])
            except:
                cls.logger.error(f"{info['request_method'], info['uri'], info['params']} 测试数据错误")
                break


# *****************************************************************************

class UiUtil:

    driver = None
    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'lib_util.UiUtil'))
    mouse = PyMouse()
    keyboard = PyKeyboard()

    @classmethod
    def get_driver(cls):

        from selenium import webdriver
        try:
            browser = FileUtil.get_ini_value('..\\conf\\base.ini', 'ui', 'browser')
            base_url = FileUtil.get_ini_value('..\\conf\\base.ini', 'ui', 'homepage_url')
            if cls.driver is None:
                cls.driver = getattr(webdriver, browser)()
                cls.driver.implicitly_wait(5)
                cls.driver.maximize_window()
                cls.driver.get(base_url)
        except:
            cls.logger.error('浏览器driver对象生成错误，请检查 ..\\conf\\base.ini UI配置文件')
        return cls.driver

    @classmethod
    def get_driver1(cls, browser='Firefox'):
        from selenium import webdriver
        # 保证webdriver只实例化一次，里面只有一个drive在传递
        if cls.driver is None:
            if browser == 'Chrome':
                cls.driver = webdriver.Chrome()
                cls.driver.maximize_window()
                cls.driver.implicitly_wait(5)
            else:
                cls.driver = webdriver.Firefox()
                cls.driver.maximize_window()
                cls.driver.implicitly_wait(5)
            return cls.driver
        return cls.driver

    @classmethod
    def find_element(cls, section, option):
        try:
            attr_element = FileUtil.get_ini_section('..\\conf\\inspector.ini', section)
            for element in attr_element:
                if option in element.keys():
                    attr = eval(element[option])
            return cls.driver.find_element(getattr(By, attr[0]), attr[1])
        except:
            cls.logger.error(f'读取 ..\\conf\\inspector.ini路径下{section}配置文件错误')
            return None

    @classmethod
    def input(cls, element, value):
        """
        对文本输入框执行点击、清理和输入值的动作
        :param element:文本元素对象
        :param value:向文本框输入的值
        :return:无
        """
        element.click()
        element.clear()
        element.send_keys(value)

    @classmethod
    def click(cls, element):
        """
        点击某个元素
        :param element:任何一个元素对象
        :return:无
        """
        element.click()

    @classmethod
    def alter_seletor_input_childdata(cls, element, value):
        """
        将选择日期框修改为可直接输入
        :param element: 操作元素
        :param value:
        :return:无
        """
        js = "$('input[id=childdate]').attr('readonly','')"  # 设置为空
        cls.driver.execute_script(js)  # 执行设置为空
        element.send_keys(value)

    @classmethod
    def alter_seletor_input(cls, element, what, value):
        """
        将选择日期框修改为可直接输入
        :param element: 操作元素
        :param what: 元素定位方式  例如：[id=childdate]
        :param value:
        :return:无
        """
        element_path = cls.get_driver().find_element_by_id(element)
        js = f"$(f'input[{what}]').attr('readonly','')"  # 设置为空
        cls.driver.execute_script(js)  # 执行设置为空
        element_path.send_keys(value)

    @classmethod
    def alter_seletor_input_earlystoretime(cls, element, value):
        """
        将选择日期框修改为可直接输入
        :param element: 操作元素
        :param value:
        :return:无
        """
        js = "$('input[id=earlystoretime]').attr('readonly','')"  # 设置为空
        cls.driver.execute_script(js)  # 执行设置为空
        element.send_keys(value)

    @classmethod
    def alter_seletor_input_laststoretime(cls, element, value):
        """
        将选择日期框修改为可直接输入
        :param element: 操作元素
        :param value:
        :return:无
        """
        js = "$('input[id=laststoretime]').attr('readonly','')"  # 设置为空
        cls.driver.execute_script(js)  # 执行设置为空
        element.send_keys(value)

    @classmethod
    def is_ElementExist(cls, how, element):
        """
        用来确认元素是否存在，如果存在返回true，否则返回false
        :param how: 用哪种方法，xpath，css，id，text
        :param element: 要寻找的元素
        :return: 返回True或者False
        """
        try:
            cls.driver.find_element(how, element)
            return True
        except:
            cls.logger.error(f'{element}元素未找到')
            return False

    @classmethod
    def select_random(cls, element):
        """
        随机选择下拉框中的某一项
        :param element: 下拉框元素对象
        :return: 无
        """
        from selenium.webdriver.support.select import Select
        import random
        random_index = random.randint(0, len(Select(element).options)-1)
        Select(element).select_by_index(random_index)

    @classmethod
    def select_by_text(cls, element, text):
        """
        根据下拉文本选择该项
        :param element: 下拉框元素对象
        :param text: 可见的文本
        :return:无
        """
        from selenium.webdriver.support.select import Select
        Select(element).select_by_visible_text(text)

    @classmethod
    def find_image(cls, target):
        """
        截取图片与当前页面截图对比返回目标图片的坐标
        :param target:要识别的图片路径
        :return: 目标图片（截取图片）的坐标
        """

        from PIL import ImageGrab
        import cv2

        image_path = '..\\image'
        screen_path = os.path.join(image_path, 'screen.png')  # 系统自动截取当前页面截图的保存地址
        ImageGrab.grab().save(screen_path)

        # 读取大图对象
        screen = cv2.imread(screen_path)
        # 读取小图对象
        template = cv2.imread(os.path.join(image_path, target))
        # 进行模板匹配，参数包括大图对象、小图对象和匹配算法
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        # 获取匹配结果
        min, max, min_loc, max_loc = cv2.minMaxLoc(result)

        similarity = FileUtil.get_ini_value('..\\conf\\base.ini', 'imagematch', 'similarity')
        if max < float(similarity):   # similarity 相似度
            return -1, -1

        x = max_loc[0] + int(template.shape[1] / 2)
        y = max_loc[1] + int(template.shape[0] / 2)
        return x, y

    @classmethod
    def click_image(cls, target):
        """
        单击一张图片
        :param target:
        :return:
        """
        x, y = cls.find_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'{target}图片未匹配')
            return
        cls.mouse.click(x, y)

    @classmethod
    def double_click_image(cls, target):
        x, y = cls.find_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'{target}图片未匹配')
            return
        cls.mouse.click(x, y, n=2)

    @classmethod
    def input_image(cls, target, msg):
        x, y = cls.find_image(target)
        if x == -1 and y == -1:
            cls.logger.error(f'{target}图片未匹配')
            return
        cls.keyboard.type_string(msg)

    @classmethod
    def select_image(cls, target, count):
        # 点击这个下拉框
        cls.click_image(target)
        # count次执行向下键
        for i in range(count):
            cls.keyboard.press_key(cls.keyboard.down_key)
        # 回车
        cls.keyboard.press_key(cls.keyboard.enter_key)

    @classmethod
    def screen_shot(cls, driver, path):
        """
        当前页面截图功能
        :param driver:
        :param path: 保存图片的路径
        :return: 无
        """
        driver.get_screenshot_as_file(path)


class Assert:

    @classmethod
    def assert_equal(cls, expect, actual):
        if expect == actual:
            test_result = 'test-pass'
        elif expect.find(actual) != -1:
            test_result = 'test-pass'
        else:
            test_result = 'test-fail'
            TestReport('shard_packing').write_result_db(test_result)
        print(test_result)


