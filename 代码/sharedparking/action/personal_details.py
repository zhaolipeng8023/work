#  个人信息模块
import time

from No_3.teacher_file.sharedparking.action.login import Login
from No_3.teacher_file.sharedparking.tools.lib_util import UiUtil


class PersonalDetails:

    def __init__(self, driver):
        # self.driver = driver
        self.driver = UiUtil.get_driver1()

    def click_mine(self):

        mine_button = UiUtil.find_element('change_mine_info', 'mine_button')
        UiUtil.click(mine_button)  # 点击主页【我的】按钮

    def click_change_personal_info(self, mine_info):
        iframe = UiUtil.find_element('change_mine_info', 'iframe')
        self.driver.switch_to.frame(iframe)  # 切换iframe
        time.sleep(2)
        info_button = UiUtil.find_element('change_mine_info', 'info_button')
        UiUtil.click(info_button)  # 点击【更改个人信息】按钮
        time.sleep(2)
        phone = UiUtil.find_element('change_mine_info', 'phone')
        UiUtil.input(phone, mine_info['phone'])  # 输入【用户电话】
        nickname = UiUtil.find_element('change_mine_info', 'nickname')
        UiUtil.input(nickname, mine_info['name'])  # 输入用户昵称
        sex = UiUtil.find_element('change_mine_info', 'sex')
        UiUtil.input(sex, mine_info['sex'])  # 输入用户性别 0=女 1=男
        submit_button = UiUtil.find_element('change_mine_info', 'submit_button')
        UiUtil.click(submit_button)

    def do_change_personal_info(self, mine_info):
        self.click_mine()
        self.click_change_personal_info(mine_info)




if __name__ == '__main__':
    driver = UiUtil.get_driver()
    login_data = {'username': '出租方1', 'password': '123', 'verifycode': '0000'}
    Login(driver).do_login(login_data)
    PersonalDetails(driver).click_mine()
    mine_info = {'phone': 18555666655, 'name': '张三', 'sex': 0}
    PersonalDetails(driver).do_change_personal_info(mine_info)