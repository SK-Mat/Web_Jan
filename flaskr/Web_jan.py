from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
from tkcalendar import *
import requests
import time
import datetime
from tkinter import messagebox
import threading
import pandas as pd
import webbrowser

urls = {}
facility_dict = {}
takatsuki = {"高槻2号":"68","高槻3号":"196","高槻シースー":"243"}
umeda = {"お初天神":"94","北新地":"144","東通":"155","かっぱ横丁":"120","東通本店":"116","S茶屋町":"106","東通3号":"103","茶屋町":"100","東中通":"76","梅田芝田町":"199","アジアン天満":"234","東通白馬車ビル":"237"}
kyobashi = {"京橋1号":"32","京橋本店":"174","京橋Door4":"236"}
nanba_shinsaibashi = {"アメリカ村":"45","心斎橋":"23","心斎橋3号":"119","千日前2号":"91","千日前3号":"203","宗右衛門町":"222","道頓堀":"109","南海通なんば":"70","なんさん通り":"172","なんば":"51","なんば本店":"96"}
kyoto = {"河原町本店":"104","京都駅前":"146","西院駅前":"132","三条河原町":"73","京都駅前":"146","四条大宮駅前":"187","四条河原町":"53","ジャジャーンカラ京大BOX":"228","S河原町本店":"105","同志社前":"148","桃山御陵前":"205","山科駅前":"113","六地蔵":"163",}
machine_list = ["JOYSOUND MAX GO","JOYSOUND MAX2","JOYSOUND MAX","LIVE DAM STADIUM","LIVE DAM Ai"]
now_status = "※複数回実行ボタンを押さないでください。"
button_state = "able"

def main():
    column = ("店舗名","JOYSOUND MAX GO","JOYSOUND MAX2","JOYSOUND MAX","LIVE DAM STADIUM","LIVE DAM Ai")

    root = Tk()
    root.title("空室確認")

    #フレームの定義
    frame_1 = Frame(root)
    frame_2 = Frame(root)
    frame_3 = Frame(root)

    #オブジェクトの定義
    var_umeda = BooleanVar()
    chk_umeda = Checkbutton(frame_1,text="大阪府（梅田）",variable = var_umeda)
    var_takatsuki = BooleanVar()
    chk_takatsuki = Checkbutton(frame_1,text="大阪府（高槻）",variable = var_takatsuki)
    var_kyobashi = BooleanVar()
    chk_kyobashi = Checkbutton(frame_1,text="大阪府（京橋）",variable = var_kyobashi)
    var_nanba_shinsaibashi = BooleanVar()
    chk_nanba_shinsaibashi = Checkbutton(frame_1,text="大阪府（難波・心斎橋）",variable = var_nanba_shinsaibashi)
    var_nanba_shinsaibashi = BooleanVar()
    chk_nanba_shinsaibashi = Checkbutton(frame_1,text="大阪府（難波・心斎橋）",variable = var_nanba_shinsaibashi)
    var_kyoto = BooleanVar()
    chk_kyoto = Checkbutton(frame_1,text="京都府",variable = var_kyoto)
    hour = StringVar()
    minute = StringVar()
    use_number = StringVar()
    use_minute = StringVar()
    course = StringVar()
    calender_date = Calendar(frame_2)
    hourbox = ttk.Combobox(frame_2,height=24,values=("00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"),textvariable=hour)
    minutebox = ttk.Combobox(frame_2,height=4,values=("00","15","30","45"),textvariable=minute)
    use_numberbox = ttk.Combobox(frame_2,height=10,values=("1","2","3","4","5","6","7","8","9","10"),textvariable=use_number)
    use_minutebox = ttk.Combobox(frame_2,height=19,values=("30","60","90","120","150","180","210","240","270","300","330","360","390","420","450","480","510","540","570"),textvariable=use_minute)
    coursebox = ttk.Combobox(frame_2,height=10,values=("昼フリー","夕方フリー","夜フリー","深夜フリー","エンドレスフリー","昼5時間パック","昼3時間パック","通常"),textvariable=course)
    hourbox.set("時")
    minutebox.set("分")
    use_number.set("人数")
    use_minute.set("利用時間(分)")
    coursebox.set("コース選択")
    status_label = ttk.Label(frame_1,text=now_status)
        #---表---
    tree = ttk.Treeview(frame_3,columns = column)
    tree.heading("#0",text="")
    tree.heading("店舗名",text="店舗名",anchor="center",)
    tree.heading("JOYSOUND MAX GO",text="JOYSOUND MAX GO",anchor="w")
    tree.heading("JOYSOUND MAX2",text="JOYSOUND MAX2",anchor="w")
    tree.heading("JOYSOUND MAX",text="JOYSOUND MAX",anchor="w")
    tree.heading("LIVE DAM STADIUM",text="LIVE DAM STADIUM",anchor="w")
    tree.heading("LIVE DAM Ai",text="LIVE DAM Ai",anchor="w")
    scrollbar = ttk.Scrollbar(frame_3, orient='v', command=tree.yview) #表にスクロールバーを追加
    tree.configure(yscrollcommand=scrollbar.set)
    #---オブジェクトの配置---
    tree.pack(pady=10,side=LEFT)
    scrollbar.pack(side=LEFT,fill=Y)
    chk_umeda.pack(side=LEFT)
    chk_takatsuki.pack(side=LEFT)
    chk_kyobashi.pack(side=LEFT)
    chk_nanba_shinsaibashi.pack(side=LEFT)
    chk_kyoto.pack(side=LEFT)
    calender_date.pack(side=LEFT)
    hourbox.pack(side=TOP)
    minutebox.pack(side=TOP)
    use_numberbox.pack(side=TOP)
    use_minutebox.pack(side=TOP)
    coursebox.pack(side=TOP)
    button = ttk.Button(frame_2,text="実行",command=lambda:[create_facility_dict(var_umeda.get(),var_takatsuki.get(),var_kyobashi.get(),var_nanba_shinsaibashi.get(),var_kyoto.get()),mult_get_table([arrange_date(calender_date),hour.get()+":"+minute.get(),use_number.get(),use_minute.get(),course.get()],tree)],state=button_state)
    button.pack(side=TOP)
    status_label.pack(side=LEFT)
    #---フレームの配置---
    frame_1.pack(side=TOP)
    frame_2.pack(side=TOP)
    frame_3.pack(side=TOP)
    root.mainloop()

def create_facility_dict(*args): #チェックボックスから店舗の辞書を生成（get_urls()に渡すため）
    global facility_dict,umeda,takatsuki,kyobashi,nanba_shinsaibashi,kyoto
    facility_dict.clear() #初期化
    if args[0] == True:
        facility_dict.update(umeda)
    if args[1] == True:
        facility_dict.update(takatsuki)
    if args[2] == True:
        facility_dict.update(kyobashi)
    if args[3] == True:
        facility_dict.update(nanba_shinsaibashi)
    if args[4] == True:
        facility_dict.update(kyoto)


def arrange_date(calender_date): #日付の整形
    month ="00"
    day="00"
    if int(calender_date.get_date().split("/")[0]) < 10:
        month = "0" + str(calender_date.get_date().split("/")[0])
    else:
        month = str(calender_date.get_date().split("/")[0])
    if int(calender_date.get_date().split("/")[1]) < 10:
        day = "0" + str(calender_date.get_date().split("/")[1])
    else:
        day = calender_date.get_date().split("/")[1]
    year = "20"+calender_date.get_date().split("/")[2]

    return year+"-"+month+"-"+day

def btn_click(msg): #テスト用
    messagebox.showinfo('サンプル', msg + " がクリックされました")

def get_urls(conditions_row): #URLを取得
    global facility_dict,urls
    urls.clear() #初期化
    conditions = conditions_row
    #---URLに従うように表記を変更
    if conditions[4] == "通常":
        conditions[4] = "1"
    elif conditions[4] == "昼フリー":
        conditions[4] = "2"
    elif conditions[4] == "夕方フリー":
        conditions[4] = "5"
    elif conditions[4] == "夜フリー":
        conditions[4] = "6"
    elif conditions[4] == "深夜フリー":
        conditions[4] = "3"
    elif conditions[4] == "エンドレスフリー":
        conditions[4] = "10"
    elif conditions[4] == "昼5時間パック":
        conditions[4] = "14"
    elif conditions[4] == "昼3時間パック":
        conditions[4] = "12"
    for key,value in facility_dict.items():
        urls[key] = "https://jankara.me/reservation/custom/user/getReservationFormDisp?reservationType=1&facilityId="+value+"&targetDate="+conditions[0]+"&overDay=0&startHours="+conditions[1]+"&useNumber="+conditions[2]+"&useDate="+conditions[0]+"+"+conditions[1]+"&useTime="+conditions[3]+"&courseId="+conditions[4]+"&reReservationRoom=0&reReservationMachine=0&gaReservationType=0&gaCalendarViaType=1&searchId=65129198"
def get_info(conditions_row):
    global machine_list
    get_urls(conditions_row)
    room_list = {}
    all_room_list = []
    key_list = ["店名","JOYSOUND MAX GO","JOYSOUND MAX2","JOYSOUND MAX","LIVE DAM STADIUM","LIVE DAM Ai"]
    cnt = 0
    for key,url in urls.items():
        room_list["店名"] = key
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        time.sleep(1.0)
        for value,machine_name in [['input[value="10"]',"JOYSOUND MAX GO"],['input[value="7"]',"JOYSOUND MAX2"],['input[value="2"]',"JOYSOUND MAX"],['input[value="6"]',"LIVE DAM STADIUM"],['input[value="9"]',"LIVE DAM Ai"]]:
            for tag in soup.select(value):
                left_room_num = tag.get("data-stock")
                if left_room_num == None:
                    continue
                room_list[machine_name] = left_room_num
        cnt=cnt+1
        #--- room_listの整形---
        for machine_name in machine_list:
            if not machine_name in room_list:
                room_list[machine_name] = "×"
            else:
                pass
        tmp_room_list = {}
        for value in key_list:
            tmp_room_list[value] = room_list[value]
        room_list = tmp_room_list
        copy_room_list = room_list.copy() #---room_listが毎回リセットされるのでコピーをもとにall_room_listを作成
        all_room_list.append(copy_room_list)
        room_list.clear()
    print(all_room_list)
    get_df(all_room_list)
    return all_room_list

def get_table(conditions_row,tree): #表に内容を記述
    global button_state
    # global now_status
    # now_status = "処理中"
    # status_label.update()
    # print(now_status)
    button_state = "disable"
    clear_table(tree) #古い表を削除
    #--- 不正な日時によるエラー処理 ---
    date_info = datetime.datetime(int(conditions_row[0].split("-")[0]),int(conditions_row[0].split("-")[1]),int(conditions_row[0].split("-")[2]),int(conditions_row[1].split(":")[0]),int(conditions_row[1].split(":")[1]),0)
    if date_info > datetime.datetime.now():
        all_room_list = get_info(conditions_row)
        for room_list in all_room_list:
            tree.insert(parent='', index='end' ,values=tuple(room_list.values()))
    else:
        messagebox.showerror("error","正しい日時を選択してください")
    # now_status = "完了"
    #---------------------------------

def mult_get_table(conditions_row,tree): #get_tableをマルチスレッドで処理するための関数
    thread = threading.Thread(target=get_table,args=(conditions_row,tree))
    thread.start()

def clear_table(tree):
    for item in tree.get_children():
        tree.delete(item)

def get_df(all_room_list):
    room_value_list = []
    for room_list in all_room_list:
        room_value_list.append(list(room_list.values()))
    transposed_list = [[row[i] for row in room_value_list] for i in range(6)]
    print(transposed_list)
    df = pd.DataFrame({
        "店舗名":transposed_list[0],
        "JOYSOUND MAX GO":transposed_list[1],
        "JOYSOUND MAX2":transposed_list[2],
        "JOYSOUND MAX":transposed_list[3],
        "LIVE DAM STADIUM":transposed_list[4],
        "LIVE DAM Ai":transposed_list[5],
    })
    now = datetime.datetime.now()
    file_name = "available_room"+now.strftime('%Y%m%d%H%M%S')+".html"
    file_path = "./results/"+file_name
    df.to_html(file_path,index=False)
    webbrowser.open("file:///C:/Users/hizih/OneDrive - Kansai University/デスクトップ/portfolio-main/flaskr/results/"+file_name, new=0, autoraise=True)


if __name__ == "__main__":
    main()
