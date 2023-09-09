from math import e
from NJUlogin import QRlogin
import sys
from bs4 import BeautifulSoup  # 借助BeautifulSoup包解析
import re
import json
import os
# 填入试卷的地址 注意 只到userScoreID, 其他不需要
url = "https://aqks.nju.edu.cn/PersonInfo/StartExamOne.aspx?PaperID=xxx&UserScoreID=xxxx"
# 填入cookie
cookie = "这里填入cookie"
num=100;


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
    'Cookie': cookie,
    'content-type': 'application/x-www-form-urlencoded',
}
question = {}
path = os.getcwd()+"\\ans.json"
print(path)
f = open(path, 'r', encoding='utf-8')
txt = open(os.getcwd()+"\\exam_ans.txt", "w")
question = json.load(f)

sys.path.append('.')
resultStr = ''
dest = "https://aqks.nju.edu.cn/xycms.aspx"
qrlogin = QRlogin()
session = qrlogin.login(dest)
for i in range(1, num+1):
    q_url = f'{url}&TestNum={i}'
    response=""
    try:
        response = session.get(q_url, headers=headers)
    except:
        print("cookie填写有误")
        exit(-1)
    soup = BeautifulSoup(response.text)
    # 构造id
    idStr = 'trTestTypeContent'+str(i)
    try:
        QuestionTable = soup.find_all('table', {'id': idStr})[0]
    except:
        print("cookie填写有误")
        exit(-1)
    column_data = []
    flag = 0
    table = QuestionTable.find_all('tr')
    print(table[0].find_all('td')[0].text)
    q = re.match(r"[0-9]+.(.*)（.*?分）",
                 table[0].find_all('td')[0].text).group(1).rstrip()
    a = ''
    if q not in question:
        a = "未知"
    else:
        a = question[q]
    print("题号", i, "答案", a, "问题", q)
    txt.write(f"{i}.{a}\n")
    # question[]
print('success!')
f.close()
txt.close()
