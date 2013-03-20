import sqlite3
cx=sqlite3.connect("./data_consume.db")
cu=cx.cursor()
while True:
    s=raw_input()
    if s.find('end')>-1:
        break
    s=cu.execute(s)
    for line in s:
        print(line)

cx.close()

