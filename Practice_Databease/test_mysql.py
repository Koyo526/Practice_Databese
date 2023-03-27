import mysql.connector    #mysql-connector-python のインストールが必要　最新バージョンは8.0.25
import pandas as pd       #pandas のインストールが必要　最新バージョンは1.2.4
import sqlalchemy as sqa  #SQLAlchemy のインストールが必要　最新バージョンは 1.4.20
 
# コネクションの作成
conn = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',#ここは最初に設定したユーザー名にして下さい（デフォルトだと「root」）
    password='root',#ここは最初に設定したパスワードにして下さい（MySQLを起動するときに求められるパスワード）
    database='test_db'#ここは使用するデータベースの名前を入れて下さい
)

# カーソルを取得する
cur = conn.cursor()
df=pd.read_csv("data/Student-Timetable.csv")
#ここのurlは各自異なるので確認が必要
#'mysql+pymysql://ここにユーザー名（デフォルトだとroot）:ここにパスワード@localhost/ここに使用するデータベース名'
#例：
# user='root'
# password='pass'
# database='test_db'
#の時のurlは以下の通り
# url = 'mysql+pymysql://root:satoken.com@localhost/test_db'
url = 'mysql+pymysql://:@localhost/'


#ここから下のプログラムは特に触らなくても大丈夫！！

#プログラム実行した後に,27個のテーブルができていればOK
#それぞれのテーブルの説明は説明用.wordに記載してます！

engine = sqa.create_engine(url, echo=True)
df.to_sql("Student_timetable", url, index=None)
week_lessons=['M1','M2','M3','M4','T2','T3_1','T3_2','T4','T5','W12','W3_1','W3_2','W4','W5_1','W5_2','Th2','Th34','Th5_1','Th5_2','F1','F2','F3','F4_1','F4_2']
for w in week_lessons:
    lesson="database/"+w+".csv"
    lesson_student=pd.read_csv(lesson)
    print(lesson_student)
    name=w
    lesson_student.to_sql(name, url, index=None)
data=pd.read_csv("data/学生リスト.csv")
data =data.drop("ふりがな", axis=1)
data["パスワード"]=data["学籍番号"]
data.to_sql("student_users", url, index=None)

data1=pd.read_csv("data/Lecture-Rules.csv")
drop_list=["開始時間","終了時間","出席限度(分)","遅刻限度(分)","試験","履修者数","曜日","受付時間","出席時間","遅刻時間"]
for dl in drop_list:
    data1=data1.drop(dl,axis=1)
data1["パスワード"]=data1["ID"]
data1.to_sql("teacher_users",url,index=None)
cur.close
conn.close