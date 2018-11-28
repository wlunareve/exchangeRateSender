
# coding: utf-8

# In[40]:


import requests
import re
from pyquery import PyQuery as pq

page_source = requests.get("https://rate.bot.com.tw/xrt?Lang=zh-TW")

doc = pq(page_source.text)('tbody')

#for currency in doc('tr').items():
    #print(currency('.visible-phone').text(), end =',')
    #print(currency('.rate-content-cash').eq(1).text())

currencies = [ i.text() for i in doc('tr').items('div.visible-phone')]
print(currencies)

currencies_eng = [''.join(re.split(r'[^A-Za-z]',j)) for j in currencies]

print(currencies_eng) 
#df_to_html_table(currency('.visible-phone').text(), currency('.rate-content-cash').eq(1).text())


# In[108]:


import pandas as pd
import time

statistical_data = []
currencies_eng = {'JPY': '日幣', 'CNY': '人民幣', 'HKD': '港幣', 'USD': '美金', 'EUR': '歐元', 'GBP': '英鎊', 'AUD': '澳幣', 'SGD': '新加坡幣', 'KRW': '韓元'}

for currency_eng_value in currencies_eng:
    url = 'https://rate.bot.com.tw/xrt/quote/l6m/{}'.format(currency_eng_value)
    print(url)
    history_page_source = requests.get(url)
    doc2 = pq(history_page_source.text)
    currency_dict = {}
    for currency in doc2('tr').items():
        currency_dict[currency('.text-center').eq(0).text()] = currency('.rate-content-cash').eq(1).text()
        #print(currency('.text-center').eq(0).text(), end = ',')
        #print(currency('.rate-content-cash').eq(1).text())

    currency_df = pd.DataFrame(list(currency_dict.items()), columns=['Date', 'DateValue'])
    currency_df = currency_df.drop(currency_df.index[0])
    currency_df['DateValue'] = currency_df['DateValue'].astype('float64')

    currency_data = {}
    currency_data['{} 本日現金賣出匯率'.format(currencies_eng[currency_eng_value])] = currency_df['DateValue'].iloc[0]
    currency_data['{} 半年內最高匯率'.format(currencies_eng[currency_eng_value])] = currency_df['DateValue'].max()
    currency_data['{} 半年內最低匯率'.format(currencies_eng[currency_eng_value])] = currency_df['DateValue'].min()
    currency_data['{} 半年內匯率 10% 價格'.format(currencies_eng[currency_eng_value])] = currency_df['DateValue'].quantile(.1)
    currency_data['{} 半年內匯率中位數'.format(currencies_eng[currency_eng_value])] = currency_df['DateValue'].quantile(.5)
    currency_data['{} 半年內匯率 90% 價格'.format(currencies_eng[currency_eng_value])] = currency_df['DateValue'].quantile(.9)
    currency_data['{} 半年內詳細資料'.format(currencies_eng[currency_eng_value])] = url
    
    statistical_data.append(currency_data)

    time.sleep(5)
print(statistical_data)


# In[109]:


from email.mime.text import MIMEText
from smtplib import SMTP
from jinja2 import Template
import configparser 
import smtplib
import sys



def dict_to_html(statistical_data):
    
    html_list = []
    for currency_data in statistical_data:
        
        key_list = list(currency_data.keys())
        
        if  currency_data[key_list[0]] < currency_data[key_list[3]]:
            html_unit_list = ['<tr><td>{0}</td><td><strong>{1}</strong></td></tr><tr><td>{2}</td><td>{3}</td></tr>'.format(key_list[0], currency_data[key_list[0]], key_list[3], currency_data[key_list[3]])] 
            html_unit = ''.join(html_unit_list)
            html_list.append(html_unit)
        elif currency_data[key_list[0]] > currency_data[key_list[5]]:
            html_unit_list = ['<tr><td>{0}</td><td><strong>{1}</strong></td></tr><tr><td>{2}</td><td>{3}</td></tr>'.format(key_list[0], currency_data[key_list[0]], key_list[5], currency_data[key_list[5]])] 
            html_unit = ''.join(html_unit_list)
            html_list.append(html_unit)
    html = ''.join(html_list)
    return html
    
html = dict_to_html(statistical_data)
print(html)

config = configparser.ConfigParser()
config.read('config.ini')

sender = config['email']['account']
passwd = config['email']['passwd']
receiver = config['email']['receiver']
receiver = 'wlunareve@gmail.com'

msg = MIMEText(html, 'html')
msg['Subject'] = "Today exchange rate"
msg['From'] = sender
msg['To'] = receiver
  
smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)

smtp.ehlo() 
smtp.login(sender, passwd)
 
smtp.send_message(msg)

smtp.close()


