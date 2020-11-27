from selenium.webdriver.support.select import Select

from No_3.teacher_file.sharedparking.action.login import Login
from No_3.teacher_file.sharedparking.tools.lib_util import UiUtil

class QuaryOrder:
    def __init__(self, driver):

        self.driver = driver

    def order_history(self):  # 进入历史订单界面
        history_button = UiUtil.find_element('query_order', 'history_button')
        UiUtil.click(history_button)

    def query_condition(self, condition):  # 选择查询条件，点击【搜索】
        # index：第一个查询条件的下拉框内容下标， second：第二个下拉框条件的时间或者文本
        iframe = UiUtil.find_element('query_order', 'iframe')
        self.driver.switch_to.frame(iframe)
        query_element = UiUtil.find_element('query_order', 'query_element')
        Select(query_element).select_by_visible_text(condition[0])   # 第一个查询条件框，用下拉框内容下标取值
        if '时间' in condition[0] :  # 选择第一种查询条件【按时间查询】
            query_time_element = self.driver.find_element_by_id('time')
            UiUtil.input_select('time', query_time_element, condition[1])  # 第二个下拉框输入日期
        else:  # 选择第二种查询条件【按状态查询】
            query_status_element = UiUtil.find_element('query_order', 'query_status_element')
            Select(query_status_element).select_by_visible_text(condition[1])  # 第二个下拉框选择文本
        UiUtil.find_element('query_order', 'query_button').click()  # 点击搜索按钮

    def do_query_condition(self, condition):
        self.order_history()
        self.query_condition(condition)



if __name__ == '__main__':
    driver = UiUtil.get_driver()
    login_data = {'username': '出租方1', 'password': '123', 'verifycode': '0000'}
    Login(driver).do_login(login_data)
    condition = ['按状态查询', '进行中']
    QuaryOrder(driver).do_query_condition(condition)

