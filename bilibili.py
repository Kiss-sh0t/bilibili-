#coding=utf-8
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
#print captcha.cookies
captcha = session.get('http://passport.bilibili.com/captcha')
sessionCookies = captcha.cookies

f = open('pic.jpeg','wb')
f.write(captcha.content)
f.close()
im=Image.open('pic.jpeg')
im.show()

jsonText = session.get('http://passport.bilibili.com/login?act=getkey', cookies=sessionCookies)
token = json.loads(jsonText.content)
#print jsonText.content

username = 'xxx'
passwd = 'xxx'
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
#print jsonText.content

#获取av信息
av = 4757328
cont = session.get('http://www.bilibili.com/video/av'+str(av))
m = re.search('cid=\d*',cont.content)
cid = m.group()[4:]
t = time.strftime('%Y-%m-%d %H:%M:%S')

#aid为视频的av号
#弹幕内容，当前时间和视频时间，视频时间以秒记，比如在1分20，时间就是80.00
#字号有两种，一种18，一种25
<<<<<<< HEAD
def postdanmu(content, t, pt, fsize=25, color=0xffffff, mod=1): 
    postdata = {
        'mode': mod, #5为顶端弹幕，1为滚动字幕，4为低端渐隐
        'color': str(int(color)), #颜色用16进制
=======
def postdanmu(content, t, pt, fsize=25): 
    postdata = {
        'mode':1, #0为顶端弹幕，1为滚动字幕，2为低端渐隐，3为逆向滚动
        'color':'16777215', #还没测试其他颜色，先用白的试试吧
>>>>>>> origin/master
        'message': content, #弹幕内容
        'pool':'0', #这个字段什么鬼
        'playTime': pt, #在视频中的时间轴，单位为秒，小数点后两位
        'cid': cid, 
        'fontsize': fsize, #字体大小，两种规格，这个是那个小的
<<<<<<< HEAD
        'rnd': 1485737224, #算了，随便生成一个好了_(:з」∠)_。投不同视频请使用不同rnd值
=======
        'rnd': 1485739224, #好像是个时间参数，蛋疼啊，到底怎么来的，算了，随便生成一个好了_(:з」∠)_
>>>>>>> origin/master
        'data': str(t) 
    }
    return session.post('http://interface.bilibili.com/dmpost?cid='+str(cid)+'&aid='+str(av)+'&pid=1', postdata)

<<<<<<< HEAD
#测试
test = postdanmu('第几？', t, 30.08, mod=5, color=0x33ff00)#顶端，绿色
=======
#测试，可以有中文
test = postdanmu('maybe the first one?', t, 80.08)

#如果不是-1，发送成功
print test.content
>>>>>>> origin/master
