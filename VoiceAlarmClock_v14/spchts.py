#encoding=utf-8
import speech_recognition as sr
import pyaudio
import re
import jieba
import sqlite3
import os
import weather
import ui

def speech_rc():                                                #語音辨識
    try:
        r = sr.Recognizer()                                     #設定語音辨識的物件
        print("請說話:")
        with sr.Microphone() as source:                         #音源輸入設定為麥克風並取名叫source
            r.adjust_for_ambient_noise(source,duration=0.5)     #處理噪音，分析音頻源中0.5秒鐘長的音頻
            audio = r.listen(source)                            #可以使用 with 塊中 Recognizer 類的 listen（）方法捕獲麥克風的輸入。該方法將音頻源作為第一個引數，並自動記錄來自源的輸入，直到檢測到靜音時自動停止。
        print(r.recognize_google(audio, language='zh-TW'))
        ui.setTitle("-語音辨識中-")
        voice_output=r.recognize_google(audio, language='zh-TW')#音訊以中文做轉換，辨識器採用google
        return voice_output
    except sr.UnknownValueError:
        print("未輸入聲音")
        ui.setTitle("-未輸入聲音-")
        
    except sr.RequestError as e:
        print("無法連接到辨識器:", e)
        ui.setTitle("-無法連接到辨識器-")
    except OSError as e:
        print("未偵測到音源輸入設備:",e)
        ui.setTitle("-未偵測到音源輸入設備-")

def jbcut(input_voice):                                         #語音斷詞
    jieba.set_dictionary('dict.txt.big')                        #載入中文繁體詞庫
    word_list = []

    l=input_voice

    arr = re.sub(r"([\w\W\u4e00-\u9fff]-)", "", l)               #正規化句子
    out = jieba.cut(arr)                                        #利用jieba進行斷詞
    for s in out :
        word_list.append(s)                                     #輸出結果寫回list
    return word_list

def keyword_file_load():                                        #設定我們需要的關鍵字
    try:
        conn=sqlite3.connect('keyword.db')
                                                                #建立關鍵字的資料庫及表
        conn.execute('''
        create table if not exists kwddict(
            kwd     char(20)    not null,
            mch     char(20)    not null
        );
        ''')
    except:
        print("table create ERROR")
    if not(os.path.isfile('check.txt')):                        #判斷是否有寫入過資料進資料表，若有寫過會出現check.txt的空檔案
        with open('keywordlist.txt','r',encoding='UTF-8') as f: #寫入設計好的關鍵字
            for line in f:
                a,b=line.strip("\n").split(",")
                try:
                    conn.execute('''insert into kwddict(kwd,mch) values(?,?);''',(a,b))
                    conn.commit()
                except:
                    print("data insert ERROR")
        open('check.txt','w').close()                           #寫入完畢後建立check.txt以防止下次呼叫重複寫入關鍵字

def keyword_check(input_word):                                  #確認說的話中是否有含關鍵字
    kystr=[]
    timelist=[]
    ky=""
    try:
        conn=sqlite3.connect('keyword.db')
        patten=re.compile(r'\d+')                               #建立只找數字的樣板
        for word in input_word:                                 #逐一與資料庫裡的關鍵字做比對
            results=conn.execute('''select mch from kwddict where kwd=?;''',(word,))
            for result in results:
                #print(result)
                ky=result[0]                                    #若有找到，則將應對的機械碼加入kystr以確定會執行的功能
                kystr.append(ky)
            num_check = patten.match(word)                      #擷取數字加入timelist以確定要設定鬧鐘的值，以下三行皆是
            if num_check:
                timelist.append(num_check.group())
        if len(timelist)<2 and len(timelist)>0:
            timelist.append("0")
        return kystr,timelist
    except Exception as e:
            print("search ERROR",e)


if __name__ == "__main__":
    
    keyword_file_load()
    try:
        while(True):                        #一定要用線程跑
            rs=None
            rs=speech_rc()
            if rs!=None:
                jbc=jbcut(rs)
                outpt,outtm=keyword_check(jbc)
                print(outpt, outtm)
    except KeyboardInterrupt:
        print("終止程式")