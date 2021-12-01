import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
import threading
import weather as w
import db
# ------------------------------------------------------------↓使用者函式--------

def setClockOff():
    global clockFlag
    clockFlag = False
    print('關閉鬧鐘聲響')
    clockimage.place_forget()


def setClockOn(in1 = ''):
    global clockFlag
    global clock_Next
    clock_Next = False
    clockFlag = True
    week, a, b = getClockInfo()
    if in1 != '':
        clock_Next = True
        week2, a, b = getClockInfo()
        if a != '-' and b != '-':
            week = in1
            p = 23
            clockimage.place(x=480, y=61 + p * (week2 - 1))
            print('鬧鐘啟動')
        else:
            clock_Next = False
            p = 23
            clockimage.place(x=480, y=61 + p * (week - 1))
    elif a != '-' and b != '-':
        p = 23
        clockimage.place(x=480, y=61 + p * (week - 1))
        print('鬧鐘啟動')
    else:
        print('時間錯誤')
        clockFlag = False
        tk.messagebox.showerror('錯誤', message='請填寫時間！')

def setClockInfo(in1,in2,in3):
    week = ['一', '二', '三', '四', '五', '六', '日']
    clocklist[in1]['h'] = str(in2)
    clocklist[in1]['m'] = str(in3)
    showClockInfo()

def setWeatherInfo(in1):
    global weather
    s = in1.split('\r')
    if '晴' in s[0]:
        weather = 1
    elif '雨' in s[0]:
        weather = 5
    elif '多雲' in s[0]:
        weather = 3
    weatherAnime()
    
    s = ''.join(s)
    label_img.place(x=660,y=315)
    label_weatherInfo.config(text=s)
    label_weatherInfo.place(x=480, y=320 , width=185)
    # label_weatherInfo.place(x=450, y=390 , width=185, height=100)

def setTitle(in1):
    form.title('已登入  使用者：{}   {}'.format(entryText_account.get(),in1))

def addAudioRecord(in1='', in2=''):
    db.add_log(in1,in2)
    tv.insert('', 'end', text=in1, values=(in2))

def getIslogin():
    global loginFlag
    return loginFlag

def getCity():
    if comboBlood.get() == '臺北市':
        return 0
        print('天氣更改:臺北市')
    if comboBlood.get() == '新北市':
        return 1
        print('天氣更改:新北市')
    if comboBlood.get() == '臺中市':
        return 2
        print('天氣更改:臺中市')
    if comboBlood.get() == '高雄市':
        return 3
        print('天氣更改:高雄市')
def getFormIsClose():
    global closeFlag
    if closeFlag:
        return True
    else:
        return False

def getClockIsOn():
    global clockFlag
    if clockFlag:
        return True
    else:
        return False

def getClockInfo():
    global clock_Next
    now_week = int(time.strftime('%w'))
    if now_week == 0:
        now_week = 7
    if clock_Next == True:
        now_week = now_week+1
    return (now_week,clocklist[now_week]['h'],clocklist[now_week]['m'] )

# ------------------------------------------------------------↓按鍵事件----------
def buttonClick_login():
    global loginFlag
    acc = entry_account.get()
    pwd = entry_password.get()
    if (acc in acclist):
        if (pwd in pwdlist):
            print('已登入')
            loginFlag = True
            tk.messagebox.showinfo('提示', message='登入成功！')
            showMenu()
            w.weather_view(getCity())
        else:
            tk.messagebox.showerror('錯誤',message='您輸入的密碼錯誤，請重新輸入！')
    else:
        isSignup = tk.messagebox.askyesno('提示', message='您尚未註冊！要立刻註冊嗎？')
        if isSignup:
            buttonClick_signup()

def buttonClick_signup():
    def signup():
        acc = signup_entry_account.get()
        pwd = signup_entry_password.get()
        pwd_confirm = signup_entry_pwd_confirm.get()
        #在這行載入資料庫
        if (acc in acclist):
            tk.messagebox.showerror('錯誤', message='這個帳號已被註冊過了！')
        elif pwd != pwd_confirm:
            tk.messagebox.showerror('錯誤', message='兩次輸入的密碼不同！')
        else:
            acclist.append(acc)
            pwdlist.append(pwd)
            db.add_user(acc,pwd)
            #在這行取出資料庫
            form_signup.destroy()
            tk.messagebox.showinfo('提示', message='註冊成功！')

    form_signup = tk.Toplevel(form)
    form_signup.geometry('350x200+770+420')
    form_signup.title('註冊')

    acc = tk.StringVar()
    acc.set('{}'.format(entry_account.get()))
    tk.Label(form_signup, text='帳號： ').place(x=10, y=10)
    signup_entry_account = tk.Entry(form_signup, textvariable=acc)
    signup_entry_account.place(x=150, y=10)

    pwd = tk.StringVar()
    tk.Label(form_signup, text='密碼: ').place(x=10, y=50)
    signup_entry_password = tk.Entry(form_signup, textvariable=pwd, show='*')
    signup_entry_password.place(x=150, y=50)

    pwd_confirm = tk.StringVar()
    tk.Label(form_signup, text='確認密碼：').place(x=10, y= 90)
    signup_entry_pwd_confirm = tk.Entry(form_signup, textvariable=pwd_confirm, show='*')
    signup_entry_pwd_confirm.place(x=150, y=90)

    button_signup = tk.Button(form_signup, text=' 註冊 ', command=signup)
    button_signup.place(x=150, y=130)

def buttonClick_setClock():
    def save():

        for i in range(7):
            clocklist[i + 1]['h'] = entrylist[i].get()
            clocklist[i + 1]['m'] = entrylist[i + 7].get()
            db.setTime(i + 1, entrylist[i].get(), entrylist[i + 7].get())
        showClockInfo()
        week, a, b = getClockInfo()
        setClockOn(week)
        form_setClock.destroy()


    form_setClock = tk.Toplevel(form)
    form_setClock.geometry('400x300+770+420')
    form_setClock.title('設定')
    form_setClock.wm_attributes('-topmost', 1)
    form_setClock.resizable(False, False)
    frame1 = tk.Frame(form_setClock)
    frame2 = tk.Frame(form_setClock)
    frame1.pack(side='left', padx=10, expand=1)
    frame2.pack(side='right')
    # tk.Label(form_setClock,text='格式：hh:mm',font=('標楷體',10)).place(x=220,y=6)
    week = ['一', '二', '三', '四', '五', '六', '日']
    for i in range(7):
        tk.Label(frame1, text='星期{}      :'.format(week[i]), font=('標楷體',14)).pack(side='top')

    StringVarList_h = []
    StringVarList_m = []
    for i in range(7):
        h = tk.StringVar()
        h.set(clocklist[i+1]['h'])
        StringVarList_h.append(h)
    for i in range(7):
        m = tk.StringVar()
        m.set(clocklist[i+1]['m'])
        StringVarList_m.append(m)

    entrylist = []
    for i in range(7):
        e = tk.Entry(form_setClock, textvariable=StringVarList_h[i], width='3')
        e.place(x=230,y=i*29+52)
        entrylist.append(e)
    for i in range(7):
        e = tk.Entry(form_setClock, textvariable=StringVarList_m[i], width='3')
        e.place(x=290,y=i*29+52)
        entrylist.append(e)

    button_save = tk.Button(form_setClock, text='儲存', command=save)
    button_save.place(x=190,y=262,width=50, height=24)    

def buttonClick_help():
    s = ''
    i = 1
    with open('keywordlist.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            a, b = line.strip("\n").split(",")

            s += a + ' ,  '
        s = s[:-4]

    tk.messagebox.showinfo('可識別關鍵字↓', message=s)

def buttonClick_Clock_end():
    clockFlag = False
    setClockOff()
    
# ------------------------------------------------------------↓其他功能----------
def showMenu():
    frame_login.destroy()
    form.geometry('840x485+450+150')
    form.wm_attributes('-topmost',1)
    form.title('已登入  使用者：{}     {}'.format(entryText_account.get(),'-等待語音輸入-'))
    frame_menu.pack(fill='both', expand=1)

def showNow():
    week = ['日', '一', '二', '三', '四', '五', '六', '']
    global now
    now = time.strftime('%Y %m %d %w %I %M %S %H').split(' ')
    tk.Label(frame_menu, text="{}年{}月{}日 星期{}"\
        .format(now[0],now[1],now[2],week[int(now[3])]), \
        font=("標楷體", 14)).place(x=90, y=135)
    tk.Label(frame_menu, text='{} {}:{}:{}'\
        .format("上午" if int(now[7]) < 12 else "下午",now[4],now[5],now[6]), \
        font=("Times", 32)).place(x=50, y=60)
    frame_menu.after(1000, showNow)

def weatherAnime():
    global weatherFlag
    if weatherFlag == 0:
        img.config(file=imglist[weather])
        weatherFlag = 1
    else:
        img.config(file=imglist[weather + 1])
        weatherFlag = 0
    frame_menu.after(1000,weatherAnime)

def clockAnime():
    global cflag
    if cflag == 0:
        clockimg.config(file=imglist[8])
        cflag = 1
    else:
        clockimg.config(file=imglist[9])
        cflag = 0
    frame_menu.after(1000,clockAnime)
    



def showClockInfo():
    tk.Label(frame_menu, \
            text='星期一  {}\n星期二  {}\n星期三  {}\n星期四  {}\n星期五  {}\n星期六  {}\n星期日  {}'\
            .format(':'.join(clocklist[1].values()), ':'.join(clocklist[2].values()), \
            ':'.join(clocklist[3].values()), ':'.join(clocklist[4].values()), \
            ':'.join(clocklist[5].values()),':'.join(clocklist[6].values()),':'.join(clocklist[7].values())) \
            ,font=("標楷體", 14),justify = 'left') \
            .place(x=505, y=60)

def closeform():
    global closeFlag
    closeFlag = True
    print('視窗已關閉')
    db.conn.close()
    form.destroy()


# ------------------------------------------------------------↓主程式、主視窗----
global loginFlag
global closeFlag
global clockFlag
global clock_Next
closeFlag = False
loginFlag = False
clockFlag = True
clock_Next = False
cflag = 0
weatherFlag = 0
weather = 0
acclist = []
pwdlist = []
for record in db.getUserList():
    acclist.append(record[0])
    pwdlist.append(record[1])

form = tk.Tk()
form.geometry('540x330+500+200')
form.resizable(False, False)
form.title('未登入')

imglist = [ 'img/cwb.png',
        'img/01.png', 
        'img/02.png', 
        'img/05.png', 
        'img/06.png', 
        'img/09.png', 
        'img/10.png',
        'img/logo.png',
        'img/clockset.png',
        'img/clockset2.png']

# ------------------------------------------------------------↓建立登入視窗------
frame_login = tk.Frame(form)
frame_login.pack(fill='both', expand=1)
px = -30
py = 10

tk.Label(frame_login, text='帳號： ').place(x=280+px, y= 190+py)
tk.Label(frame_login, text='密碼： ').place(x=280+px, y= 230+py)
entryText_account = tk.StringVar()
entryText_account.set('')
entry_account = tk.Entry(frame_login, textvariable = entryText_account)
entry_account.place(x=340+px, y=192+py)
entry_password = tk.Entry(frame_login, show="*")
entry_password.place(x=340+px, y=232+py)
button_login = tk.Button(frame_login, text=' 登入 ', command=buttonClick_login)
button_login.place(x=370+px, y=272+py,height=25)
button_signup = tk.Button(frame_login, text=' 註冊 ', command = buttonClick_signup)
button_signup.place(x=430+px, y=272+py,height=25)


logo = tk.PhotoImage(file = imglist[7])
login_img = tk.Label(frame_login, image = logo)
login_img.place(x=0, y=40)

# ------------------------------------------------------------↓建立選單視窗------
frame_menu = tk.Frame(form)


                # --------------------------------------------↓現在時間----------
tk.Label(frame_menu, text='現在時間 ', font=('time', 16, 'italic')).place(x=10, y=10)
showNow()


                # --------------------------------------------↓語音紀錄----------
tk.Label(frame_menu, text='語音紀錄 ', font=('time', 16, 'italic')).place(x=10, y=200)
tv = ttk.Treeview(frame_menu, columns=('content'))
tv.column('#0', width=200)
tv.column('#1', width=180)
tv.heading('#0', text='輸入')
tv.heading('#1', text='回應')
sb = ttk.Scrollbar(frame_menu, orient="vertical", command=tv.yview)
sb.place(x=386, y=251, height=225)
tv.configure(yscrollcommand=sb.set)
tv.place(x=25, y=250)

                # --------------------------------------------↓鬧鐘設定----------
tk.Label(frame_menu, text='鬧鐘設定 ',font=('time', 16,'italic')).place(x=460, y=10)

button_cancelClock = tk.Button(frame_menu, text='關閉聲響', command=buttonClick_Clock_end)

button_cancelClock.place(x=745, y=18, width=80, height=24)

button_setClock = tk.Button(frame_menu, text='手動設定', command=buttonClick_setClock)
button_setClock.place(x=745, y=47, width=80, height=24)

# button_setClock = tk.Button(frame_menu, text='手動啟動', command=setClockOn)
# button_setClock.place(x=745, y=76, width=80, height=24)

button_setClock = tk.Button(frame_menu, text='語音關鍵字', command=buttonClick_help)
button_setClock.place(x=745, y=76, width=80, height=24)
# button_setClock.place(x=745, y=105, width=80, height=24)

# imgc = tk.PhotoImage(file = imglist[8])
# img_clock = tk.Label(form, image = imgc)
# img_clock.place(x=720, y=12)
# tk.Label(frame_menu, text='表示已啟動',font=('time', 9)).place(x=747, y=19)

clocklist = [ {},
    {'h': '-', 'm': '-'},
    {'h': '-', 'm': '-'},
    {'h': '-', 'm': '-'},
    {'h': '-', 'm': '-'},
    {'h': '-', 'm': '-'},
    {'h': '-', 'm': '-'},
    {'h': '-', 'm': '-'}
]
for record in db.getTime():
    clocklist[int(record[0])]['h'] = record[1]
    clocklist[int(record[0])]['m'] = record[2]

showClockInfo()

                # --------------------------------------------↓天氣預報----------
tk.Label(frame_menu, text='天氣預報 ',font=('time', 16,'italic')).place(x=460, y=250)

img = tk.PhotoImage(file = imglist[0])
label_img = tk.Label(form, image = img)
label_img.place(x=680, y=310)
#___________________________________________________________________________________________________
clockimg = tk.PhotoImage(file = imglist[8])
clockimage = tk.Label(form, image=clockimg)
clockAnime()



comboBlood = ttk.Combobox(frame_menu, values=('臺北市', '新北市', '臺中市','高雄市'))
comboBlood.place(x=600, y=258, width=80, height=22)
comboBlood.current(2)  #默認選擇第一個
comboBlood_btn= tk.Button(frame_menu, text='更改', command=lambda:w.weather_view(getCity()))
comboBlood_btn.place(x=682, y=258, width=50, height=22)

tk.Label(frame_menu, text='天氣來源：中央氣象局', font=('標楷體',12))\
        .place(x=630, y=455)

label_weatherInfo = tk.Label(frame_menu, text='OuO', font=("標楷體", 14),justify = 'left')
label_weatherInfo.place(x=530, y=350 , width=185)


# ------------------------------------------------------------↓其他-------------
form.protocol("WM_DELETE_WINDOW", closeform)
# form.withdraw()
# form.deiconify()

