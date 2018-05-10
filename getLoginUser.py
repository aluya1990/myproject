# _*_ coding:utf-8 _*_
import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
# from PIL import Image
import webbrowser
import unittest
import json
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# 使用登录cookie信息
session = requests.session()
# 获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://192.168.10.90:8887/csdc-permissions-web//getVerifyCode.do?tock=' + t
    print(captcha_url)
    response = session.get(captcha_url)
    with open('getVerifyCode3.gif', 'wb') as f:
        f.write(response.content)
        # f.close()
    try:
        webbrowser.open('getVerifyCode3.gif')
        # im = Image.open('getVerifyCode3.gif')
        # im.show()
        # im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))

    captcha = raw_input("please input the captcha\n>")
    return captcha


def login(secret, account):
    post_url = 'http://192.168.10.90:8887/csdc-permissions-web//login.do'
    firstResp = session.post(post_url)
    requests.utils.add_dict_to_cookiejar(session.cookies, firstResp.cookies.get_dict())
    postdata = {
        'username': account,
        'password': secret,
        'jcaptchaCode': get_captcha()
    }
    response = session.post(post_url, data=postdata)
    print(response.text)

class testGetLoginUser(unittest.TestCase):
    def testgetLoginUser(self):
        login("csdc1111", "xulu")
        self.get_url = 'http://192.168.10.90:8887/csdc-permissions-web/getLoginUser.do?_=1521775230948'
        response = session.get(self.get_url)
        print (response.text)
        result = response.json()
        data = result['data']
        get_result = data['id']
        print (get_result)
        # 断言
        self.assertEqual(12, get_result)

if __name__ == '__main__':
    unittest.main()
