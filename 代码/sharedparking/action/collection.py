import os

from selenium import webdriver
from sharedparking.tools.util import DBUtil
from sharedparking.tools.util import LogUtil
from pykeyboard import PyKeyboard
from pymouse import PyMouse


class Collection:
    keyboard = PyKeyboard()
    mouse = PyMouse()

    logger = LogUtil.get_logger(os.path.join(os.getcwd(), 'collection'))
    driver = None

    @classmethod
    def open_browser(cls, browser):
        """
        打开浏览器
        :param browser: 浏览器名称
        :return: 返回driver对象
        """
        if hasattr(webdriver, browser):
            cls.driver = getattr(webdriver, browser)()
        else:
            cls.logger.error('浏览器名称不正确')
            cls.driver = webdriver.Firefox()

        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()
        return cls.driver

    @classmethod
    def find_element(cls, attr):
        """
        查找页面元素
        :param attr: id=username,类似这种
        :return: 返回element
        """
        at = attr.split('=')
        element = None
        try:
            if at[0] == 'id':
                element = cls.driver.find_element_by_id(at[1])
            elif at[0] == 'link_text':
                element = cls.driver.find_element_by_link_text(at[1])
            elif at[0] == 'css_selector':
                element = cls.driver.find_element_by_css_selector(at[1])
            elif at[0] == 'xpath':
                element = cls.driver.find_element_by_xpath(at[1])
        except BaseException:
            cls.logger.error(f'没有找到{attr}元素')
        finally:
            return element

    @classmethod
    def get_page(cls, url):
        """
        获取页面
        :param url: 主页的url
        :return: 无
        """
        cls.driver.get(url)

    @classmethod
    def click(cls, attr):
        """
        点击
        :param attr:
        :return:
        """
        element = cls.find_element(attr)
        if element is not None:
            element.click()
        return element

    @classmethod
    def input(cls, attr, value):
        """
        输入
        :param attr:
        :param value:
        :return:
        """
        element = cls.click(attr)
        element.clear()
        element.send_keys(value)

    @classmethod
    def select(cls, attr, value):
        """
        选择文本值
        :param attr:
        :param value:
        :return:
        """
        element = cls.click(attr)
        from selenium.webdriver.support.select import Select
        Select(element).select_by_visible_text(value)

    @classmethod
    def get_page_text(cls, attr):
        """
        获取元素文本值
        :param attr:
        :return:
        """
        element = cls.find_element(attr)
        return element.text

    @classmethod
    def aleert_button(cls, option):
        """
        allert弹窗
        :param option: accept 或者 dismiss
        :return:
        """
        if option == 'accept':
            cls.driver.switch_to.alert.accept()
        elif option == 'dismiss':
            cls.driver.switch_to.alert.dismiss()

    @classmethod
    def assert_exist_element(cls, attr):
        """
        判断元素存在
        :param attr:
        :return: Ture 或 False
        """
        element = cls.find_element(attr)
        if element is not None:
            return True
        else:
            return False

    @classmethod
    def query_one(cls, option, sql):
        """
        查询一条记录
        :param option: 节点
        :param sql: sql语句  select * from table_name
        :return:
        """
        return DBUtil(option).query_one(sql)

    @classmethod
    def query_all(cls, option, sql):
        """
        查询多条记录
        :param option: 节点
        :param sql: sql语句  select * from table_name
        :return:
        """
        return DBUtil(option).query_all(sql)

    @classmethod
    def query_write_file(cls, option, sql):
        """
        将查询结果写入文件
        :param option:
        :param sql:
        :return: file文件对象
        """
        result = DBUtil(option).query_one(sql)
        with open("..\\kw_ui_script\\sql_result", 'w', encoding='utf8') as file:
            file.write(str(result[0]))
            return file

    @classmethod
    def assert_two_result(cls, option, sql):
        """
        断言两次查询结果
        :param option: 读取配置文件节点
        :param sql: 查询语句
        :return:
        """
        second_result = str(DBUtil(option).query_one(sql)[0])
        with open('..\\kw_ui_script\\sql_result', encoding='utf8') as file:
            once_result = file.read()
        if second_result != once_result:
            print(second_result, once_result)
            print('测试通过')
            return True
        else:
            print('测试失败')
            return False

    @classmethod
    def assert_equal(cls, attr, expect):
        actual = cls.get_page_text(attr)
        if expect == actual:
            return True
        else:
            return False

    @classmethod
    def sleep(cls, ctime):
        """
        休眠
        :param ctime: 整数
        :return:
        """
        import time
        time.sleep(int(ctime))

    @classmethod
    def close(cls):
        """
        关闭
        :return:
        """
        cls.driver.quit()

    @classmethod
    def do_enter(cls):
        """
        enter确定
        :return:
        """
        cls.keyboard.press_key(cls.keyboard.enter_key)


if __name__ == '__main__':
    c = Collection
    # c.open_browser('Firefox')
    # c.get_page('http://172.16.13.120:8080/WoniuSales1.4/')
    # c.input('id=username', 'admin')
    # c.input('id=password', 'admin')
    # c.input('id=verifycode', '0000')
    # c.click('xpath=/html/body/div[4]/div/form/div[6]/button')
    # c.sleep(2)
    # c.assert_exist_element('link_text=注销')
    # c.close()
    # c.query_write_file('db_info', "select count(*) FROM sellsum;")
    print(c.assert_two_result('db_info', "select count(*) FROM sellsum;"))

