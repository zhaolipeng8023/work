from sharedparking.action.login import Login
from sharedparking.tools.lib_util import UiUtil


class StoreQuery:  # 库存查询

    def __init__(self, driver):
        self.driver = driver

    def click_query_button(self):
        button = UiUtil.find_element('store_query', 'query_button')
        UiUtil.click(button)

    def click_condition_button(self):
        button = UiUtil.find_element('store_query', 'condition_query')
        UiUtil.click(button)

    def click_notStored_button(self):
        button = UiUtil.find_element('store_query', 'notStored_query')
        UiUtil.click(button)

    def click_zeroStored_button(self):
        button = UiUtil.find_element('store_query', 'zeroStored_query')
        UiUtil.click(button)

    def input_goodsSize(self, goodsserial):
        gsize = UiUtil.find_element('store_query', 'gserial')
        UiUtil.input(gsize, goodsserial)

    def input_goodsname(self, goodsname):
        gname = UiUtil.find_element('store_query', 'gname')
        UiUtil.input(gname, goodsname)

    def input_barcode(self, barcode):
        code = UiUtil.find_element('store_query', 'barcode')
        UiUtil.input(code, barcode)

    def input_goodstype(self, goodstype):
        type = UiUtil.find_element('store_query', 'goodstype')
        UiUtil.select_by_text(type, goodstype)

    def input_earlytime(self, earlystoretime):
        eartime = UiUtil.find_element('store_query', 'earlytime')
        UiUtil.alter_seletor_input_earlystoretime(eartime, earlystoretime)

    def input_endtime(self, laststoretime):
        lasttime = UiUtil.find_element('store_query', 'lasttime')
        UiUtil.alter_seletor_input_laststoretime(lasttime, laststoretime)

    def do_condition_query(self, query_data):
        self.click_query_button()
        self.input_goodsSize(query_data['goodssize'])
        self.input_goodsname(query_data['goodsname'])
        self.input_barcode(query_data['barcode'])
        self.input_goodstype(query_data['goodstype'])
        # UiUtil.alter_seletor_input(('ID', 'earlystoretime'), '[id=earlystoretime]', query_data['earlytime'])
        # UiUtil.alter_seletor_input(('ID', 'earlystoretime'), '[id=laststoretime]', query_data['earlytime'])
        self.input_earlytime(query_data['earlytime'])
        self.input_endtime(query_data['endtime'])
        self.click_condition_button()

    def do_zeroStored_query(self):
        self.click_query_button()
        self.click_zeroStored_button()

    def do_notStored_query(self):
        self.click_query_button()
        self.click_notStored_button()


if __name__ == '__main__':
    driver = UiUtil.get_driver()
    login_data = {'username': 'admin', 'password': 'admin', 'verifycode': '0000'}
    Login(driver).do_login(login_data)
    query_data ={'goodssize':'M3Q1498B','goodsname':'米乐果后开连衣裙','barcode':'11111111','goodstype':'衣服','earlytime':'2018-05-08','endtime':'2020-02-13'}
    StoreQuery(driver).do_condition_query(query_data)


