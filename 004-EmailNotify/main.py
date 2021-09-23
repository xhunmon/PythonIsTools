#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 玩客家 币价变化，邮件通知 api
@Date       :2020/12/17
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import json
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from my_fake_useragent import UserAgent

ua = UserAgent()
agent = ua.random()


class Email(object):
    def __init__(self, from_user, pwd, to_other):
        """
        :param from_user: 发送者邮箱号
        :param pwd:       发送者邮箱密码（非登录密码）
        :param to_other:  目标邮箱
        """
        self.__from_user = from_user
        self.__pwd = pwd
        self.__to_other = to_other

    def sendMsg(self, title="", content=""):
        print("%s向%s发送邮件：标题{%s}\t内容{%s}" % (self.__from_user, self.__to_other, title, content))
        retry = 0
        while True:
            print("【%s】开始发送，次数：%3d" % (title, retry))
            try:
                msg = MIMEMultipart()
                msg.attach(MIMEText(content, 'plain', 'utf-8'))
                msg['Subject'] = title
                msg['From'] = self.__from_user
                s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 通过SSL方式发送，服务器地址和端口
                s.login(self.__from_user, self.__pwd)  # 登录邮箱
                s.sendmail(self.__from_user, self.__to_other, msg.as_string())  # 开始发送
                print("邮件发送成功，发送时间【%s】" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
                break
            except Exception as e:
                print(
                    "邮件发送失败，5秒钟后重新发送，发送时间【%s】" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
                print(e)
                retry += 1
                time.sleep(5)


class Coin(object):
    def __init__(self, coin="", diff=3.0, sleep=3, reload=1 * 60 * 60, email: Email = None):
        self.__COIN = coin  # 币名称
        self.__DIFF = diff  # 当trend的值幅度差为该设定值，邮箱进行通知
        self.__SLEEP_TIME = sleep  # 每次获取的睡眠时间
        self.__RELOAD_TIME = reload  # 每小时重复更新一次页面
        self.__email = email
        self.__RINGE_COUNT = int(self.__RELOAD_TIME / self.__SLEEP_TIME)
        self.__is_release = False
        self.__last_price = 0.0
        self.__last_time = 0
        self.__last_trend = 0.0
        self.__is_first = True
        self.__URL = "https://app.wkj.pub/api/market/getMarketTradeJson"  # 请求地址
        self.__DATA = 'market=%s_bitcny&sellnum=10&buynum=10&donenum=10' % coin.lower()
        self.__headers = {"user-agent": agent}

    def start(self):
        print("thread【%2s diff is %2s , sleep is %2d ,retry time is %5ld】" % (
            self.__COIN, str(self.__DIFF), self.__SLEEP_TIME, self.__RELOAD_TIME))
        while True:
            try:
                time.sleep(self.__SLEEP_TIME)
                if self.__is_release:
                    print("%2s 已释放，退出！" % self.__COIN)
                    break
                req = requests.post(self.__URL, data=self.__DATA, headers=self.__headers)
                if req.status_code != 200:
                    print("%2s 请求失败-%s" % (self.__COIN, req.status_code))
                    continue
                data = json.loads(req.text)
                # print(req.text)
                price = float(data.get("data").get("new_price"))  # 当前价格
                trend = float(data.get("data").get("change"))  # 跌涨幅 趋势
                num = float(data.get("data").get("doneOrders")[0].get("num"))  # 当前成交价
                done_time = int(data.get("data").get("doneOrders")[0].get("time"))  # 当前成交价
                done_type = int(data.get("data").get("doneOrders")[0].get("type"))  # 当前状态（1-buy，2-sell）
                if price <= 0:
                    print("%2s 价格为0，没有获取到数据，跳过" % self.__COIN)
                    continue
                if done_time == self.__last_time:  # 没有最新成交的单
                    print("【%2s …………】" % self.__COIN)
                    continue
                status = "buy" if done_type == 1 else "sell"
                print("【%2s \t| %2s \t| %5s \t| %2s％ \t| %2s】" % (
                    self.__COIN, status, str(price), trend, str(num)))
                self.__last_price = price
                self.__last_time = done_time
                if self.__is_first:  # 第一次启动就不必了
                    self.__is_first = False
                    self.__last_trend = trend
                    print("【%2s __is_first】" % self.__COIN)
                    continue
                temp_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                if self.__last_trend - trend > self.__DIFF:  # 跌了
                    self.__last_trend = trend
                    self.__email.sendMsg(
                        "【%2s跌:%s | %s％】" % (self.__COIN, str(self.__last_price), str(trend)),
                        str("【价格：%s，跌幅：%s％，时间：%s】" % (
                            str(self.__last_price), str(trend), temp_time)))
                elif trend - self.__last_trend > self.__DIFF:  # 涨了
                    self.__last_trend = trend
                    self.__email.sendMsg(
                        "【%2s涨:%s | %s％】" % (self.__COIN, str(self.__last_price), str(trend)),
                        str("【价格：%s，涨幅：%s％，时间：%s】" % (
                            str(self.__last_price), str(trend), temp_time)))
            except Exception as e:
                print("wkj api【%2s】异常，5秒钟后重试!" % self.__COIN)
                print(e)
                time.sleep(5)
        print("【%2s 结束了】" % self.__COIN)


if __name__ == "__main__":
    email = Email(from_user="aaa@qq.com", pwd="bbb", to_other='ccc@qq.com')
    eth = Coin(coin="ETH", diff=2, sleep=5, reload=2 * 60 * 60, email=email)
    eth.start()