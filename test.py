from NJUlogin import QRlogin
import sys
from bs4 import BeautifulSoup  # 借助BeautifulSoup包解析
import re
import json
# 填入试卷的地址
url = "https://aqks.nju.edu.cn/PersonInfo/StartExamOne.aspx?PaperID=181&UserScoreID=181229"
# 填入cookie
cookie = "_ga=GA1.1.856900051.1655542278; _ga_J3YE5G7DJT=GS1.1.1677420313.1.1.1677420480.0.0.0; USER_COOKIE=UserName=211870187&UserPassword=; ASP.NET_SessionId=yaotkmvdpbn1sbxiloglbr0l; iPlanetDirectoryPro=bfcZclnajdD7NgecZgumcU; MOD_AUTH_CAS=MOD_AUTH_ST-4099384-21uKjPta2ep6HfbCAVYb1683879523185-0Mqp-cas"


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
    'Cookie': cookie,
    'content-type': 'application/x-www-form-urlencoded',
}
question = {}
path = r"C:\Users\mikumifa\Downloads\Data\ans.json"
f = open(path, 'r', encoding='utf-8')
question = json.load(f)

sys.path.append('.')
resultStr = ''
dest = "https://aqks.nju.edu.cn/xycms.aspx"
qrlogin = QRlogin()
session = qrlogin.login(dest)
for i in range(1, 100):
    q_url = f'{url}&TestNum={i}'
    response = session.get(q_url, headers=headers)
    soup = BeautifulSoup(response.text)
    # 构造id
    idStr = 'trTestTypeContent'+str(i)
    QuestionTable = soup.find_all('table', {'id': idStr})[0]
    column_data = []
    flag = 0
    table = QuestionTable.find_all('tr')
    print(table[0].find_all('td')[0].text)
    q = re.match(r"[0-9]+.(.*)（1分）",
                 table[0].find_all('td')[0].text).group(1)
    a = question.get(q, "未知")
    print("题号", i, "答案", a, "问题", q)
    # question[]
print('success!')
f.close()
