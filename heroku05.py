# 部署到雲端server
from flask import Flask, render_template,request

import urllib.request as req
import json
import pandas as pd
import EricFunc

app = Flask(__name__)

@app.route("/")
def home():
    return """<h1>Eric Lu 20 天</h1>
<p>全身都是肌肉沒半點腦子。反正，那就是鄭尼那晚照顧的草泥馬。我完全無法了解，我發誓我沒辦法。</p>
"""

# 練習1: 回傳值到HTML
@app.route("/try")
def try1():
    src = "https://data.taipei/api/v1/dataset/36847f3f-deff-4183-a5bb-800737591de5?scope=resourceAquire"
    with req.urlopen(src) as response:
         data = json.load(response)
        
    clist = data["result"]["results"]
    print(clist[1]["stitle"])

    return render_template("listall.html", myclist=clist)

# # # 練習2:
@app.route("/search")
def search1():
    src = "https://data.taipei/api/v1/dataset/36847f3f-deff-4183-a5bb-800737591de5?scope=resourceAquire"
    with req.urlopen(src) as response:
         data = pd.read_json(response)
        
    clist = data["result"]["results"]
    # 轉成dataFrame格式,尋找特定字串
    xclist = pd.DataFrame(clist)
    condition = xclist["MRT"] == "中山"
    filtdata =  xclist[condition]
    
    # 把dataFrame資料轉換格式(dataFrame格式無法秀在網頁上)
    n1 = filtdata.shape[0]
    titlelist = filtdata.columns.values
    clist = clist[0:n1]
    i = 0
    while i < n1:
        for j in titlelist:
            clist[i][j] = filtdata[j].values[i]
        i = i + 1

    print(filtdata.values)
    return render_template("listall.html", myclist=clist)

    #return filtdata.to_html(header="true",table_id="table")

# # 練習3：建立一個搜尋網頁 find1:完全符合 , find2：關鍵字搜尋
@app.route('/find1',methods=['POST','GET'])
def getdata():
    return render_template('find1.html')

@app.route('/find2',methods=['POST','GET'])
def getdata2():
    return render_template('find2.html')

# #練習4: 整合進去搜尋網頁
@app.route('/mysearch1', methods=['POST'])
def submit():
    findword = request.form.get('username')
    clist = EricFunc.ericsearch(findword)
    return render_template("listall.html", myclist=clist)

# @app.route('/mysearch2', methods=['POST'])
def submit2():
    findword = request.form.get('username')
    clist = EricFunc.erickeyword(findword)
    return render_template("listall.html", myclist=clist)

# # # 練習5: 利用bootstrape 的CSS美化頁面
@app.route('/mysearch3', methods=['POST','GET'])
def submit3():
    findword = request.form.get('city_name')
    print(findword)
    if findword == None :
        findword = '台北'

    clist = EricFunc.erickeyword(findword)
    return render_template("find3.html",myclist = clist)



if __name__ == "__main__":
    app.run()








# 第一次上傳到 heroku 
# heroku login 
# git init
# heroku git:remote -a eatrol-heroku01
# git add.
# git commit -m "1st upload, YA"
# git push heroku master

# 第二次以後 
# git add.
# git commit -m "2nd change,test"
# git push heroku master