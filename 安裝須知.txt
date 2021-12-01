VoiceAlarmClock /語音鬧鐘    版本：v14 
Python版本：3.7
------------------------------------------------------------------------

用途：在關燈上床休息時也能使用語音設定明日鬧鐘及了解上午天氣狀況

------------------------------------------------------------------------
直接複製虛擬環境venv可能會因路徑不同而發生問題
使用pip freeze > requirements.txt將所用套件訊息打包移植到不同電腦安裝，
其中Pyaudio在Python3.7安裝較特別，需要用官網的.whl檔安裝，以下為教學

新電腦如何安裝：

方法一:
在命令提示字元裡
輸入pip install virtualenv (安裝虛擬環境)
↓
輸入cd 目錄路徑
↓
輸入virtualenv venv
↓
輸入venv\Scripts\activate
↓
輸入pip install -r requirements.txt 
↓
輸入pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl
↓
輸入python main.py

方法二:
安裝Anaconda
輸入conda install pyaudio

------------------------------------------------------------------------
若遇到解析度100%以上電腦(win10)，排版縮放會有問題。
請至.\venv\Scripts\python.exe右鍵-內容-相容性-變更高DPI設定
將"覆寫高DPI縮放比例行為"打勾


