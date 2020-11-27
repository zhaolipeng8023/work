
from No_3.teacher_file.sharedparking.action.login import Login
from No_3.teacher_file.sharedparking.tools.lib_util import UiUtil


class AddCarport:

    def __init__(self, driver):
        self.driver = driver

    def click_add_carport(self):  # 点击添加车位
        iframe = UiUtil.find_element('add_carport', 'iframe')  # 这里需要切换一次iframe
        self.driver.switch_to.frame(iframe)
        add_carport = UiUtil.find_element('add_carport', 'add')
        UiUtil.click(add_carport)

    def input_car_id(self, value):  # 输入车位号
        car_id = UiUtil.find_element('add_carport', 'car_id')
        UiUtil.input(car_id, value)

    def input_location_id(self, value):  # 输入位置id
        location_id = UiUtil.find_element('add_carport', 'location_id')
        UiUtil.input(location_id, value)

    def input_location(self, value):  # 输入详细地址
        location = UiUtil.find_element('add_carport', 'location')
        UiUtil.input(location, value)

    def click_add(self):  #  输完内容之后点击增加按钮
        add_button = UiUtil.find_element('add_carport', 'add_button')
        UiUtil.click(add_button)

    def do_add_carport(self, carport_data):  # 执行动作
        self.click_add_carport()
        self.input_car_id(carport_data['car_id'])
        self.input_location_id(carport_data['location_id'])
        self.input_location(carport_data['location'])
        self.click_add()


if __name__ == '__main__':
    driver = UiUtil.get_driver()
    login_data = {'username': '出租方1', 'password': '123', 'verifycode': '0000'}
    parmars = {'car_id': 27, 'location_id': 4009, 'location': '未央路凤城二路口'}
    Login(driver).do_login(login_data)
    AddCarport(driver).do_add_carport(parmars)