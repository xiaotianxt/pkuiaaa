from unittest import TestCase
from os import getenv

import pkuiaaa

studentid = getenv('STUDENTID')
password = getenv('PASSWORD')

if not studentid or not password:
    raise Exception(
        'Please set STUDENTID and PASSWORD in environment variables.')


class TestPKUIAAA(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_IAAASession_login(self):
        session = pkuiaaa.IAAASession()
        res = session.login(studentid, password,
                            "https://portal.pku.edu.cn/portal2017/ssoLogin.do")

        self.assertEqual(res.status_code, 200)
