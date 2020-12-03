#!/usr/bin/env python
# encoding: utf-8
# @Author   : Xingyu Zhao
# @Software : Pycharm
# @File     : status_query.py
# @Time     : 2020/12/3 15:28
# @Desc     : Contribution status query



import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time



def main(num_id: str, num_password: str):
    chrome_options = Options()

    chrome_options.add_argument('--headless')

    #输入chrome_driver的绝对路径
    chrome_driver = "xxx"

    browser = webdriver.Chrome(executable_path=chrome_driver,chrome_options=chrome_options)

    browser.get('https://mc.manuscriptcentral.com/twc')

    time.sleep(2)

    element = browser.find_element_by_xpath("//div/fieldset/div[2]/input[@id='USERID']")

    # 输入用户名
    element.send_keys(num_id)

    #输入密码
    element = browser.find_element_by_xpath("//input[@id='PASSWORD']")

    element.send_keys(num_password)

    element = browser.find_element_by_xpath("//a[@id='logInButton']")

    element.click()

    time.sleep(2)

    element = browser.find_element_by_xpath("//li[@class='nav-link '][1]/a")

    element.click()

    time.sleep(2)

    result = browser.find_element_by_xpath("//td[1]/table/tbody/tr/td[2]").text

    tittle = browser.find_element_by_xpath("//td[3]").text

    tittle = tittle[:tittle.find("\n")]

    sub_date = browser.find_element_by_xpath("//td[@class='whitespace-nowrap'][2]").text

    day1 = time.strptime(sub_date, "%d-%b-%Y")

    tmp = time.strftime('%Y %m %d', time.localtime(time.time()))

    day2 = time.strptime(tmp, "%Y %m %d")

    deta = str(int((int(time.mktime(day2)) - int(time.mktime(day1))) / (24 * 60 * 60)))


    browser.close()

    # 发送者的登陆用户名和密码
    sender = 'xxx'
    password = 'xxx'
    # 发送者邮箱的SMTP服务器地址
    smtpserver = 'xxx'
    # 接收者的邮箱地址
    receiver = 'xxx'

    content = "尊敬的星宇霸霸：\n 您的论文：{} \n \t\t目前状态是：{}，投稿日期为：{}，目前耗时：{}天。".format(tittle,result,sub_date,deta)
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver
    send_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    subject = '您的论文查询结果  ' + send_time
    msg['Subject'] = subject

    smtp = smtplib.SMTP()  # 实例化SMTP对象
    smtp.connect(smtpserver, 25)  # （缺省）默认端口是25 也可以根据服务器进行设定
    smtp.login(sender, password)  # 登陆smtp服务器
    smtp.sendmail(sender, [receiver], msg.as_string())  # 发送邮件 ，这里有三个参数
    '''
    login()方法用来登录SMTP服务器，sendmail()方法就是发邮件，由于可以一次发给多个人，所以传入一个list，邮件正文
    是一个str，as_string()把MIMEText对象变成str。
    '''
    smtp.quit()

    return True

if __name__ == '__main__':
    dic = {'xxx': 'xxx'}
    for i in dic:
        result = main(i, dic[i])
        print(result)