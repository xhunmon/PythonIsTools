#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: WordPress 站点 将图片转 webp 格式，实现内容重组
@Date       :2022/10/12
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""


import os


def get_contain_pics(folder, content):
    files = next(os.walk(folder))[2]
    results = []
    for f in files:
        name, ext = os.path.splitext(f)
        if len(name) < 1 or len(ext) < 1 or '.json' == str(ext) or '.txt' == str(ext):  # 非视频文件
            continue
        if content in f:
            results.append(f)
    return results


def convert_pic_to_webp(folder, sku, pic_files, t, key1, key2, key3, youtube_num):
    dst_folder = os.path.join('data', sku)
    desc_links = []
    desc_links.append(
        '<div align="center"><iframe width="370" height="658" src="https://www.youtube.com/embed/{}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>\n'.format(
            youtube_num))
    desc_links.append(
        '<div align="center"><a href="https://www.youtube.com/channel/UCm2yBXcNJUjYDMl3yE8Ib7w">more video with youtube >></a></div>\n')
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    # TODO - 上传日期需要注意 月份
    full_url = '<img class="aligncenter size-full wp-image-1376" src="https://www.foryoutoy.com/wp-content/uploads/2022/05/{}" alt="{}" width="{}" height="{}" /> \n'
    tail = '''
<h2>key1 Design Philosophy</h2>
<strong>1st: Ideal Size </strong>
key1 for girls are great companions, are filled with pp cotton. key2 are many sizes to choose from.This soft friend is irresistible! Anirollz got their name from being key3 shaped like rolls, and they are pure squishy fun.

<strong>2nd: Fine Workmanship </strong>
The soft fleece fabric, exquisite embroidery, special color, and full filling of various parts. Therefore, the bear stuffed animal funny plush toy look more lovely and texture. So silky smooth plush toys, you'll never want to let go!

<strong>3rd: Wide Range Of Uses </strong>
key2 can meet different needs. For example, put on the bed, car, sofa for holding, lying down, leaning. The cuddle key1 is soft and comfortable. Therefore, you can use this key1 as your sleeping partner!

<strong>4th: Perfect Gift </strong>
Our key1 will be loved by kids and adults like. For instance, It's a great gift for family or friends at Christmas, Thanksgiving, birthday, graduation or Valentine's day.

<strong>5th: Develop Empathy And Social Skills </strong>
With a cuddling, comforting plush toy companion. It also helps to develop empathy and social skills, and not only stimulates children's imagination and interest in the animal world. And by taking care of their key2 for kids, they build bridges with their friends in the future.in addition, plush toys are the perfect companions for kids three and older and add a unique decorative touch to any nursery, bedroom, or playroom!

<h2>key2 Buyer notice</h2>
<strong>1st: About hair removal</strong>
Did you notice hair loss after receiving the goods? Don't worry, Our giant stuffed animal toys don't shed hair themselves.Because it is a new product, it will have a little floating hair and filling fiber, after you get it, tap it a few times, shake it a few times. it will remove the floating hair.

<strong>2nd: About size</strong>
All products are measured in kind, and the key2 itself is soft and will have a certain error (about 3 cm).

<strong>3rd: About packaging</strong>
We exhaust part of the air for packaging, because key1 itself is relatively large. Only after taking the time to transport can the product be better protected, so when you receive the product, it is slightly off
the description. Small or a little wrinkled, please don't be surprised. because this is a normal phenomenon, shake a few times after opening, under the sun expose for half an hour and recover immediately!

<h2>Our guarantee</h2>
<h3>Insurance</h3>
Each order includes real-time tracking details and insurance.
<h3>Order And Safe</h3>
We reps ready to help and answer any questions, you have within a 24 hour time frame, 7 days a week. We use state-of-the-art SSL Secure encryption to keep your personal and financial information 100% protected.

<h2>Other aspects</h2>
we’re constantly reinventing and reimagining our key3. If you have feedback you would like to share with us, <a href="/contact">please contact us</a>! We genuinely listen to your suggestions when reviewing our existing toys as well as new ones in development. And are you looking for wholesale plush doll for your school or church carnival? We have the perfect mix of darling stuffed toys for carnival prizes all sold at wholesale prices! We have everything from small stuffed animals such as key1 & dogs, fish, turtles, apes, owls, sharks, & bugs to big stuffed doll such as our large stuffed toy frog and our lovable, key3 and puppy dog!

<img class="aligncenter size-full wp-image-1043" src="https://www.foryoutoy.com/wp-content/uploads/2022/04/shoppingtell-3.webp" alt="large stuffed animals for adults and kids" width="470" height="113" />    
    '''
    tail = tail.replace('key1', key1).replace('key2', key2).replace('key3', key3)
    for i in range(0, len(pic_files)):
        f = pic_files[i]
        src = os.path.join(folder, f)
        # dst_name = '{}-m-{}{}'.format(sku, i + 1, ext)
        dst_name = '{}-{}-{}.webp'.format(sku, t, i + 1)  # 更新至webp
        dst = os.path.join(dst_folder, dst_name)
        from PIL import Image
        im = Image.open(src)  # 读入文件
        print(im.size)
        width = 500
        if im.size[0] > width:
            h = int(width * im.size[1] / im.size[0])
            print(h)
            im.thumbnail((width, h), Image.ANTIALIAS)  # 重新设置图片大小
        im.save(dst)  # 保存
        print(dst)
        if i < 1:
            alt_key = key3
        elif i < 3:
            alt_key = key2
        else:
            alt_key = key1
        if t == 'd':
            size = Image.open(dst).size
            desc_links.append(full_url.format(dst_name, alt_key, size[0], size[1]))
    if t == 'd':
        with open(os.path.join('data/desc-html', '{}.txt'.format(sku)), mode='w', encoding='utf-8') as f:
            for link in desc_links:
                f.write(link)
                f.write('\n')
            f.write(tail)
        f.close()


def deal_sku(folder, sku, key1, key2, key3, youtube_num):
    folder = os.path.join(folder, sku)
    main_pics = sorted(get_contain_pics(folder, '主图'))
    desc_pics = sorted(get_contain_pics(folder, '详情'))
    convert_pic_to_webp(folder, sku, main_pics, 'm', key1, key2, key3, youtube_num)
    convert_pic_to_webp(folder, sku, desc_pics, 'd', key1, key2, key3, youtube_num)


def deal_sku_list():
    folder = 'xxx/SKU/'
    deal_sku(folder, 'FYTA032DX', 'elephant plush toy', 'stuffed animal elephant', 'elephant stuffed toy', '4kB0ZJBmMkU')  # 奶瓶大象


def convert_2_webp(src, dst):
    from PIL import Image
    im = Image.open(src)  # 读入文件
    print(im.size)
    # width = 500
    # if im.size[0] > width:
    #     h = int(width * im.size[1] / im.size[0])
    #     print(h)
    #     im.thumbnail((width, h), Image.ANTIALIAS)  # 重新设置图片大小
    im.save(dst)  # 保存


def convert_folder(src_folder, dst_folder):
    files = next(os.walk(src_folder))[2]
    for f in files:
        if str(f).startswith('.'):
            continue
        name, ext = os.path.splitext(f)
        convert_2_webp(os.path.join(src_folder, f), os.path.join(dst_folder, '{}.webp'.format(name)))


'''
操作说明：
一：使用Fatkun工具下载图片后进行刷选
1、主图主要4张
2、详情图看情况删除一些，最好保留产品尺寸相关说明的图，正常不会超过10张
二：使用本脚本进行进图压缩以及格式转换（压缩了10倍左右）
1.本脚本将图片宽带缩小至500，高度等比例缩小
2.本脚本将jpg、png格式转换成webp格式
三：新建产品编辑
1.本脚本生成描述图片连接，直接拷贝过去
2.将变量尺寸属性值数字后面加上cm
3.两种产品，定价范围
A. 长条（如：FYTA004BR，长条兔子），属性名称：Long
70cm  18~21
90cm  35~40
110cm 60~70
130cm 90~100
150cm 120~130
B. 圆形（如：FYTA001SP，奶瓶猪），属性名称：Height
35cm  30~35
45cm  55~59
55cm  80~88
65cm  120~130
75cm  160~180
'''
if __name__ == '__main__':
    # deal_sku_list()
    convert_folder('xxx/png', 'xxx/webp')

#Best Stuffed Pig Toys With A Hat