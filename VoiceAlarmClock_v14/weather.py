import pyperclip    #剪貼簿
import tempfile    #臨時檔案,關閉後會自動刪除
import re   
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys    
from gtts import gTTS   #文字轉成語音
from pygame import mixer    #用於載入和播放聲音的pygame模組

import ui

def speak(sentence, lang, loops=1):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts=gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()  #初始化混音器模組
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play(1) #播放次數

citylist = [ 'https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=63',
        'https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=65',   
        'https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=66',
        'https://www.cwb.gov.tw/V8/C/W/County/County.html?CID=64']


def weather_voice():
    speak('設定完成 明日天氣 {}'.format(fin), 'zh-tw')

def weather_view(in1):

    ui.label_weatherInfo.config(text='獲取天氣資訊中..')
    ui.label_img.place_forget()
    
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(citylist[in1])   #讀取城市天氣預報網址
    element = driver.find_element_by_tag_name('body')
    element.send_keys(Keys.CONTROL + 'a')   #全選
    element.send_keys(Keys.CONTROL + 'c')   #複製
    driver.quit()   #關閉

    text = pyperclip.paste()    #取得剪貼簿文字
    patten = re.compile('發布時間(.*)發布時間', re.DOTALL)
    matchList = patten.findall(text)
    str1 = "".join(matchList)
    str2 = str1.splitlines()
    global fin
    fin = str(str2[7]) + "\r\n" + str(str2[8]) + "度\r\n" + str(str2[9]) + \
    "\r\n" + str(str2[10]) + "\r\n"
    print(fin)
    ui.setWeatherInfo(fin)

