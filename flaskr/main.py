from flaskr import app
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import webbrowser
import time
import datetime
import requests
from bs4 import BeautifulSoup
import os

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

def create_facility_dict(*args): #チェックボックスから店舗の辞書を生成（get_urls()に渡すため）
    global facility_dict,umeda,takatsuki,kyobashi,nanba_shinsaibashi,kyoto
    facility_dict.clear() #初期化
    if args[0] == "True":
        facility_dict.update(umeda)
    if args[1] == "True":
        facility_dict.update(takatsuki)
    if args[2] == "True":
        facility_dict.update(kyobashi)
    if args[3] == "True":
        facility_dict.update(nanba_shinsaibashi)
    if args[4] == "True":
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
    get_df(all_room_list)
    return all_room_list

def get_table(conditions_row): #表に内容を記述
    if date_info > datetime.datetime.now():
        all_room_list = get_info(conditions_row)

def mult_get_table(conditions_row): #get_tableをマルチスレッドで処理するための関数
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
    file_path = "./templates/"+file_name
    df.to_html(file_path,index=False)
    file_path = "./flaskr/templates/"+file_name
    df.to_html(file_path,index=False)
    # webbrowser.open("file:///C:/Users/hizih/OneDrive - Kansai University/デスクトップ/portfolio-main/flaskr/results/"+file_name, new=0, autoraise=True)

def apply_condition(input_list, condition_values):
    result = [False] * len(input_list)

    for value in condition_values:
        if value in input_list:
            result[input_list.index(value)] = True

    return result


@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/process_form', methods=['POST'])
def process_form():
    if request.method == 'POST':
        # チェックボックスとプルダウンの値を取得
        var_umeda = request.form.get('region1')
        var_takatsuki = request.form.get('region2')
        var_kyobashi = request.form.get('region3')
        var_nanba_shinsaibashi = request.form.get('region4')
        var_kyoto = request.form.get('region5')
        hour = request.form.get('hour')
        minute = request.form.get('minute')
        use_number = request.form.get('use_number')
        use_minute = request.form.get('use_minute')
        course = request.form.get('course')
        calender_date = request.form.get('selected_date')

        create_facility_dict(var_umeda,var_takatsuki,var_kyobashi,var_nanba_shinsaibashi,var_kyoto)
        get_info([calender_date,hour+":"+minute,use_number,use_minute,course])
    return redirect(url_for('html_file'))

@app.route('/html_file')
def html_file():
    # フォルダ内のHTMLファイルを表示
    folder_path = 'templates'  # HTMLファイルが格納されているフォルダのパス
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    
    if html_files:
        # 例として最初のHTMLファイルを表示
        return render_template(html_files[-1])

    # HTMLファイルが存在しない場合の処理
    return 'No HTML files found in the templates folder.'

# @app.route('/get_date', methods=['POST'])
# def get_date():
#     selected_date = request.form['selected_date']
#     # 選択された日付を使用して何かを行うことができます
#     return f'Selected date: {selected_date}'