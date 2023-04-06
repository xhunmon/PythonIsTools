"""
@Description: 生成autotk.app(https://github.com/xhunmon/autotk)中post发送内容解析，
@Date       :2022/3/20
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
import datetime
import os
import random
import re
import time

import file_util as futls


def get_real_files(folder):
    '''
    获取真实文件，去掉(.xxx)等文隐藏文件
    :param files:
    :return:
    '''
    files = next(os.walk(folder))[2]
    results = []
    for f in files:
        name, ext = os.path.splitext(f)
        if len(name) < 1 or len(ext) < 1 or '.json' == str(ext) or '.txt' == str(ext):  # 非视频文件
            print('非视频文件：{}'.format(f))
            continue
        results.append(f)
    return results


def format_num(num):
    if num < 10:
        return '00{}'.format(num)
    elif num < 100:
        return '0{}'.format(num)
    else:
        return '{}'.format(num)


def split_en_title(spl, content):
    if spl in content:
        temps = content.split(spl)
        coverDesc, title = "", ""
        for temp in temps:
            if len(temp) < 35:
                coverDesc = temp
            else:
                title = temp
        # print('------->过滤《{}》-> {} | {}'.format(spl, coverDesc, title))
        return coverDesc, title
    return None, None


def chose_cover_title(transfer: str):  # 截取合适的标题和封面内容
    # 大于5个字符才开始截取
    trans = re.findall(r'(.{5,}?\?|.{5,}?\.|.{5,}?#|.{5,}?!|.{5,}?$)', transfer)
    title, cover = '', ''
    for tran in trans:
        tran = tran.replace('#', '').strip()
        t_size = len(tran)
        if len(title) < t_size:  # title取最长的
            title = tran
        # cover 优先取10~35个字符的，然后取靠拢的值
        if len(cover) == 0:
            cover = tran
        elif 35 > t_size > 10:
            cover = tran
        elif 10 > t_size > len(cover):
            cover = tran
        elif 35 < t_size < len(cover):
            cover = tran
    return cover, title


def match_info(pre, files, transfers):
    file_name, cover, title, transfer = None, None, None, None
    for v in files:  # 文件名称
        if str(v).startswith(pre):
            file_name = str(v)
            break
    if not file_name:
        raise RuntimeError('没有找到匹配的文件：{}'.format(pre))
    for k in transfers:  # 翻译后当前数据
        if str(k).startswith(pre):
            transfer = str(k)
            break
    if not transfer:
        raise RuntimeError('没有找到匹配的文件：{}'.format(pre))
    # 处理标题
    transfer = transfer[3:].replace('-', '').strip()
    cover, title = chose_cover_title(transfer)
    if not cover or not title:
        raise RuntimeError('获取数据异常：{} | {} | {}'.format(file_name, cover, title))
    return file_name, cover, title


def format_time_by_str(date):  # str转换为时间戳
    time_array = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(time_array))


def format_time_by_stamp(stamp):  # 时间戳转换为时间
    return str(datetime.datetime.fromtimestamp(stamp))


def random_tag(tags):
    num = random.randint(1, 2)
    if len(tags) < num:
        num = len(tags)
    results = []
    rsp = ''
    while True:
        if len(results) == num:
            break
        tag = random.choice(tags)
        if tag in results:
            continue
        results.append(tag)
        rsp += '#{} '.format(tag)
    return rsp


def write_title_one(file_name, folder):
    datas = get_real_files(folder)
    with open(file_name, 'a', encoding='utf-8') as txt_f:
        for f in datas:
            name, ext = os.path.splitext(f)
            txt_f.write('{}\n'.format(name))
        # txt_f.write('AAAAAAAA\n')


def write_title():
    file_name = 'lib/title.txt'
    write_title_one(file_name, 'xxx/bzhsrc/')


def read_title_one(file_name):
    datas = []
    with open(file_name, 'r', encoding='utf-8') as txt_f:
        while True:
            txt = txt_f.readline().replace('\n', '')
            if not txt:
                break
            if len(txt) > 5:
                datas.append(txt)
    return datas


def del_content(content, dels):
    for d in dels:
        content = content.replace(d, '')
    return content


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
    return False


def rename_files(src_folder):  # 重新生成序列
    dels = ['#热࿆门', '#࿆热࿆门', '#热门', '“', '”',
            '-', '-', '[', ']', '《', '》', '/', ':',
            ' ']
    files = get_real_files(src_folder)
    index = 1
    for f in files:
        src = os.path.join(src_folder, f)
        new_name: str = del_content(f, dels)
        num = new_name[0:3]
        if is_number(num):  # 如果有序号
            new_name = '{}-{}'.format(num, new_name[3:])  # 有序号时使用
        else:
            new_name = '{}-{}'.format(format_num(index), new_name)
        dst = os.path.join(src_folder, new_name)
        print(new_name)
        os.rename(src, dst)
        index += 1
    print('总共有[{}]个!'.format(len(files)))


def start_post(userId, src_folder, date_start, title_tags, transfers, musics, dst='post.txt', index=1, space_start=30,
               space_end=40,
               num_start=3, num_end=6, half_time=7):
    '''
    开始生成post.txt文件
    :param userId: 用户id
    :param src_folder: 视频目录
    :param date_start: 第一个启动的时间，格式如：'2022-3-23 19:05:00'
    :param title_tags:
    :param transfers:
    :param musics:
    :param index: 起点位置
    :param space_start: 下一个随机间隔开始发送的视频时间（分钟）
    :param space_end: 下一个随机间隔结束发送的视频时间（分钟）
    :param num_start: 每天随机发几个开始区间
    :param num_end: 每天随机发几个结束区间
    :param half_time（小时）: 保证一半在12点，一半在6点后
    :return:
    '''
    posts = []
    stamp = format_time_by_str(date_start)
    cover_tags = ["Vector", "Glitch", "Tint", "News", "Retro", "Skew", "Pill", "Pop"]  # "Standard" --》有问题
    files = get_real_files(src_folder)
    import copy
    temp_files: list = copy.deepcopy(files)
    size = len(files)
    while index <= size:
        stamp_1 = stamp
        num = random.randint(num_start, num_end)
        half_num = int(num / 2)
        for j in range(0, num):
            if index > size:
                print('已经处理完了：{}'.format(index))
                break
            stamp_1 += random.randint(1, 30) * 60
            if j == half_num:  # 在一半的时候加上秒
                stamp_1 += half_time * 60 * 60
            date = format_time_by_stamp(stamp_1)
            sound = random.choice(musics)
            # pre = format_num(index)
            pre = temp_files.pop()[0:3]
            file, coverDesc, title1 = match_info(pre, files, transfers)
            # TODO- #foryoutoy 玩具需要
            title = '{} {} #foryoutoy'.format(title1, random_tag(title_tags))
            coverTag = random.choice(cover_tags)
            coverPic = random.randint(1, 3)
            post = {"date": date, "sound": sound, "title": title, "file": file, "userId": userId,
                    "coverDesc": coverDesc, "coverTag": coverTag, "coverPic": coverPic}
            print(post)
            posts.append(post)
            stamp_1 += random.randint(space_start, space_end) * 60
            index += 1
        # print('----' * 5)
        stamp += 24 * 60 * 60  # 下一天
    futls.write_json(posts, dst)


def all_step():
    # 1. 翻译文件，整理成txt
    # 2. 标题标签tag，整理成json
    # 3. 过滤无效信息，重命名文件
    # 4. post
    # 美国比英国晚5个小时
    transfers = futls.read_2_list('lib/furrytoy/fanyi_en.txt')  # 英国 19~21,最多8个视频
    title_tags = futls.read_json('lib/furrytoy/tags.json')
    musics = futls.read_json('lib/musics.json')
    dst = 'lib/furrytoy/post.json'
    start_post('kif_nee2022', 'xxx/fyt_toy/', '2022-5-8 10:00:00', transfers=transfers,
               title_tags=title_tags, musics=musics, dst=dst, space_start=70,
               space_end=83,
               num_start=2, num_end=2, half_time=8)  # 每天1~2个，12小时*60


if __name__ == '__main__':
    # write_title()
    # all_step()
    rename_files('xxx/beizhihui')  # 去掉冗余信息
