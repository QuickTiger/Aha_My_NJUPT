import MySQLdb
cx=MySQLdb.connect(host='localhost',user='',passwd='',db='NUPT_user',charset='utf8')
cu=cx.cursor()
cu.execute('create table if not exists Consume (StudentID nvarchar(15) not null ,CONSUMETYPE nvarchar(10),CURRENTDBMONEY double,CARDNO nvarchar(10),FLOWCODE nvarchar(15) primary key,CONTYPE nvarchar(10),DISPOSETIME datetime,CONSUMETIME datetime,RN int,TRANSACTMONEY double,WINNAME nvarchar(30))')
cx.commit()
