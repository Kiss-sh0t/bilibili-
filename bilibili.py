import requests
import Image
import rsa
import binascii
import json
import re
import time



session = requests.Session()

captcha = session.get('http://www.bilibili.com')
c = captcha.cookies
captcha = session.get('http://passport.bilibili.com/login', cookies=c)
print captcha.cookies
captcha = session.get('http://passport.bilibili.com/captcha')
sessionCookies = captcha.cookies

f = open('pic.jpeg','wb')
f.write(captcha.content)
f.close()
im=Image.open('pic.jpeg')
im.show()

jsonText = session.get('http://passport.bilibili.com/login?act=getkey', cookies=sessionCookies)
token = json.loads(jsonText.content)
print jsonText.content
username = 'user'
passwd = 'pass'
vdcode = raw_input('Enter captcha > ')
def encryptpwd(passwd,token):
    password = token['hash'] + passwd
    pub_key = token['key']
    pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
    message = rsa.encrypt(str(password),pub_key)
    message = binascii.b2a_base64(message)
    return message
encrypass = encryptpwd(passwd, token)

postdata = {
    'act':'login',
    'gourl':'',
    'keeptime':'2592000',
    'userid':username,
    'pwd':encrypass,
    'vdcode':vdcode
    }
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
jsonText = session.post('http://passport.bilibili.com/login/dologin', postdata, cookies=sessionCookies)

cont = session.get('http://space.bilibili.com')
print cont.content