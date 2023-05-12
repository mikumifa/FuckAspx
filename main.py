from NJUlogin import QRlogin
import sys
from bs4 import BeautifulSoup  # 借助BeautifulSoup包解析
import re
import json
import os
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
    'Cookie': '_ga=GA1.3.1256847576.1601191563; ASP.NET_SessionId=ixi0wac51sgxmbdi4m4pv2fu; iPlanetDirectoryPro=ZbN712VGOA30elEnQByPYg',
    'content-type': 'application/x-www-form-urlencoded',
}
url = "https://aqks.nju.edu.cn/PersonInfo/StartExercise.aspx"
sys.path.append('.')
resultStr = ''
dest = url
qrlogin = QRlogin()
session = qrlogin.login(dest)
question = {}
path = os.getcwd()+'\\ans.json'
print(path)
txt_path = os.getcwd()+"\\ans.txt"
f = open(path, 'w', encoding='utf-8')
txt = open(txt_path, 'w', encoding='utf-8')

for i in range(1, 9999):
    q_url = f'https://aqks.nju.edu.cn/PersonInfo/StartExercise.aspx?TestNum={i}'
    response = qrlogin.get(q_url)
    soup = BeautifulSoup(response.text)
    # 构造id
    idStr = 'trTestTypeContent1'
    QuestionTable = soup.find_all('table', {'id': idStr})[0]
    column_data = []
    flag = 0
    for row in QuestionTable.find_all('tr'):
        tds = row.find_all('td')
        if len(tds) == 0:
            flag = 1
            break
        column_data.append(tds[-1].text)
    if flag == 1:
        break
    q = re.match(r"[0-9]+.(.*)共 [0-9]+ 题", column_data[0]).group(1).rstrip()
    a = re.match(r"参考答案：(.*)", column_data[-3]).group(1)
    print(i, "finished")
    txt.write(f"{q} {a}\n")
    if q not in question:
        question[q] = a
    else:
        print("有重复在", i, '个题目')

    # question[]
print('success!')
json.dump(question, f, ensure_ascii=False)
f.close()
txt.close()
