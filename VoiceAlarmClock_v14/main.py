import ui
import weather as w
import winsound  # 匯入此模組實現聲音播放功能
import time
import threading
import spchts
import command
import weather
#                 #目前做的鬧鐘七天都可設時間，啟動不用傳參數只能啟動當天的~(應該是要明天的，方便測試所以改當天的)。
# 可用ㄉ函式    
# ui.addAudioRecord('輸入','輸出')       #新增語音紀錄
# ui.setClockInfo(星期,時,分)            #設定鬧鐘啟動資訊(跟那個手動設定一樣 星期日=7)
# ui.setClockOn()                       #啟動鬧鐘
# ui.setClockOff()                      #關閉鬧鐘
# ui.getIslogin()                       #取得使用者是否登入(回傳布林值)
# ui.getFormIsClose()                   #取得視窗是否關閉(回傳布林值)
# ui.getClockIsOn()                     #取得鬧鐘是否啟動(回傳布林值)
# ui.getClockInfo()                     #取得鬧鐘啟動資訊(回傳三個參數"星期","時","分")


 

def job():
    i = 0
    print('提示：您尚未登入！')
    while not ui.getIslogin() and not ui.getFormIsClose():#_____________________如果沒登入、視窗沒關就卡在這循環
        time.sleep(1)
    t3.start()
    # while i < 10 and not ui.getFormIsClose():#________________________________測試用
    #     i+=1
    #     if i == 4:
    #         print('loop{} #語音輸入：設定鬧鐘星期六21點13分'.format(i))
    #         ui.addAudioRecord('幫我設定鬧鐘', '好的已設定！')
    #         ui.setClockInfo(7, 0, 24)
    #     elif i == 8:                                                          
    #         print('loop{} #啟動鬧鐘'.format(i))
    #         ui.setClockOn()#____________________________________________________啟動鬧鐘
    #         ui.addAudioRecord('啟動鬧鐘', '好的已啟動！')#________________________將文字紀錄到語音紀錄
    #         # t3.setDaemon(True)
            
    #         #_______________________________________開天氣爬蟲
    #     else:
    #         print('loop{}'.format(i))
    #     time.sleep(1)
    #-------------------------------------------測試完啟動語音
    thread2 = myThread(2, "Thread-2")
    thread2.setDaemon(True)
    thread2.start()


def voice():                                #語音程式用線程在背景運作
    
    spchts.keyword_file_load()
    try:
        while(True):
            rs=None
            rs=spchts.speech_rc()
            if rs!=None:
                jbc=spchts.jbcut(rs)
                outpt,outtm=spchts.keyword_check(jbc)
                command.ins_choice(outpt, outtm, rs)
                ui.setTitle("-等待語音輸入-")
                #print(outpt)
    except Exception as e:
        print("終止程式:",e)

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        voice()
#_______________________________________________________________________________以下線程啟動
t = threading.Thread(target=job)
t.start()




#_______________________________________________________________________________以下鬧鐘
def clockStrat():
    while not ui.getFormIsClose():
        while ui.getClockIsOn() and not ui.getFormIsClose():
            t = time.localtime()  # 當前時間的紀元值
            fmt = "%H %M"
            now = time.strftime(fmt, t)  # 將紀元值轉化為包含時、分的字串
            now = now.split(' ')  # 以空格切割，將時、分放入名為now的列表中
            hour = now[0]
            minute = now[1]

            try:
                a,my_hour, my_minute = ui.getClockInfo()
                if len(my_hour) == 1:
                    my_hour = '0' + str(my_hour)
                if len(my_minute) == 1:
                    my_minute = '0'+str(my_minute)
            except:
                print('鬧鐘時間沒設')

            print('你設定{}:{}  現在{}:{}'.format(my_hour, my_minute, hour, minute))
            if my_hour == hour and my_minute == minute:
                music = 'Candyland.wav'
                winsound.PlaySound(music, winsound.SND_FILENAME)
                break
            time.sleep(1)
        if not ui.getClockIsOn():
            t = time.localtime()  # 當前時間的紀元值
            fmt = "%w %M"
            now = time.strftime(fmt, t)  # 將紀元值轉化為包含時、分的字串
            now = now.split(' ')  # 以空格切割，將時、分放入名為now的列表中
            week = int(now[0])
            minute = now[1]
            a,my_hour, my_minute = ui.getClockInfo()
            if not (my_minute == minute):
                ui.setClockOn(week+1)
            time.sleep(1)

t3 = threading.Thread(target=clockStrat)



#最後一行要加上這個
ui.form.mainloop()