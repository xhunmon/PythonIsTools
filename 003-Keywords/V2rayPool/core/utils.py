#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import re
import os
import socket
import string
import sys
import termios
import tty
import urllib.request
import signal
import subprocess
from enum import Enum, unique


class ProtocolType(object):
    TROJAN = 'trojan://'
    SS = 'ss://'
    VMESS = 'vmess://'


@unique
class StreamType(Enum):
    TCP = 'tcp'
    TCP_HOST = 'tcp_host'
    SOCKS = 'socks'
    SS = 'ss'
    MTPROTO = 'mtproto'
    H2 = 'h2'
    WS = 'ws'
    QUIC = 'quic'
    KCP = 'kcp'
    KCP_UTP = 'utp'
    KCP_SRTP = 'srtp'
    KCP_DTLS = 'dtls'
    KCP_WECHAT = 'wechat'
    KCP_WG = 'wireguard'
    VLESS_KCP = 'vless_kcp'
    VLESS_UTP = 'vless_utp'
    VLESS_SRTP = 'vless_srtp'
    VLESS_DTLS = 'vless_dtls'
    VLESS_WECHAT = 'vless_wechat'
    VLESS_WG = 'vless_wireguard'
    VLESS_TCP = 'vless_tcp'
    VLESS_TLS = 'vless_tls'
    VLESS_WS = 'vless_ws'
    VLESS_GRPC = 'vless_grpc'
    VLESS_XTLS = 'vless_xtls'
    TROJAN = 'trojan'


def header_type_list():
    return ("none", "srtp", "utp", "wechat-video", "dtls", "wireguard")


def ss_method():
    return ("aes-256-gcm", "aes-128-gcm", "chacha20-poly1305")


def xtls_flow():
    return ("", "xtls-rprx-origin", "xtls-rprx-direct")


def get_ip():
    """
    获取本地ip
    """
    my_ip = ""
    try:
        my_ip = urllib.request.urlopen('http://api.ipify.org').read()
    except Exception:
        my_ip = urllib.request.urlopen('http://icanhazip.com').read()
    return bytes.decode(my_ip).strip()


def port_is_use(port):
    """
    判断端口是否占用
    """
    tcp_use, udp_use = False, False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(3)
    tcp_use = s.connect_ex(('127.0.0.1', int(port))) == 0
    try:
        u.bind(('127.0.0.1', int(port)))
    except:
        udp_use = True
    finally:
        u.close()
    return tcp_use or udp_use


def random_port(start_port, end_port):
    while True:
        random_port = random.randint(start_port, end_port)
        if not port_is_use(random_port):
            return random_port


def is_email(email):
    """
    判断是否是邮箱格式
    """
    str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    return re.match(str, email)


def is_ipv4(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(ip)
        except socket.error:
            return False
        return ip.count('.') == 3
    except socket.error:  # not a valid ip
        return False
    return True


def is_ipv6(ip):
    try:
        socket.inet_pton(socket.AF_INET6, ip)
    except socket.error:  # not a valid ip
        return False
    return True


def check_ip(ip):
    return is_ipv4(ip) or is_ipv6(ip)


def bytes_2_human_readable(number_of_bytes, precision=1):
    """
    流量bytes转换为kb, mb, gb等单位
    """
    if number_of_bytes < 0:
        raise ValueError("!!! number_of_bytes can't be smaller than 0 !!!")

    step_to_greater_unit = 1024.

    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'

    number_of_bytes = round(number_of_bytes, precision)

    return str(number_of_bytes) + ' ' + unit


def random_email():
    domain = ['163', 'qq', 'sina', '126', 'gmail', 'outlook', 'icloud']
    core_email = "@{}.com".format(random.choice(domain))
    return ''.join(random.sample(string.ascii_letters + string.digits, 8)) + core_email


def readchar(prompt=""):
    if prompt:
        sys.stdout.write(prompt)
        sys.stdout.flush()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    print(ch)
    return ch.strip()

def kill_all_v2ray():
    pids = os.popen("ps aux |grep v2ray |awk '{print $2}'").read().split('\n')
    for pid in pids:
        try:
            import subprocess
            # subprocess.check_output("kill %d" % int(pid))
            a = os.popen("kill %d" % int(pid)).read()
        except Exception as e:
            pass

# netstat -nlp | grep :1080 | awk '{print $7}' | awk -F\" / \" '{ print $1 }'
def kill_process_by_port(port):
    try:
        # kill -9 `ps -ef |grep act1 |awk 'NR==1{print $3}'`
        # pids = os.popen("pgrep -f v2ray|xargs -n1 kill -9").read().split('\n')
        pids = os.popen("pgrep -f v2ray|xargs kill -9").read().split('\n')
        print(pids)
        # a = os.kill(int(pid), 0)
        # a = os.popen("kill %d" % int(pid)).read()
        # print('已杀死port为%d,pid为%s的进程,　返回值是:%s' % (port, pid, a))
    except:
        pass
    pid_all = []
    # ps aux | grep 'v2ray' |  awk '{print $2}
    # pids = os.popen("lsof -i:%d |  awk '{print $2}'" % (port)).read().split('\n')


    # pids = os.popen("ps aux |grep v2ray |awk '{print $2}'").read().split('\n')
    # # pids = os.popen("ps aux | grep 'v2ray' |  awk '{print $2}'").read().split('\n')
    # print(pids)
    # for pid in pids:
    #     temp = pid.strip()
    #     if len(temp) > 1 and temp != 'PID' and temp != '0' and temp not in pid_all:
    #         pid_all.append(temp)
    # for pid in pid_all:
    #     # a = os.kill(int(pid), 0)
    #     # a = os.popen("kill -9 %d" % int(pid)).read()
    #     try:
    #         process = subprocess.Popen("kill %d" % int(pid), shell=True)
    #         os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    #         # a = os.kill(int(pid), 0)
    #         # a = os.popen("kill %d" % int(pid)).read()
    #         print('已杀死port为%d,pid为%s的进程,　返回值是:%s' % (port, pid, a))
    #     except:
    #         pass
