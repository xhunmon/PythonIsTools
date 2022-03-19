#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: tiktok app（版本：22.8.2）刷评论脚本
@Date       :2021/12/22
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import random
import time
from datetime import datetime

import file_util as futil

import uiautomator2 as u2

'''
https://github.com/openatx/uiautomator2
运行pip3 install -U uiautomator2 安装uiautomator2
运行python3 -m uiautomator2 init安装包含httprpc服务的apk到安卓手机
uiautomator2操作：https://python.iitter.com/other/35522.html
借助：weditor 来获取元素，双击找控件id
(注意电脑要把代理关掉)
'''

d = u2.connect()
print(d.info)
d.implicitly_wait(20)

comments = ['good job', 'good', 'look me', 'crazy', 'emm...', 'I wish you a happy new year',
            'May you be happy, lucky and happy.', 'I wish you a happy new year and good luck!',
            'to put people and life above everything else', 'heroes in harm’s way', 'spirited', ' behind wave',
            'mythical creatures', 'dagongren, which refers to people who work for others', 'involution',
            'Versailles literature', 'Look at my', 'Too good', 'To learn', 'learned', 'Thank you', 'I got it.',
            '666', 'nice', 'Well done', 'Look at my', 'Wonderful', 'Mine is not bad either.', 'Kudos', 'like u',
            'lean it', 'well...', '😊', 'My god!', 'Me too', 'I see', 'Come on', 'See you', 'Allow me', 'Have fun',
            'I\'m home', 'Bless you!', 'Follow me', 'Good luck!', 'Bottoms up!', 'Guess what?', 'Keep it up!',
            'Time is up', 'I like it!', 'That\'s neat', 'Let\'s face it.', 'Let\'s get started', 'Is that so',
            'That\'s something', 'Do you really mean it', 'Mind you', 'I am behind you', 'That depends',
            'What\'s up today?', 'Cut it out', 'What did you say', 'Knock it off', '[angel]', '[astonish]',
            '[awkward]', '[blink]', '[complacent]', '[cool]', '[cool][cute]', '[cool][cool]', '[cool][cool][cool]',
            '[cry]', '[cute]', '[cute][cute]', '[cute][cute][cute]', '[disdain]', '[drool]',
            '[embarrassed]', '[evil]', '[excited]', '[facewithrollingeyes]', '[flushed]', '[funnyface]', '[greedy]',
            '[happy]', '[hehe]', '[joyful]', '[laugh]', '[laughwithtears]', '[loveface]', '[lovely]', '[nap]',
            '[pride]', '[proud]', '[rage]', '[scream]', '[shock]', '[shout]', '[slap]', '[smile]', '[smileface]',
            '[speechless]', '[stun]', '[sulk]', '[surprised]', '[tears]', '[thinking]', '[weep]', '[wicked]',
            '[wow]', '[wronged]', '[yummy]',
            ' You kick ass.', ' You did a great job.', " You're a really strong person.", ' You read a lot.',
            ' That was impressive.', ' Your work on that project was incredible.', ' Keep up the good work!',
            " We're so proud of you.", ' How smart of you!', ' You have a real talent.',
            ' Well, a good teacher makes good student.', ' I would like to compliment you on your diligence.',
            " We're proud of you.", ' He has a long head.', ' You look great today.', " You're beautiful/gorgeous.",
            ' You look so healthy.', ' You look like a million dollars.', ' You have a good taste.',
            ' I am impressed.', ' You inspire me.', ' You are an amazing friend.', 'You are such a good friend.',
            ' You have a good sense of humor.', " You're really talented.", " You're so smart.",
            " You've got a great personality.", ' You are just perfect!', ' You are one of a kind.',
            ' You make me want to be a better person.', 'brb', 'g2g', 'AMA', 'dbd', 'this look great',
            'we’re so proud of you.', 'nice place.', 'nice going! ', 'emm...amazing!', 'ohh...unbelievable!',
            'yeh,impressive.', 'terrific..', 'fantastic!', 'fabulous.', 'attractive..', 'hei...splendid.',
            'ooh, remarkable', 'gorgeous', 'h.., glamorous', 'marvelous.', 'brilliant..', 'well...glorious',
            'outstanding...', 'stunning!', 'appealing.', 'yeh,impressive[cool]', 'terrific[angel]', 'fantastic[cool]',
            'fabulous[angel]', 'attractive[cool]', 'splendid[angel]', 'remarkable[cool]', 'gorgeous[angel]',
            'glamorous[angel]', 'marvelous[cool]', 'brilliant[angel]', 'glorious[cool]', 'outstanding[angel]',
            'stunning[cool]', 'appealing[angel]', 'Would you like me?[angel]', 'Do you like crafts?[angel]',
            'I have a new creative work, welcome![thinking]']

print('总共有{}条随机评论！'.format(len(comments)))


def start_vpn():  # 启动代理app
    d.press("home")
    # d.app_stop('com.v2ray.ang')
    d.app_start('com.v2ray.ang')
    if 'Not' in d(resourceId="com.v2ray.ang:id/tv_test_state").get_text():
        print_t('正在启动v2ray...')
        d(resourceId='com.v2ray.ang:id/fab').click()
    if 'Connected' in d(resourceId="com.v2ray.ang:id/tv_test_state").get_text():
        print_t('启动v2ray完成，正在测试速度...')
        d(resourceId='com.v2ray.ang:id/layout_test').click()
    while 'Testing' in d(resourceId="com.v2ray.ang:id/tv_test_state").get_text():
        time.sleep(1)
    print_t(d(resourceId="com.v2ray.ang:id/tv_test_state").get_text())


def review_forYou():
    # d.press("home")
    # d.app_start('com.zhiliaoapp.musically', stop=True)
    time.sleep(1)
    stop, index = random.randint(40, 70), 0
    while index < stop:  # 随机刷几十条
        cur_comment = comments[random.randint(0, len(comments) - 1)]
        print_t('foryou-总共有：{}条 | 现在到：{}条\t评论：{}'.format(stop, index, cur_comment))
        comment_foryou(cur_comment)
        try:
            time.sleep(random.randint(7, 35))  # 随机停顿1~5秒
            d.swipe_ext("up")  # 上划，下一个视频
        except Exception as e:
            print_t(e)
        index += 1


def review_tiktok():  # 评论
    keys = ['handmadecraft']  # '#homedecor #flowershower #handmadecraft'
    d.press("home")
    d.app_start('com.zhiliaoapp.musically', stop=False)
    time.sleep(1)
    try:
        d(text='Discover', className='android.widget.TextView').click()  # 点击发现
        time.sleep(1)
        d(resourceId="com.zhiliaoapp.musically:id/fbt").click()  # 点击搜索
    except Exception as e:
        print_t(e)
    for key in keys:
        # 不能搜索search
        try:
            d(resourceId="com.zhiliaoapp.musically:id/b15").clear_text()  # 清除历史
            d(resourceId="com.zhiliaoapp.musically:id/b15").set_text(key)  # 输入
            d(resourceId="com.zhiliaoapp.musically:id/fap").click()  # 点击搜索
            d(resourceId="android:id/text1", text="Videos").click()  # 点击视频，然后点击第一条
            d.xpath(
                '//*[@resource-id="com.zhiliaoapp.musically:id/cfh"]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]').click()
        except Exception as e:
            print_t(e)
        stop, index = random.randint(35, 60), 0
        while index < stop:  # 随机刷几十条
            cur_comment = comments[random.randint(0, len(comments) - 1)]
            print_t('{}-总共有：{}条 | 现在到：{}条\t评论：{}'.format(key, stop, index, cur_comment))
            comment(cur_comment)
            try:
                time.sleep(random.randint(5, 20))  # 随机停顿1~5秒
                d.swipe_ext("up")  # 上划，下一个视频
            except Exception as e:
                print_t(e)
            index += 1
        time.sleep(random.randint(int(0.5 * 60), 5 * 60))
        d(resourceId="com.zhiliaoapp.musically:id/t4").click()  # 返回搜索


def comment(content):
    try:
        time.sleep(random.randint(3, 10))  # 随机停顿1~5秒
        d(resourceId="com.zhiliaoapp.musically:id/acm").click()  # 点击评论按钮
    except Exception as e:
        print_t(e)
    try:
        time.sleep(random.randint(1, 3))  # 随机停顿1~2秒
        e_ele = d(text='Add comment...', className='android.widget.EditText')
        e_ele.click()  # 点击弹出键盘
        time.sleep(random.randint(1, 3))  # 随机停顿1~2秒
        e_ele.clear_text()
        e_ele.set_text(content)  # 输入
    except Exception as e:
        print_t(e)
    try:
        time.sleep(random.randint(1, 3))  # 随机停顿1~2秒
        d(resourceId="com.zhiliaoapp.musically:id/ad6").click()  # 发送
    except Exception as e:
        print_t(e)
    # 关闭系统键盘
    try:
        time.sleep(random.randint(1, 3))  # 随机停顿1~2秒
        d(resourceId="com.zhiliaoapp.musically:id/t4").click()  # 关闭评论
    except Exception as e:
        print_t(e)


def comment_foryou(content):
    try:
        time.sleep(random.randint(3, 10))  # 随机停顿1~5秒
        d(resourceId="com.zhiliaoapp.musically:id/acm").click()  # 点击评论按钮
    except Exception as e:
        print_t(e)
    try:
        time.sleep(random.randint(1, 3))  # 随机停顿1~2秒
        e_ele = d(text='Add comment...', className='android.widget.EditText')
        e_ele.click()  # 点击弹出键盘
        time.sleep(random.randint(1, 3))  # 随机停顿1~2秒
        e_ele.clear_text()
        e_ele.set_text(content)  # 输入
    except Exception as e:
        print_t(e)
    try:
        time.sleep(random.randint(1, 3))  # 随机停顿1~2秒
        d(resourceId="com.zhiliaoapp.musically:id/ad6").click()  # 发送
    except Exception as e:
        print_t(e)
    # 关闭系统键盘
    try:
        d.press("back")  # 返回1，关闭系统键盘
    except Exception as e:
        print_t(e)


def print_t(content):
    dt = datetime.now()
    print(dt.strftime('%H:%M:%S') + '\t' + str(content))


if __name__ == "__main__":
    # start_vpn()
    # review_tiktok()
    # review_forYou()
    # comment('Look at my')
    d(resourceId="com.zhiliaoapp.musically:id/afa").click()
