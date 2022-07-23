import pandas as pd
from flask import Flask,request,render_template,redirect,url_for
from flask import session as se
import json

def zhiyuantianbao(paiming,xuanke):   #以后详细改善
    file='shandong.csv'
    data=pd.read_csv(file,encoding='utf-8')
    data = data[['院校代码', '院校名称', '专业名称', '选考科目', '最低分', '最低分位次']]
    xuanke1=xuanke
    data1=[]
    data=data[abs(data.最低分位次 - int(paiming)) <= 1000]
    for row in data.itertuples():
        if '和' in row[4]:
            str1=str(row[4])
            b=str1.split('和')
            if b in xuanke1:
                data1.append(row)
        elif '或' in row[4]:
            str1=str(row[4])
            b=str1.split('或')
            for i in b:
                if i in xuanke1:
                    data1.append(row)
                    break
        else:
            if row[4]=='不限':
                data1.append(row)
            else:
                str1=str(row[4])
                if str1 in xuanke1:
                    data1.append(row)
    data1=pd.DataFrame(data1)
    html_index=data1.to_html()
    return html_index

def daxuechaxun(daxue):
    file = 'shandong.csv'
    data = pd.read_csv(file, encoding='utf-8')
    data = data[['院校代码', '院校名称', '专业名称', '选考科目', '最低分', '最低分位次','招生人数']]
    # data=data[daxue == data['院校名称']]  keyerror=true?不知道怎么改
    data1=[]
    for row in data.itertuples():
        if str(daxue) in row[2]:
            data1.append(row)
    data1=pd.DataFrame(data1)
    html_index=data1.to_html()
    return html_index

def zhuanyechaxun(major,paiming):
    file = 'shandong.csv'
    data = pd.read_csv(file, encoding='utf-8')
    data = data[['院校代码', '院校名称', '专业名称', '选考科目', '最低分', '最低分位次', '招生人数']]
    data=data[abs(data.最低分位次 - int(paiming)) <= 10000]
    data1 = []
    for row in data.itertuples():
        if str(major) in row[3]:
            data1.append(row)
    data1 = pd.DataFrame(data1)
    html_index = data1.to_html()
    return html_index

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
@app.route('/',methods=['GET','POST'])
def zuoye():
     if request.method=='GET':
         return render_template('zhiyuantianbao.html')
     elif request.method=='POST':
        rank=request.form.get('rank')

        list=["物理","化学","生物","政治","历史","地理"]
        subjects = []
        for i in list:
            if request.form.get(i):
                subjects.append(i)
        return zhiyuantianbao(rank,subjects)

@app.route('/daxuechaxun',methods=['GET','POST'])
def zuoye1():
    if request.method=='GET':
        return render_template('daxuechaxun.html')
    elif request.method=='POST':
        daxue=request.form.get('daxue')
        return daxuechaxun(daxue=daxue)

@app.route('/zhuanyechaxun',methods=['GET','post'])
def zuoye2():
    if request.method=='GET':
        return render_template('zhuanyechaxun.html')
    elif request.method=='POST':
        major=request.form.get('major')
        rank=request.form.get('rank')
        return zhuanyechaxun(major,rank)

@app.route('/dituzhanshi',methods=['GET','POST'])
def zuoye3():
    return render_template('dituzhanshi.html')

@app.route('/dituzhanshi2',methods=['GET','POST'])
def zuoye4():
    return render_template('dituzhanshi2.html')


if __name__ == '__main__':
    app.run(debug=True)





