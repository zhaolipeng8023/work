import time

from sharedparking.action.login import Login
from sharedparking.tools.lib_util import UiUtil


class CustomerManage:
    def __init__(self, driver):
        self.driver = driver

    def input_cusphone(self, customerphone):
        cphone = self.driver.find_element_by_id('customerphone')
        UiUtil.input(cphone, customerphone)

    def input_cusname(self, cusname):
        cname = self.driver.find_element_by_id('customername')
        UiUtil.input(cname, cusname)

    def input_sex(self, childsex):
        sex = self.driver.find_element_by_id('childsex')
        UiUtil.select_by_text(sex, childsex)

    def input_data(self, childdate):
        data = self.driver.find_element_by_id('childdate')
        UiUtil.alter_seletor_input(data, 'id=childdate', childdate)

    def input_creditkids(self, creditkids):
        credit = self.driver.find_element_by_id('creditkids')
        UiUtil.input(credit, creditkids)

    def input_creditcloth(self, creditcloth):
        credcloth = self.driver.find_element_by_id('creditcloth')
        UiUtil.input(credcloth, creditcloth)

    def click_add_button(self):
        add_button = self.driver.find_element_by_css_selector('button.form-control:nth-child(1)')
        UiUtil.click(add_button)

    def click_query_button(self):
        query_button = self.driver.find_element_by_css_selector('button.form-control:nth-child(3)')
        UiUtil.click(query_button)

    def click_alter_button(self):
        alter_button = self.driver.find_element_by_id('editBtn')
        UiUtil.click(alter_button)

    def do_add_customer(self, login_data):
        self.input_cusphone(login_data['phone'])
        self.input_sex(login_data['childsex'])




if __name__ == '__main__':
    driver = UiUtil.get_driver()
    login_data = {'username': 'admin', 'password': 'admin', 'verifycode': '0000'}
    Login(driver).do_login(login_data)
    data = {'phone':11111111111,'childsex':'男','childdate':2020-10-21}
    driver = UiUtil.get_driver()

    CustomerManage(driver).do_add_customer(data)