#coding=gb2312
import re
import time



holidaylist=[]        
semesterFoodRatelist=[]
allList=[]
daydict={}
mondict={}
daylist=[]
monlist=[]
placedict={}
placelist=[]

def holiday(daylist,holidaylist):

    for i in range(len(daylist)-1):
        if time.strptime(daylist[i+1].day,'%Y%m%d').tm_yday-time.strptime(daylist[i].day,'%Y%m%d').tm_yday in range(15,100): 
            print "Holiday : " + daylist[i].day+'-'+daylist[i+1].day
            holidaylist.append((daylist[i].day,daylist[i+1].day))
    print "MAx semester is :" +str(len(holidaylist))
    
def maxConsume(allList):
    
    print sorted([(time.strftime('%Y%m%d %H:%M:%S',x.datetime),x.money,x.place) for x in allList],key=lambda x:x[1],reverse=True)[:5]
    
def maxDayConsume(daylist):
    
    print sorted([(x.day,x.money) for x in daylist ],key=lambda x:x[1],reverse=True)[:5]
    
def foodRate(allList):
    for item in ['Breakfast','Lunch','Dinner','Snack']:
        print("Avevary Rate of "+ item +" is :"+ str(len([x for x in allList if x.type==item])*1.0/len(daylist)))
        for i in range(7):
            print("in weekday :"+str(i+1))
            print(len([x for x in allList if x.type==item and x.datetime.tm_wday ==i])*1.0/len([x for x in daylist if time.strptime(x.day,'%Y%m%d').tm_wday ==i]))

def foodRateOfSemester(allList,holidaylist):
    
    for semester in range(len(holidaylist)+1):
        semesterFoodRatelist.append([])
        tmp_typeindex=0
        for item in ['Breakfast','Lunch','Dinner','Snack']:
            semesterFoodRatelist[semester].append([])
            semesterFoodRatelist[semester][tmp_typeindex]=[]
            semesterFoodRatelist[semester][tmp_typeindex].append(len([x for x in allList if x.type==item and x.semester==semester])*1.0/len([x for x in daylist if x.semester==semester]))
           # print("Averary Rate of "+ item +" is :"+ str(len([x for x in allList if x.type==item])*1.0/len(daylist)))
            print "++++++++++++++++++++++++++++++++++++++++"
            print len([x for x in allList if x.type==item and x.semester==semester])
            print len([x for x in daylist if x.semester==semester])

            for i in range(7):
                print str(semester)+"::"+item
                print str(len([x for x in allList if x.datetime.tm_wday ==i and x.semester==semester]))+":"+str(len([x for x in daylist if x.semester==semester and time.strptime(x.day,'%Y%m%d').tm_wday ==i]))
                #print len([x for x in allList if x.type==item and x.datetime.tm_wday ==i and x.semester==semester])
                semesterFoodRatelist[semester][tmp_typeindex].append(len([x for x in allList if x.type==item and x.datetime.tm_wday ==i and x.semester==semester])*1.0/len([x for x in daylist if x.semester==semester and time.strptime(x.day,'%Y%m%d').tm_wday ==i]))
            tmp_typeindex+=1
def findType(allList):
    for item in allList:
        if item.place.find("超市")!=-1:
            item.type= 'Market'
        elif item.datetime.tm_hour in range(5,10):
            item.type='Breakfast'
        elif item.datetime.tm_hour in range(11,14):
            item.type='Lunch'
        elif item.datetime.tm_hour in range(16,20):
            item.type='Dinner'
        elif item.datetime.tm_hour >20:
            item.type='Snack'

def findSemester(allList,holidaylist):
    
    for item in allList:
        for i in range(1,len(holidaylist)):
            if time.strftime('%Y%m%d',item.datetime)<=holidaylist[i][0] and time.strftime('%Y%m%d',item.datetime)>=holidaylist[i-1][0] :
                item.semester=i
                #print time.strftime('%Y%m%d',item.datetime)+":"+holidaylist[i][0]
                #print item.semester
                #print i
            if time.strftime('%Y%m%d',item.datetime)<=holidaylist[0][0]:
                item.semester=0
            if time.strftime('%Y%m%d',item.datetime)>=holidaylist[len(holidaylist)-1][1]:
                item.semester=len(holidaylist)
    for item in daylist:
        for i in range(1,len(holidaylist)):
            if item.day<=holidaylist[i][0] and item.day>=holidaylist[i-1][0]:
                item.semester=i
            if item.day<=holidaylist[0][0]:
                item.semester=0
            if item.day>=holidaylist[len(holidaylist)-1][1]:
                item.semester=len(holidaylist)
                
            
def findDayFood(allList,daylist):
    for item in allList:
        if item.type=='Market':
            [x.food for x in daylist if x.day==time.strftime('%Y%m%d',item.datetime)][0][0]=1
        if item.type=='Breakfast':
            [x.food for x in daylist if x.day==time.strftime('%Y%m%d',item.datetime)][0][1]=1
        if item.type=='Lunch':
            [x.food for x in daylist if x.day==time.strftime('%Y%m%d',item.datetime)][0][2]=1
        if item.type=='Dinner':
            [x.food for x in daylist if x.day==time.strftime('%Y%m%d',item.datetime)][0][3]=1
        if item.type=='Snack':
            [x.food for x in daylist if x.day==time.strftime('%Y%m%d',item.datetime)][0][4]=1
		
		
		
		
class Consume :
    def __init__(self,data):
        self.data=data
        self.money=float(re.split('\t',self.data)[2])
        self.datetime=time.strptime(data.split('\t')[4],'%Y-%m-%d %H:%M:%S')
        self.place=re.split('\t',self.data)[5]
        self.type=''
        self.semester=-1
    def output(self) :
        print self.datetime
class day:
    def __init__(self,day,money):
        self.day=day
        self.money=money
        self.semester=-1
        self.wday=time.strptime(self.day,'%Y%m%d').tm_wday
        self.food=[0,0,0,0,0]
class month:
    def __init__(self,month,money):
        self.month=month
        self.money=money
class place:
    def __init__(self,place,money):
        self.place=place
        self.money=money




dataFile=open('c://123','r')
for line in dataFile:
    allList.append(Consume(line))


for item in allList:
    tmp_time=item.datetime
    money=item.money
    if (time.strftime('%Y%m%d',tmp_time))not in daydict.keys():
        daydict[time.strftime('%Y%m%d',tmp_time)]=item.money
    else:
        daydict[time.strftime('%Y%m%d',tmp_time)]+=item.money
        
    if (time.strftime('%Y%m',tmp_time))not in mondict.keys():
        mondict[time.strftime('%Y%m',tmp_time)]=item.money
    else:
        mondict[time.strftime('%Y%m',tmp_time)]+=item.money

    if item.place not in placedict.keys():
        placedict[item.place]=item.money
    else:
        placedict[item.place]+=item.money
        
for item in sorted([(x,daydict[x]) for x in daydict.keys()],key=lambda x:x[0]):
    daylist.append(day(item[0],item[1]))
for item in sorted([(x,mondict[x]) for x in mondict.keys()],key=lambda x:x[0]):
    
    monlist.append(month(item[0],item[1]))
for item in sorted([(x,placedict[x]) for x in placedict.keys()],key=lambda x:x[0]):
    placelist.append(place(item[0],item[1]))


holiday(daylist,holidaylist)
findSemester(allList,holidaylist)
findType(allList)
maxConsume(allList)
maxDayConsume(daylist)
foodRate(allList)
#foodRateOfSemester(allList,holidaylist)
findDayFood(allList,daylist)



print len([x for x in daylist if x.semester==1 and x.food[2]==1 and x.wday==0])*1.0/len([x for x in daylist if x.semester==3 and x.wday==0])
