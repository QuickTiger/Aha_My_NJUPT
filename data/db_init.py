import sqlite3
cx=sqlite3.connect("./data_consume.db")
cu=cx.cursor()
cu.execute('create table if not exists Consume (StudentID nvarchar(30),CONSUMETYPE nvarchar(30),CURRENTDBMONEY nvarchar(30),CARDNO nvarchar(30),FLOWCODE nvarchar(30),CONTYPE nvarchar(30),DISPOSETIME nvarchar(30),CONSUMETIME nvarchar(30),RN nvarchar(30),TRANSACTMONEY nvarchar(30),WINNAME nvarchar(30))')
cx.commit()
