import unittest
import os

import pkuiaaa

studentid = os.getenv('PKU_USERNAME')
password = os.getenv('PKU_PASSWORD')

if not studentid or not password:
    raise Exception(
        'Please set `PKU_USERNAME` and `PKU_PASSWORD` in environment variables.')


class TestPKUIAAA(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.appid = 'portal2017'
        self.redirUrl = 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'

    def test_IAAASession_login(self):
        session = pkuiaaa.IAAASession()
        res = session.login(studentid, password, self.appid, self.redirUrl)

        self.assertEqual(res.status_code, 200)

    def test_login_func(self):
        session = pkuiaaa.login(studentid, password, self.appid, self.redirUrl)
        self.assertIsInstance(session, pkuiaaa.IAAASession)

    def test_login_getenv(self):
        os.environ['PKU_USERNAME'] = studentid
        os.environ['PKU_PASSWORD'] = password
        session = pkuiaaa.login_with_env(self.appid, self.redirUrl)
        self.assertIsInstance(session, pkuiaaa.IAAASession)
