from sharedparking.tools.util import DBUtil
from sharedparking.tools.util import LogUtil
from sharedparking.tools.util import TimeUtil

import os


class TestReport:

    def __init__(self, app_name):
        self.app_name = app_name
        self.logger = LogUtil.get_logger('test_report')

    def write_result_db(self, result_info):

        now = TimeUtil.get_standard_format_time()
        sql = f'insert into {self.app_name}(version, module, case_type, ' \
              f'case_id, uri, request_method, case_desc, test_result, finish_time, error_msg, error_screenshot) ' \
              f'values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
              % (result_info['version'], result_info['module'], result_info['case_type'],
                 result_info['case_id'], result_info['uri'], result_info['request_method'],
                 result_info['case_desc'], result_info['test_result'], f'{now}',
                 result_info['error_msg'], result_info['error_screenshot'])
        # print(sql)
        DBUtil('db_report').update_db(sql)

    def generate_html_report(self, version):

        # 根据不同的版本读取该版本的测试结果数据
        sql_all = f'select * from {self.app_name} where version="{version}"'

        all_result = DBUtil('db_report').query_all(sql_all)

        if len(all_result) == 0:
            self.logger.info('没有该版本的测试结果')
            return

        # 计算测试执行成功的数量
        sql_success = f'select count(*) from {self.app_name} where version="{version}" and test_result="test-pass"'
        sucess_result = DBUtil('db_report').query_one(sql_success)[0]
        # 计算测试执行失败的数据
        sql_fail = f'select count(*) from {self.app_name} where version="{version}" and test_result="test-fail"'
        fail_result = DBUtil('db_report').query_one(sql_fail)[0]
        # 计算测试执行错误的数据
        sql_error = f'select count(*) from {self.app_name} where version="{version}" and test_result="test-error"'
        error_result = DBUtil('db_report').query_one(sql_error)[0]

        # 获取最后一条用例执行的时间
        lasttime_sql = 'select finish_time from test_result order by finish_time desc limit 0,1'
        lasttime = str(DBUtil('db_report').query_one(lasttime_sql)[0])

        # 获取日期
        test_data = lasttime.split(' ')[0]
        #
        # # 替换html页面中指定位置的数据
        # with open('template.html', encoding='utf8') as file:
        #     contents = file.read()

        result_str = ''
        for result in all_result:
            if result[6] == 'test-pass':
                color = 'green'
            elif result[6] == 'test-fail':
                color = 'red'
            else:
                color = 'yellow'
            if result[9] == '无':
                screenshot = '无'
            else:
                screenshot = f'<a href="{result[9]}">查看截图</a>'

            # 表格中添加内容
            result_str += f'<tr height="40">' \
                          f'<td width="3%">{result[0]}</td>' \
                          f'<td width="9%">{result[2]}</td>' \
                          f'<td width="9%">{result[3]}</td>' \
                          f'<td width="10%">{result[4]}</td>' \
                          f'<td width="16%">{result[10]}</td>' \
                          f'<td width="4%">{result[11]}</td>' \
                          f'<td width="20%">{result[5]}</td>' \
                          f'<td width="7%" bgcolor="{color}">{result[6]}</td>' \
                          f'<td width="8%">{result[7]}</td>' \
                          f'<td width="8%">{result[8]}</td>' \
                          f'<td width="6%">{screenshot}</td>' \
                          f'</tr>\r\n'

            # 替换模板上特定位置的字符串
            with open('..\\conf\\template.html', encoding='utf-8') as file:
                contents = file.read()

            contents = contents.replace('$test-date', test_data)
            contents = contents.replace('$test-version', version)
            contents = contents.replace('$pass-count', str(sucess_result))
            contents = contents.replace('$fail-count', str(fail_result))
            contents = contents.replace('$error-count', str(error_result))
            contents = contents.replace('$last-time', lasttime)

            contents = contents.replace('$test-result', result_str)
        # 将内容写入新的测试报告中
        if not os.path.exists(f'..\\report\\{version}'):
            os.mkdir(f'..\\report\\{version}')

        report_path = f'..\\report\\{version}\\{self.app_name}{version}版本测试报告.html'
        with open(report_path, 'w', encoding='utf-8') as file:
            file.write(contents)


if __name__ == '__main__':

    result_info = {'version':'v2.0', 'module':'login', 'case_type':'ui','uri':'dfghjkl','request_method':'POST',
                   'case_id':'login-02','case_desc':'1.输入账号；2.输入密码；3.输入验证码；4.点击登录按钮',
                   'test_result':'test-pass', 'error_msg':'无', 'error_screenshot':'无'}

    TestReport('test_result').write_result_db(result_info)

    TestReport('test_result').generate_html_report('v2.0')