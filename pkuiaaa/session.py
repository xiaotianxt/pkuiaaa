import random
from functools import wraps
from requests import Session

OAUTHLOGIN = "https://iaaa.pku.edu.cn/iaaa/oauthlogin.do"


class IAAASession(Session):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
        })
        self.real_post = super().post
        self.real_get = super().get

    def __del__(self):
        self.close()

    def get(self, url, *args, **kwargs):
        """重写 Session.get 方法，验证状态码"""
        res = super().get(url, *args, **kwargs)
        res.raise_for_status()
        return res

    def post(self, url, *args, **kwargs):
        """重写 Session.post 方法，验证状态码"""
        res = super().post(url, *args, **kwargs)
        res.raise_for_status()
        return res

    def login(self, username: str, password: str, appid: str, redirect: str) -> bool:
        """登录 IAAA 并重定向"""

        # IAAA 登录
        json = self.post(OAUTHLOGIN, data={
            "userName": username,
            "appid": appid,
            "password": password,
            "redirUrl": redirect,
            "randCode": "",
            "smsCode": "",
            "optCode": "",
        }).json()
        assert json['success'], json

        # 重定向
        return self.get(redirect, params={
            '_rand': random.random(),
            'token': json['token']
        })


@wraps('check_login')
def login_check(func):
    """检查 IAAA 令牌是否过期"""

    def wrapper(self, *args, **kwargs):
        # TODO: should check login status from iaaa, WIP
        return func(self, *args, **kwargs)
    return wrapper


def login(username: str, password: str, appid: str, callback: str) -> IAAASession:
    """登录门户，返回 IAAASession 对象"""
    session = IAAASession()
    session.login(username, password, appid, callback)
    return session
