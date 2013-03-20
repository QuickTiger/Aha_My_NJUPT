#encoding=utf-8
import HTMLParser 
import urlparse 
import urllib 
import urllib2 
import cookielib 
import string 
import re
import time
import sqlite3
#set the server
hosturl='http://my.njupt.edu.cn'
posturl='http://my.njupt.edu.cn/ccs/main.login.do'
#set the Accounts
StudentID=''
password=''
drcom=''

def getdata(username,password,drcom_nu):
	cj = cookielib.LWPCookieJar() 
	h = urllib2.urlopen(hosturl) 
	cookie_support = urllib2.HTTPCookieProcessor(cj) 
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler) 
	urllib2.install_opener(opener) 
	
	headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1', 'Referer' : 'http://my.njupt.edu.cn/ccs/main/loginIndex.do'}
	postData='email='+username+'&password='+password
	request = urllib2.Request(posturl, postData, headers) 
	response = urllib2.urlopen(request) 
	if response.read().find('用户名或密码错误')>-1:
		print('sailimnu')
		return False
	urllib2.urlopen( urllib2.Request('http://xykadmin.njupt.edu.cn/web/main.jsp'))
	final_data=[]
	for i in range(100):
		tmp_data=urllib2.urlopen( urllib2.Request('http://xykadmin.njupt.edu.cn/web/SystemListener?className=cn.com.system.query.DealQuery&methodName=getDealQuery&paramCount=6&param_2=2000-01-01&param_3=2020-03-14&param_4=0&param_5='+drcom_nu,'param_0='+str(i*1024)+'&param_1='+str(i*1024+1024),headers)).read()
		if len(eval(tmp_data)['results'])==0:
			break
		final_data.append(tmp_data)
	return final_data


final_data=getdata(StudentID,password,drcom)
for data in final_data:
	if data:
		dict_data=eval(data)
		for item in dict_data['results']:
			print(StudentID+'\t'+item['CONSUMETYPE']+'\t'+item['TRANSACTMONEY']+'\t'+item['FLOWCODE']+'\t'+item['CONSUMETIME']+'\t'+item['WINNAME'])
	

