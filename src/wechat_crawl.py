# coding: utf-8
import requests

#发现一个用浏览器获取公众号历史文章的方法
profile_root = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU3MjE2NzQ4Mg==&scene=124&#wechat_redirect"
profile_root1 = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI3MTgwNTE0Mg==&scene=124&#wechat_redirect"
#profile_root = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzIyOTM3ODAxNA==&scene=124&devicetype=android-23&version=26051633&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=i9hOYLZZef7lSHlRGS5XIh5VAGYkbdC%2BShjvuuTd4bsiNGKCnZFdfBrhsPczOQC7&wx_header=1"

sub_url = "http://mp.weixin.qq.com/s?__biz=MzIyOTM3ODAxNA==&mid=2247491183&idx=2&sn=d1bd8baf699213a947431a94f49b0ec3&chksm=e842ccdedf3545c8a73f771bc0770610ec040445467076d83cf609240e5b507af89dcaa38365&scene=38"

profile_content = ""

with open("profile.html") as f:
    for line in f:
        if "var msgList" in line:
            profile_content = line
print profile_content
i = profile_content.find('content_url')
j = profile_content.find('wechat_redirect')
while i >= 0:
    i = profile_content.find('content_url')
    j = profile_content.find('wechat_redirect')
    sub_url = profile_content[(i+len('content_url')): j]

    for rp in ['&quot;', 'amp;', '\\', '#']:
        sub_url = sub_url.replace(rp, '')
    sub_url = sub_url[1:]
    print sub_url
# s = requests.session()
# s.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11"}
# result = s.get(sub_url, timeout=500)
#
# print result.text

