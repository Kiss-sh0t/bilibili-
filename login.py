#coding=utf-8
import rsa
import json
import time
import urllib2,urllib,urlparse
import httplib
import binascii
import re


#open ajax page to get hash and public key
def gethash():
	url = "http://account.bilibili.com/login?act=getkey&_="+str(int(time.time()*1000))
	req = urllib2.Request(url)
	req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
	req.add_header('X-Requested-With','XMLHttpRequest')
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116')
	response = urllib2.urlopen(req)
	jsonText = response.read()
	token = json.loads(jsonText)
	return token


#encrypt passwd via rsa
def encryptpwd(passwd,token):
	password = token['hash'] + passwd
	pub_key = token['key']
	pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
	message = rsa.encrypt(str(password),pub_key)
	message = binascii.b2a_base64(message)
	return message


#post data to login
def postdata(uid,pwd):
	posturl = "https://account.bilibili.com/ajax/miniLogin/login"
	data = {'captcha':'','keep':'1','pwd':pwd,'userid':uid}
	req = urllib2.Request(posturl)
	data = urllib.urlencode(data)
	response = urllib2.urlopen(req,data)
	jsonText = response.read()
	text = json.loads(jsonText)
	if text['status']==True:
		print '[*] login success!'
	else:
		print '[-] login failed!'
		exit(1)
	return text['data']['crossDomain']

#get cookie
def getcookie(url):
	parse = urlparse.urlsplit(url)
	host = parse[1]
	path = parse[2]
	query = parse[3]
	#print parse
	#print host,path+query
	httpClient = httplib.HTTPConnection(host, 80, timeout=30)
	httpClient.request('GET', path+"?"+query)
	response = httpClient.getresponse()
	return response.getheaders()[2][1].split(';')

#change info of users
#not work yet
def changeinfo(cookie):
	posturl = "https://account.bilibili.com/site/UpdateSetting"
	data = {'birthday':'1994-02-02','city':'1','datingtype':'1','marital':'1','province':'2','sex':'男','sign':'this is anthor test sign','uname':'2333'}
	req = urllib2.Request(posturl)
	req.add_header('Cookie',cookie)
	data = urllib.urlencode(data)
	response = urllib2.urlopen(req,data)
	jsonText = response.read()
	text = json.loads(jsonText)
	print text

#process cookie
def proc_cookie(cookie):
	cookies = ''
	re_str = 'domain=.bilibili.cn'
	i = 0
	for strings in cookie:
		if re.search(re_str,strings):
			cookies = cookies + strings.replace(' domain=.bilibili.cn, ','') + ';'
			i += 1
			if i==3:
			#the only 3 thing we need is  DedeUserID,DedeUserID__ckMd5,SESSDATA
				break
	return cookies

#add attention
def addatention(fid,cookie):
	posturl = "http://space.bilibili.com/ajax/friend/AddAttention"
	data = {'mid':fid}
	req = urllib2.Request(posturl)
	req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.8.0')
	req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
	req.add_header('Accept','application/json, text/javascript, */*; q=0.01')
	req.add_header('Accept-Language', 'en-US,en;q=0.5')
	req.add_header('X-Requested-With','XMLHttpRequest')
	req.add_header('Referer','http://space.bilibili.com/'+str(fid)+'/')
	req.add_header('Cookie', cookie)
	data = urllib.urlencode(data)
	response = urllib2.urlopen(req,data)
	jsonText = response.read()
	text = json.loads(jsonText)
	if text['status']==True:
		print '[*] Add attention success!'
	else:
		print '[-] Add attention failed!'
		exit(1)

#main
def main():
	#config of username and password
	user = 'yourusername'
	passwd = 'yourpassword'
	token = gethash()
	enc = encryptpwd(passwd, token)
	domain = postdata(user,enc)
	cookie = getcookie(domain)
	cookies = proc_cookie(cookie)
	changeinfo(cookies)
	#addatention('100',cookies)

if __name__ == '__main__':
	main()
