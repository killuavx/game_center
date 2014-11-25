# -*- coding: utf-8 -*-
import random
from toolkit.CCPSDK.CCPRestSDK import REST

def randcode(codelen=6):
    mask_str = "%0" + str(codelen) + "d"
    return mask_str % random.randint(0, int(codelen * "9"))

#主帐号
CLOOPEN_ACCOUNT_SID = '8a48b55149d5792d0149e063bc3705e4'

#主帐号Token
CLOOPEN_ACCOUNT_TOKEN = 'a4cab57a70374530a1c8f979f34dfb7f'

#应用Id
#CLOOPEN_APPID = '8a48b55149d5792d0149e06c3ef905f1'
CLOOPEN_APPID = '8a48b55149d5792d0149e0640dec05e8'

#请求地址，格式如下，不需要写http://
CLOOPEN_SERVER_IP = 'sandboxapp.cloopen.com'
#CLOOPEN_SERVER_IP = 'app.cloopen.com'

#请求端口
CLOOPEN_SERVER_PORT = '8883'

#REST版本号
CLOOPEN_SOFT_VERSION = '2013-12-26'

cloopen_api = REST(CLOOPEN_SERVER_IP, CLOOPEN_SERVER_PORT, CLOOPEN_SOFT_VERSION)
cloopen_api.setAccount(CLOOPEN_ACCOUNT_SID, CLOOPEN_ACCOUNT_TOKEN)
cloopen_api.setAppId(CLOOPEN_APPID)


# 注册验证码模板 {1}验证码 {2}有效期
#SMS_TEMPID_SIGNUP = 7867
SMS_TEMPID_SIGNUP = 1

# 发送模板短信
# @param $to 手机号码
# @param $datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id
def send_sms(to, datas, tempId=1):
    res = cloopen_api.sendTemplateSMS2(to, datas, str(tempId))
    if res.get('statusCode') == '000000':
        return True, res
    return False, res


from toolkit.cache_tagging_mixin import default_cache


class PhoneAuth(object):

    duration = 60

    MASK_PHONE_AUTH_CODE = 'phone_code_%s'

    cache = default_cache

    def __init__(self, phone, duration=60):
        self.phone = phone
        self.duration = duration

    @property
    def code_key(self):
        return self.MASK_PHONE_AUTH_CODE % self.phone

    def check_code(self, code):
        print("check phone code: ", self.code_key, self.cache.get(self.code_key))
        return self.cache.get(self.code_key) == code

    def make_code(self, ex=60, overwrite_exists=True):
        code = self.cache.get(self.code_key)
        print(self.code_key, code, ex)
        if not overwrite_exists and code:
            return code
        code = randcode()
        print(self.code_key, code, ex)
        self.cache.set(self.code_key, code, ex)
        return code

