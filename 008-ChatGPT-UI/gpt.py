#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description:gpt.py
@Date       :2023/03/31
@Author     :xhunmon
@Mail       :xhunmon@126.com
"""

import time
from datetime import datetime

from utils import *


class Gpt(object):
    func_ui_print = None

    def __init__(self, config: Config):
        self.session = []
        self.api_prompt = []
        self.update_config(config)
        self.content = ""
        self.is_change = False
        self.is_finish = True
        gpt_t = threading.Thread(target=self.start)
        gpt_t.setDaemon(True)
        gpt_t.start()

    def update_config(self, config: Config):
        self.cfg = config
        self.api_key = self.cfg.api_key
        self.api_base = self.cfg.api_base
        self.api_model = self.cfg.model
        self.api_stream = self.cfg.stream
        self.api_response = self.cfg.response
        self.proxy = self.cfg.proxy
        openai.api_key = self.api_key
        if self.api_base:
            openai.api_base = self.api_base
        openai.proxy = self.proxy

    def start(self):
        while True:
            if self.is_finish:
                while not self.is_change:
                    time.sleep(0.3)
                self.print("\nMY:\n{}".format(self.content))
                self.print("\nGPT:\n")
                self.is_change = False
                self.is_finish = False
                self.handle_input(self.content)
            time.sleep(1)

    def print(self, content):
        Gpt.func_ui_print(content)

    def query_openai_stream(self, data: dict) -> str:
        messages = []
        messages.extend(self.api_prompt)
        messages.extend(data)
        answer = ""
        try:
            response = openai.ChatCompletion.create(
                model=self.api_model,
                messages=messages,
                stream=True)
            for part in response:
                finish_reason = part["choices"][0]["finish_reason"]
                if "content" in part["choices"][0]["delta"]:
                    content = part["choices"][0]["delta"]["content"]
                    answer += content
                    self.print(content)
                elif finish_reason:
                    pass

        except KeyboardInterrupt:
            self.print("Canceled")
        except openai.error.OpenAIError as e:
            self.print("OpenAIError:{}".format(e))
            answer = ""
        return answer

    def content_change(self, content: str):
        if not content:
            return
        if self.content != content:
            self.content = content
            self.is_change = True

    def handle_input(self, content: str):
        if not content:
            return
        self.is_finish = False
        self.session.append({"role": "user", "content": content})
        if self.api_stream:
            answer = self.query_openai_stream(self.session)
        else:
            answer = self.query_openai(self.session)
        if not answer:
            self.session.pop()
        elif self.api_response:
            self.session.append({"role": "assistant", "content": answer})
        if answer:
            try:
                if self.cfg.folder and not os.path.exists(self.cfg.folder):
                    os.makedirs(self.cfg.folder)
                wfile = os.path.join(self.cfg.folder, "gpt.md" if self.cfg.repeat else "gpt_{}.md".format(
                    datetime.now().strftime("%Y%m%d%H%M:%S")))
                if self.cfg.repeat:
                    with open(wfile, mode='a', encoding="utf-8") as f:
                        f.write("MY:\n{}\n".format(content))
                        f.write("\nGPT:\n{}\n\n".format(answer))
                        f.close()
                else:
                    with open(wfile, mode='w', encoding="utf-8") as f:
                        f.write("MY:\n{}\n".format(content))
                        f.write("\nGPT:{}".format(answer))
                        f.close()
            except Exception as e:
                self.print("Write error: {} ".format(e))
        self.is_finish = True

    def query_openai(self, data: dict) -> str:
        messages = []
        messages.extend(self.api_prompt)
        messages.extend(data)
        try:
            response = openai.ChatCompletion.create(
                model=self.api_model,
                messages=messages
            )
            content = response["choices"][0]["message"]["content"]
            self.print(content)
            return content
        except openai.error.OpenAIError as e:
            self.print("OpenAI error: {} ".format(e))
        return ""
