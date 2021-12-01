import sqlite3

def getUserList():
    try:
        cursor = conn.execute(' select * from user; ')
        print('讀取使用者清單')
        return cursor
    except:
        return ""

def getTime():
    try:
        cursor = conn.execute(' select * from time; ')
        print('讀取使用者時間')
        return cursor
    except:
        return ""

def setTime(in1,in2,in3):

    conn.execute(" update time set hour='{}' where week='{}'; ".format(in2,in1))
    conn.execute(" update time set minute='{}' where week='{}'; ".format(in3, in1))
    
    conn.commit()

def add_user(in1,in2):
    try:
        conn.execute("insert into user(acc, pwd) values ('{}','{}');" \
            .format(in1, in2))
        print('資料庫使用者已新增')
        conn.commit()
    except:
        print('=>新增帳號 {} 失敗'.format(in1))


def add_log(in1,in2):
    try:
        with sqlite3.connect("database.db") as con:

            con.execute("insert into log(input, output) values ('{}','{}');" \
                        .format(in1, in2))
            print('資料庫語音紀錄已新增')
            con.commit()

    except:
        print('=>新增語音紀錄失敗')

try:
    conn = sqlite3.connect('database.db')
    conn.execute('''create table if not exists user(
                    acc char(10) not null,
                    pwd char(10) not null); ''')
                    
    conn.execute('''create table if not exists log(
                    input char(10) not null, 
                    output char(10) not null); ''')

    conn.execute('''create table if not exists time(
                    week char(10) not null,
                    hour char(10) not null,
                    minute char(10) not null); ''')
    for i in range(7):
        
        conn.execute("insert into time(week, hour, minute) select '{}', '{}', '{}' \
                where not exists(select 1 from time where week='{}'); "\
                    .format(i+1, '-', '-', i+1))
        
    conn.commit()
except:
    print('=>資料庫連接或資料表建立失敗')
    quit()


