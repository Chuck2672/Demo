# coding=gbk

import string
import re
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 爬取网页中产品name及vaule

url = 'https://www.watchguard.com/wgrd-products/appliances-compare'

res = requests.get(url)                                         # 请求网络                   
res.raise_for_status()                                          # 检查是否连接成功
res.encoding = res.apparent_encoding                            # 从内容中分析出的响应编码方式
soup = BeautifulSoup(res.text, 'html.parser')                   # 遍历文档树，并解析
#print(soup)
optGrp = soup.find_all('optgroup')                              # 获取所有optgroup
# print(type(optGrp))


productName = []                                                # 创建两个列表存放产品名和对应数据
productValue = []
for i in range(2):                                              # 获取前两个optgroup下的option
    option = optGrp[i].find_all('option')
    # print(option)
    for y in option:                                            # 逐一获取option中的信息
        info = y.get_text()
        obj = re.findall(r'WatchGuard.*Firebox.(.*)',info)      # 正则表达式获取该字符串后的数据得到产品名称
      # print(obj[0])
        name = obj[0].replace(' ','')
      # print(name)
        value = y.attrs['value']                                # 逐一获取value属性的数值
        productName.append(name)
        productValue.append(value)        
# print(productName)
# print(productValue)


dic = dict(zip(productName, productValue))                      # 将这两个列表打包成一个元组并转换为字典
print(dic)


# 爬取pefermance中的数据并保存

compareGrp = random.sample(productName,3)                       # 随机从产品名称列表中随机三个对象
print(compareGrp)


c_url = 'https://www.watchguard.com/wgrd-products/appliances-compare/' + dic[compareGrp[0]] + '/' + dic[compareGrp[1]] + '/' + dic[compareGrp[2]]
print(c_url)
c_res = requests.get(c_url)                       
c_res.raise_for_status()      
c_res.encoding = c_res.apparent_encoding
soup = BeautifulSoup(c_res.text, 'html.parser') 


c_tr = soup.find_all('tr')                                       # 获取所有tr
all_table = []
for tr in c_tr:
    ui = []
    for td in tr:                                                # 逐一在tr中获取td
        ui.append(td.string)                                     # 在ui列表末尾添加新对象
    all_table.append(ui)
# print(all_table)


performance = []                                                 # 创建performance列表用于保存网页表格中的内容
for i in range(len(all_table)):
    for j in range(len(all_table[i])):
        if all_table[i][j] == 'Performance':                     # 在all_table的嵌套列表中寻找到performance关键字，并获取之后6行内容
            for x in range(1, 7):
                s = ''.join(all_table[i + x])                    # 转换成字符串
                z = s.strip('\n').split('\n')                    # 通过换行符切片再移除字符串头尾的换行字符
                performance.append(z)
            break
# print(len(performance[1]))
# print(performance)


data = pd.DataFrame(performance)                                 # 调用Pandas模块中的数据结构函数生成一个表格
print(data)
data.set_index([0], inplace=True)                                # 去掉矩阵第一列指针
data = data.T                                                    # 将矩阵的行列转置
data['Products'] = compareGrp
data.set_index('Products', inplace=True)                         # 将转置后第一列替换为产品名称，并以Firewall Throughput列的内容排序
data = data.sort_values(by='Firewall Throughput ', axis=0, ascending=True)                 
print(data)


data.to_csv('performance_result.csv')                            # 保存文件称.csv



