# coding: utf-8

import requests
from pyquery import PyQuery as pq
import pandas as pd
from email.mime.text import MIMEText
from smtplib import SMTP
import configparser 
import smtplib
import sys

def run_crawler():
    # page_source = requests.get("https://rate.bot.com.tw/xrt?Lang=zh-TW")

    # doc = pq(page_source.text)('tbody')
    # for currency in doc('tr').items():
    #     print(currency('.visible-phone').text(), end =',')
    #     print(currency('.rate-content-cash').eq(1).text())



    history_page_source = requests.get("https://rate.bot.com.tw/xrt/quote/l6m/AUD")
    doc2 = pq(history_page_source.text)
    AUD_dict = {}
    for currency in doc2('tr').items():
        AUD_dict[currency('.text-center').eq(0).text()] = currency('.rate-content-cash').eq(1).text()
        #print(currency('.text-center').eq(0).text(), end = ',')
        #print(currency('.rate-content-cash').eq(1).text())

    AUD_df = pd.DataFrame(list(AUD_dict.items()), columns=['Date', 'DateValue'])
    AUD_df = AUD_df.drop(AUD_df.index[0])
    AUD_df['DateValue'] = AUD_df['DateValue'].astype('float64')

    return AUD_df

def send_email(AUD_df):

    config = configparser.ConfigParser()
    config.read('config.ini')

    sender = config['email']['account']
    passwd = config['email']['passwd']
    receiver = config['email']['receiver']

    msg = MIMEText("""<tr>
                    <td>澳幣本日現金賣出匯率</td>
                    <td>{}</td>
                    </tr>
                    <tr>
                    <td>澳幣半年內最高匯率</td>
                    <td>{}</td>
                    </tr>
                    <tr>
                    <td>澳幣半年內最低匯率</td>
                    <td>{}</td>
                    </tr>
                    <tr>
                    <td>澳幣半年內匯率第一四分位率</td>
                    <td>{}</td>
                    </tr>
                    <tr>
                    <td>澳幣半年內匯率中位數</td>
                    <td>{}</td>
                    </tr>
                    <tr>
                    <td>澳幣半年內匯率第三四分位率</td>
                    <td>{}</td>
                    </tr>
                    <tr>
                    <td>半年內詳細資料</td>
                    <td>{}</td>
                    </tr>
                    """.format(AUD_df['DateValue'].iloc[0], AUD_df['DateValue'].max(), AUD_df['DateValue'].min(), AUD_df['DateValue'].quantile(.25), AUD_df['DateValue'].quantile(.5), AUD_df['DateValue'].quantile(.75), 'https://rate.bot.com.tw/xrt/quote/l6m/AUD') , 'html')

    msg['Subject'] = "AUD exchange rate < 22.0 "
    msg['From'] = sender
    msg['To'] = receiver
    
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    smtp.ehlo() 
    smtp.login(sender, passwd)
    
    smtp.send_message(msg)
    smtp.close()

if __name__ == '__main__':
    AUD_df = run_crawler()
    # 澳幣低於 22.00 元 通知
    if AUD_df['DateValue'].iloc[0] < 22.00:
        print('寄出信件!')
        send_email(AUD_df)