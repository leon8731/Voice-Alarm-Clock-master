import ui
import winsound # 匯入此模組實現聲音播放功能
import time  # 匯入此模組，獲取當前時間
import weather


def ins_choice(ins_list,num_list,ins):                    #機械碼轉換動作程式
    if len(ins_list)>0:
        if "st" in ins_list:                            #判讀有說出設定才開始動作
            if len(num_list)>0:
                if "pmc" in ins_list:                   #下午轉換
                    chg=int(num_list[0])
                    chg+=12
                    num_list[0]=str(chg)
    #---------------------------------------------------------星期轉換
                week=0
                if "mon" in ins_list:
                    week=1
                    ui.setClockInfo(1,int(num_list[0]),int(num_list[1]))
                    ui.addAudioRecord(ins,"好的已設定！")
                if "tue" in ins_list:
                    week=2
                    ui.setClockInfo(2,int(num_list[0]),int(num_list[1]))
                    ui.addAudioRecord(ins,"好的已設定！")
                if "wed" in ins_list:
                    week=3
                    ui.setClockInfo(3,int(num_list[0]),int(num_list[1]))
                    ui.addAudioRecord(ins,"好的已設定！")
                if "thu" in ins_list:
                    week=4
                    ui.setClockInfo(4,int(num_list[0]),int(num_list[1]))
                    ui.addAudioRecord(ins,"好的已設定！")
                if "fri" in ins_list:
                    week=5
                    ui.setClockInfo(5,int(num_list[0]),int(num_list[1]))
                    ui.addAudioRecord(ins,"好的已設定！")
                if "sat" in ins_list:
                    week=6
                    ui.setClockInfo(6,int(num_list[0]),int(num_list[1]))
                    ui.addAudioRecord(ins,"好的已設定！")
                if "sun" in ins_list:
                    week=7
                    ui.setClockInfo(7,int(num_list[0]),int(num_list[1]))
                    ui.addAudioRecord(ins,"好的已設定！")
                if "tdy" in ins_list:
                    chweek=int(getNowweek())
                    if chweek==0:
                        chweek=7
                    ui.setClockInfo(chweek,int(num_list[0]),int(num_list[1]))
                    ui.addAudioRecord(ins,"好的已設定！")
                if "tmr" in ins_list:
                    chweek=int(getNowweek())+1
                    if chweek > 7:
                        chweek=1
                    ui.setClockInfo(chweek,int(num_list[0]),int(num_list[1]))
                    ui.addAudioRecord(ins,"好的已設定！")
                weather.weather_voice()
                ui.setClockOn()
                time.sleep(13)
            else:
                ui.addAudioRecord(ins,"未輸入時間!")
        if 'auto' in ins_list:
            week, h, m = ui.getClockInfo()
            ui.addAudioRecord(ins, '上課鬧鐘已設定啟動！')
            weather.weather_voice()
            ui.setClockOn(week+1)
            time.sleep(13)

    #-----------------------------------------------------------關閉鬧鐘
        if "cl" in ins_list:
            ui.setClockOff()
            ui.addAudioRecord(ins,"好的已清除！")
    #-----------------------------------------------------------開啟鬧鐘
        if "op" in ins_list:
            ui.setClockOn()
            ui.addAudioRecord(ins, "好的已開啟！")
    else:
        ui.addAudioRecord(ins,"未輸入指令!")

def getNowHour():
    t = time.localtime()  # 當前時間的紀元值
    fmt = "%H %M"
    now = time.strftime(fmt, t)  # 將紀元值轉化為包含時、分的字串
    now = now.split(' ')  # 以空格切割，將時、分放入名為now的列表中
    return(now[0])

def getNowweek():
    wt=time.localtime()
    wmt= "%w"
    wnow=time.strftime(wmt,wt)
    return wnow