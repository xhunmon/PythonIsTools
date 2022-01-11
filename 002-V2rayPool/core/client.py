#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import json
import os
import urllib

from core.conf import Config
from core.group import Vmess, Vless, Socks, SS, Mtproto, Trojan, Group, Dyport
from core.utils import ProtocolType
import core.utils as util


class ClientWriter:
    def __init__(self, group):
        self.config_factory = Config()
        # with open(self.config_factory.get_path('config_path'), 'r') as json_file:
        #     self.config = json.load(json_file)

        self.write_path = self.config_factory.get_path("config_path")
        self.template_path = self.config_factory.json_path
        self.group = group
        self.node = group.node

    def load_template(self, template_name):
        '''
        load special template
        '''
        with open(self.template_path + "/" + template_name, 'r') as stream_file:
            template = json.load(stream_file)
        return template

    def transform(self):
        user_json = None
        if type(self.node) == Vmess:
            self.client_config = self.load_template('client.json')
            user_json = self.client_config["outbounds"][0]["settings"]["vnext"][0]
            user_json["users"][0]["id"] = self.node.password
            user_json["users"][0]["alterId"] = self.node.alter_id

        elif type(self.node) == Vless:
            self.client_config = self.load_template('client.json')
            user_json = self.client_config["outbounds"][0]["settings"]["vnext"][0]
            user_json["users"][0]["id"] = self.node.password
            del user_json["users"][0]["alterId"]
            del user_json["users"][0]["security"]
            user_json["users"][0]["encryption"] = self.node.encryption
            if self.node.flow:
                user_json["users"][0]["flow"] = self.node.flow
            self.client_config["outbounds"][0]["protocol"] = "vless"

        elif type(self.node) == Socks:
            self.client_config = self.load_template('client_socks.json')
            user_json = self.client_config["outbounds"][0]["settings"]["servers"][0]
            user_json["users"][0]["user"] = self.node.user_info
            user_json["users"][0]["pass"] = self.node.password

        elif type(self.node) == SS:
            self.client_config = self.load_template('client_ss.json')
            user_json = self.client_config["outbounds"][0]["settings"]["servers"][0]
            user_json["method"] = self.node.method
            user_json["password"] = self.node.password

        elif type(self.node) == Trojan:
            self.client_config = self.load_template('client_trojan.json')
            user_json = self.client_config["outbounds"][0]["settings"]["servers"][0]
            user_json["password"] = self.node.password

        elif type(self.node) == Mtproto:
            print("")
            print("MTProto protocol only use Telegram, and can't generate client json!")
            print("")
            exit(-1)

        try:
            if isinstance(self.group.port, int):
                user_json["port"] = self.group.port
            else:
                user_json["port"] = int(self.group.port)
            user_json["address"] = self.group.ip
            self.client_config["inbounds"][0]["listen"] = self.group.listen
            self.client_config["inbounds"][0]["port"] = self.group.i_port
        except:
            print('数据异常，启动失败')
            return
            # inbounds = self.client_config["inbounds"]
        # for inbound in inbounds:
        #     inbound["listen"] = self.group.listen

        # if type(self.node) != SS:
        #     self.client_config["outbounds"][0]["streamSettings"] = self.config["inbounds"][self.group.index][
        #         "streamSettings"]

        if self.group.tls == 'tls':
            self.client_config["outbounds"][0]["streamSettings"]["tlsSettings"] = {}
        elif self.group.tls == 'xtls':
            self.client_config["outbounds"][0]["streamSettings"]["xtlsSettings"]["serverName"] = self.group.ip
            del self.client_config["outbounds"][0]["streamSettings"]["xtlsSettings"]["certificates"]
            del self.client_config["outbounds"][0]["streamSettings"]["xtlsSettings"]["alpn"]
            del self.client_config["outbounds"][0]["mux"]

    def write(self):
        '''
        写客户端配置文件函数
        '''
        json_dump = json.dumps(self.client_config, indent=1)
        with open(self.write_path, 'w') as write_json_file:
            write_json_file.writelines(json_dump)
        # print("{0}({1})".format("save json success!", self.write_path))


class Creator(object):
    """
    生成代理json并启动
    """

    def __init__(self):
        self.__thread = None
        self.__main_pid = os.getpid()

    def parse_vmess(self, vmesslink):
        """返回：{'v': '2', 'ps': 'https://git.io/v9999 圣何塞sv2', 'add': 'sv2.free3333.xyz', 'port': '26707', 'id': '8f7a28a6-002a-11ec-b64a-00163cf00cd9', 'aid': '0', 'net': 'tcp', 'type': 'none', 'host': '', 'path': '', 'tls': '', 'sni': ''}"""
        if vmesslink.startswith(ProtocolType.VMESS):
            bs = vmesslink[len(ProtocolType.VMESS):]
            # paddings
            blen = len(bs)
            if blen % 4 > 0:
                bs += "=" * (4 - blen % 4)
            vms = base64.b64decode(bs).decode()
            return json.loads(vms)
        else:
            raise Exception("vmess link invalid")

    def parse_trojan(self, link):
        link = urllib.parse.unquote(link)
        trStr = link[link.find("//") + 2:]
        password = trStr[:trStr.find('@')]
        trStr = trStr[trStr.find('@') + 1:]
        sni = trStr[:trStr.find(':')]
        trStr = trStr[trStr.find(':') + 1:]
        port = trStr[:trStr.find('#')]
        name = trStr[trStr.find('#') + 1:]
        node = {
            "name": name,
            "server": sni,
            "port": port,
            "type": "trojan",
            "password": password,
            "sni": sni
        }
        return node

    def parse_ss(self, sslink):
        RETOBJ = {
            "v": "2",
            "ps": "",
            "add": "",
            "port": "",
            "id": "",
            "aid": "",
            "net": "shadowsocks",
            "type": "",
            "host": "",
            "path": "",
            "tls": ""
        }
        if sslink.startswith(ProtocolType.SS):
            info = sslink[len(ProtocolType.SS):]

            if info.rfind("#") > 0:
                info, _ps = info.split("#", 2)
                RETOBJ["ps"] = urllib.parse.unquote(_ps)

            if info.find("@") < 0:
                # old style link
                # paddings
                blen = len(info)
                if blen % 4 > 0:
                    info += "=" * (4 - blen % 4)
                info = base64.b64decode(info).decode()
                atidx = info.rfind("@")
                method, password = info[:atidx].split(":", 2)
                addr, port = info[atidx + 1:].split(":", 2)
            else:
                atidx = info.rfind("@")
                addr, port = info[atidx + 1:].split(":", 2)
                info = info[:atidx]
                blen = len(info)
                if blen % 4 > 0:
                    info += "=" * (4 - blen % 4)
                info = base64.b64decode(info).decode()
                method, password = info.split(":", 2)
            RETOBJ["add"] = addr
            RETOBJ["port"] = port
            RETOBJ["aid"] = method
            RETOBJ["id"] = password
            return RETOBJ

    def generateAndWrite(self, url: str):
        # listen="127.0.0.1",
        group = Group(None, 1024, end_port=None, tls="none", tfo="open", dyp=Dyport(), index=0)
        if url.startswith(ProtocolType.VMESS):
            _json = self.parse_vmess(url.strip())
            node = Vmess(uuid=_json['id'], alter_id=int(_json['aid']), network=_json['net'], user_number=1,
                         path=_json['path'] if 'path' in _json else None,
                         host=_json['host'], header=None, email=None,
                         quic=None)
            group.port = _json['port']
            group.tls = _json['tls']
            group.ip = _json['add']
            group.protocol = node.__class__.__name__
            group.node = node
            print(_json)
        elif url.startswith(ProtocolType.SS):
            _json = self.parse_ss(url.strip())
            # {'v': '2', 'ps': 'github.com/freefq - 罗马尼亚  10', 'add': '194.110.115.83', 'port': '43893', 'id': 'YyCBeDdYX4cadHpCkkmdJLq8', 'aid': 'aes-256-gcm', 'net': 'shadowsocks', 'type': '', 'host': '', 'path': '', 'tls': ''}
            node = SS(0, _json['id'], _json['aid'], None)
            group.port = _json['port']
            group.tls = _json['tls']
            group.ip = _json['add']
            group.protocol = node.__class__.__name__
            group.node = node
            print(_json)
        elif url.startswith(ProtocolType.TROJAN):
            _json = self.parse_trojan(url.strip())
            node = Trojan(0, _json['password'], None)
            group.port = _json['port']
            group.tls = ''
            group.ip = _json['sni']
            group.protocol = node.__class__.__name__
            group.node = node
            print(_json)
        else:
            print('无效地址：%s' % url)
            return
        cw = ClientWriter(group)
        cw.transform()
        cw.write()

    def __kill_threading(self):
        pids = os.popen("ps aux |grep v2ray |awk '{print $2}'").read().split('\n')
        pid_all = []
        for pid in pids:
            temp = pid.strip()
            if len(temp) > 1 and temp != 'PID' and temp != '0' and temp != str(self.__main_pid) and temp not in pid_all:
                pid_all.append(temp)
        for pid in pid_all:
            try:
                import subprocess
                # subprocess.check_output("kill %d" % int(pid))
                a = os.popen("kill %d" % int(pid)).read()
            except Exception as e:
                pass
        util.sys_proxy_off()

    def __child_thread(self, url: str, isSysOn: False):
        self.generateAndWrite(url)
        # 执行就可，不需要知道结果
        if Config.get_v2ray_core_path() is None:
            raise Exception('请先调用#Config.set_v2ray_core_path 设置路径')
        v2ray_path = os.path.join(Config.get_v2ray_core_path(), 'v2ray')
        config_path = os.path.join(Config.get_v2ray_core_path(), 'config.json')
        os.popen("%s -config %s >/dev/null 2>&1" % (v2ray_path, config_path))
        print("%s -config %s >/dev/null 2>&1" % (v2ray_path, config_path))
        if isSysOn:
            util.sys_v2ray_on()

    def v2ray_start(self, url: str, isSysOn: False):
        self.__kill_threading()
        self.__child_thread(url, isSysOn)

    def v2ray_start_with_log(self, url: str, isSysOn: False):
        try:
            self.v2ray_start(url, isSysOn)
        except Exception as e:
            print(e)
            print("启动异常：%s" % url)
            return False
        return True
