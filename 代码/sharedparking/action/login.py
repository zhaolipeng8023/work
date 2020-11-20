import time

from sharedparking.tools.lib_util import UiUtil


class Login:
    def __init__(self, driver):

        self.driver = driver

    def input_username(self, username):
        uname = UiUtil.find_element('login', 'uname')
        UiUtil.input(uname, username)

    def input_password(self, password):
        pws = UiUtil.find_element('login', 'upass')
        UiUtil.input(pws, password)

    def input_verifycode(self, verifycode):
        vfcode = UiUtil.find_element('login', 'vfcode')
        UiUtil.input(vfcode, verifycode)

    def click_login_button(self):
        login_button = UiUtil.find_element('login', 'login_button')
        UiUtil.click(login_button)

    def click_loginout_button(self):
        logout = UiUtil.find_element('login', 'logout_uname')
        UiUtil.click(logout)
        logout_button = UiUtil.find_element('login', 'logout_button')
        UiUtil.click(logout_button)

    def do_login(self, login_data):
        self.input_username(login_data['username'])
        self.input_password(login_data['password'])
        self.input_verifycode(login_data['verifycode'])
        self.click_login_button()

    def do_loginout(self, login_data):
        self.do_login(login_data)
        time.sleep(5)
        self.click_loginout_button()


if __name__ == '__main__':
    driver = UiUtil.get_driver()
    login_data = {'username':'抢租客0', 'password':'123', 'verifycode':'0000'}
    Login(driver).do_loginout(login_data)



