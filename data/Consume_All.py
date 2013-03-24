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
from os import system
hosturl='http://my.njupt.edu.cn'
posturl='http://my.njupt.edu.cn/ccs/main.login.do'

def getdata(username,password,drcom_nu):

    # The following command is useless and will make remote serve tired.
    #h = urllib2.urlopen(hosturl)


	cj = cookielib.LWPCookieJar() 
	cookie_support = urllib2.HTTPCookieProcessor(cj) 
	opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler) 
	urllib2.install_opener(opener) 


	headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1', 'Referer' : 'http://my.njupt.edu.cn/ccs/main/loginIndex.do'}
	postData='email='+username+'&password='+password

	request = urllib2.Request(posturl, postData, headers) 
	response = urllib2.urlopen(request) 
	if response.read().find('用户名或密码错误')>-1:
		print('Login Failt')
		return False


	urllib2.urlopen( urllib2.Request('http://xykadmin.njupt.edu.cn/web/main.jsp'))
	final_data=[]
	for i in range(100):
		tmp_data=urllib2.urlopen( urllib2.Request('http://xykadmin.njupt.edu.cn/web/SystemListener?className=cn.com.system.query.DealQuery&methodName=getDealQuery&paramCount=6&param_2=2000-01-01&param_3=2020-01-1&param_4=0&param_5='+drcom_nu,'param_0='+str(i*1024)+'&param_1='+str(i*1024+1024),headers)).read()
		if len(eval(tmp_data)['results'])==0:
			break
		final_data.append(tmp_data)
	return final_data




f=open('./lastone','rw')
lastone=f.read().split('\n')[0]
f.close()
cx=sqlite3.connect("./data.db")
cu=cx.cursor()
raws=(cu.execute('select * from User'))
cx.commit()
flag=0
for line in raws:
	if line[2]:
		if int(line[0][1:3])>5:
			studentID=line[0]
			drcom_nu=line[2]
			password=line[3][12:18]
			student_name=line[1]
			print(studentID+'\t'+student_name)
			if studentID==lastone:
				flag=1
                continue
			if lastone=='':
				flag=1
			if flag==0:
				continue
			final_data=getdata(studentID,password,drcom_nu)
			if final_data==False:
				continue
			if len(final_data)>0:
				count=0
				for data in final_data:
					cx1=sqlite3.connect("./data_consume.db")
					cu1=cx1.cursor()
					dict_data=eval(data)
					print(dict_data['totalCount']+' : '+str(len(dict_data['results'])))
					for item in dict_data['results']:
						item['DISPOSETIME']=item['DISPOSETIME'].replace(' ','-')
						item['CONSUMETIME']=item['CONSUMETIME'].replace(' ','-')
						item['DISPOSETIME']=item['DISPOSETIME'].replace(':','-')
						item['CONSUMETIME']=item['CONSUMETIME'].replace(':','-')
                    
						cu1.execute('insert into Consume values(\''+studentID+'\',\''+item['CONSUMETYPE'].decode('gb2312')+'\',\''+item['CURRENTDBMONEY']+'\',\''+item['CARDNO']+'\',\''+item['FLOWCODE']+'\',\''+item['CONTYPE']+'\',\''+item['DISPOSETIME']+'\',\''+item['CONSUMETIME']+'\',\''+item['RN']+'\',\''+item['TRANSACTMONEY']+'\',\''+item['WINNAME'].decode('gb2312')+'\')')
						count=count+1
					cx1.commit()
				system('echo '+studentID+' >./lastone')
				print(count)
cx1.close()
cx.close()
print("All Done")

