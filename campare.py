# coding=gbk

import string
import re
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup

# ��ȡ��ҳ�в�Ʒname��vaule

url = 'https://www.watchguard.com/wgrd-products/appliances-compare'

res = requests.get(url)                                         # ��������                   
res.raise_for_status()                                          # ����Ƿ����ӳɹ�
res.encoding = res.apparent_encoding                            # �������з���������Ӧ���뷽ʽ
soup = BeautifulSoup(res.text, 'html.parser')                   # �����ĵ�����������
#print(soup)
optGrp = soup.find_all('optgroup')                              # ��ȡ����optgroup
# print(type(optGrp))


productName = []                                                # ���������б��Ų�Ʒ���Ͷ�Ӧ����
productValue = []
for i in range(2):                                              # ��ȡǰ����optgroup�µ�option
    option = optGrp[i].find_all('option')
    # print(option)
    for y in option:                                            # ��һ��ȡoption�е���Ϣ
        info = y.get_text()
        obj = re.findall(r'WatchGuard.*Firebox.(.*)',info)      # ������ʽ��ȡ���ַ���������ݵõ���Ʒ����
      # print(obj[0])
        name = obj[0].replace(' ','')
      # print(name)
        value = y.attrs['value']                                # ��һ��ȡvalue���Ե���ֵ
        productName.append(name)
        productValue.append(value)        
# print(productName)
# print(productValue)


dic = dict(zip(productName, productValue))                      # ���������б�����һ��Ԫ�鲢ת��Ϊ�ֵ�
print(dic)


# ��ȡpefermance�е����ݲ�����

compareGrp = random.sample(productName,3)                       # ����Ӳ�Ʒ�����б��������������
print(compareGrp)


c_url = 'https://www.watchguard.com/wgrd-products/appliances-compare/' + dic[compareGrp[0]] + '/' + dic[compareGrp[1]] + '/' + dic[compareGrp[2]]
print(c_url)
c_res = requests.get(c_url)                       
c_res.raise_for_status()      
c_res.encoding = c_res.apparent_encoding
soup = BeautifulSoup(c_res.text, 'html.parser') 


c_tr = soup.find_all('tr')                                       # ��ȡ����tr
all_table = []
for tr in c_tr:
    ui = []
    for td in tr:                                                # ��һ��tr�л�ȡtd
        ui.append(td.string)                                     # ��ui�б�ĩβ����¶���
    all_table.append(ui)
# print(all_table)


performance = []                                                 # ����performance�б����ڱ�����ҳ����е�����
for i in range(len(all_table)):
    for j in range(len(all_table[i])):
        if all_table[i][j] == 'Performance':                     # ��all_table��Ƕ���б���Ѱ�ҵ�performance�ؼ��֣�����ȡ֮��6������
            for x in range(1, 7):
                s = ''.join(all_table[i + x])                    # ת�����ַ���
                z = s.strip('\n').split('\n')                    # ͨ�����з���Ƭ���Ƴ��ַ���ͷβ�Ļ����ַ�
                performance.append(z)
            break
# print(len(performance[1]))
# print(performance)


data = pd.DataFrame(performance)                                 # ����Pandasģ���е����ݽṹ��������һ�����
print(data)
data.set_index([0], inplace=True)                                # ȥ�������һ��ָ��
data = data.T                                                    # �����������ת��
data['Products'] = compareGrp
data.set_index('Products', inplace=True)                         # ��ת�ú��һ���滻Ϊ��Ʒ���ƣ�����Firewall Throughput�е���������
data = data.sort_values(by='Firewall Throughput ', axis=0, ascending=True)                 
print(data)


data.to_csv('performance_result.csv')                            # �����ļ���.csv



