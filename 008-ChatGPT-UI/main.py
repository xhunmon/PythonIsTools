#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: main
@Date       :2023/03/31
@Author     :xhunmon
@Mail       :xhunmon@126.com
"""
import sys
import tkinter as tk
from tkinter.filedialog import *

from gpt import *
from utils import *


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder='', **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = self['fg']
        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<FocusOut>', self.on_focus_out)
        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def remove_placeholder(self):
        cur_value = self.get()
        if cur_value == self.placeholder:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg_color

    def on_focus_in(self, event):
        self.remove_placeholder()

    def on_focus_out(self, event):
        if not self.get():
            self.put_placeholder()


class Application(tk.Frame):
    def __init__(self, config: Config, master=None):
        super().__init__(master)
        self.cfg = config
        self.gpt = None
        self.repeat = False
        self.master = master
        self.master.title(ConfigIni.instance().get_title())
        self.pack()
        self.create_widgets()

    def create_config(self):
        row = tk.Frame(self)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        button = tk.Button(row, text="Config", width='7', command=self.click_config)
        button.pack(side=tk.LEFT, padx=5, pady=5)
        self.configEntry = EntryWithPlaceholder(row, placeholder=self.cfg.config_path, width=45)
        self.configEntry.pack(side=tk.LEFT, padx=5, pady=5)
        button = tk.Button(row, text="Create", width='7', command=self.click_create)
        button.pack(side=tk.LEFT, padx=5, pady=5)

    def create_folder(self):
        row = tk.Frame(self)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        button = tk.Button(row, text="Folder", width='7', command=self.click_folder)
        button.pack(side=tk.LEFT, padx=5, pady=5)
        self.folderEntry = EntryWithPlaceholder(row,
                                                placeholder=self.cfg.folder if self.cfg.folder else f'{Config.pre_tips} chat output directory, default current',
                                                width=50)
        self.folderEntry.pack(side=tk.LEFT, padx=5, pady=5)

    def create_key(self):
        row = tk.Frame(self)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        label = tk.Label(row, text=f"Key: ", width='7')
        label.pack(side=tk.LEFT)
        self.keyEntry = EntryWithPlaceholder(row,
                                             placeholder=self.cfg.api_key if self.cfg.api_key else f'{Config.pre_tips} input key id',
                                             width=50)
        self.keyEntry.pack(side=tk.LEFT, padx=5, pady=5)

    def create_model(self):
        row = tk.Frame(self)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        label = tk.Label(row, text=f"Model: ", width='7')
        label.pack(side=tk.LEFT)
        self.modelEntry = EntryWithPlaceholder(row,
                                               placeholder=self.cfg.model if self.cfg.model else f'{Config.pre_tips} default gpt-3.5-turbo, or: gpt-4/gpt-4-32k',
                                               width=50)
        self.modelEntry.pack(side=tk.LEFT, padx=5, pady=5)

    def create_proxy(self):
        row = tk.Frame(self)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        label = tk.Label(row, text=f"Proxy: ", width='7')
        label.pack(side=tk.LEFT)
        self.proxyEntry = EntryWithPlaceholder(row,
                                               placeholder=self.cfg.proxy if self.cfg.proxy else f'{Config.pre_tips} default empty, or http/https/socks4a/socks5',
                                               width=50)
        self.proxyEntry.pack(side=tk.LEFT, padx=5, pady=5)

    def create_send(self):
        row = tk.Frame(self)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.sendEntry = EntryWithPlaceholder(row, placeholder=f'{Config.pre_tips} say something, then click send.',
                                              width=55)
        self.sendEntry.pack(side=tk.LEFT, padx=5, pady=5)
        self.sendEntry.bind("<Return>", self.on_return_key)
        button = tk.Button(row, text="Send", width='7', command=self.click_send)
        button.pack(side=tk.LEFT, padx=5, pady=5)

    def create_widgets(self):
        self.create_config()
        self.create_folder()
        self.create_key()
        self.create_model()
        self.create_proxy()
        self.create_send()
        # bottom text
        text_frame = tk.Frame(self)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.text = tk.Text(text_frame, wrap=tk.WORD, undo=True, font=("Helvetica", 12))
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_bar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text.yview)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=scroll_bar.set)

        # email text
        email_button = tk.Button(self, text=ConfigIni.instance().get_email())
        email_button.pack(side=tk.LEFT, padx=5, pady=5)

        # version text
        version_button = tk.Button(self, text=ConfigIni.instance().get_version_name())
        version_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # clear text
        clear_button = tk.Button(self, text="clear", width=10, command=self.clear)
        clear_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # copy text
        copy_button = tk.Button(self, text="copy", width=10, command=self.copy)
        copy_button.pack(side=tk.RIGHT, padx=5, pady=5)

        Gpt.func_ui_print = self.func_ui_print

    def refresh(self):
        # self.set_entry(self.configEntry, self.cfg.default)
        self.set_entry(self.folderEntry, self.cfg.folder)
        self.set_entry(self.keyEntry, self.cfg.api_key)
        self.set_entry(self.modelEntry, self.cfg.model)
        self.set_entry(self.proxyEntry, self.cfg.proxy)

    def func_ui_print(self, txt):
        self.show_text(txt)

    def click_config(self):
        path = askopenfilename()
        self.set_entry(self.configEntry, path)
        if self.cfg.update(path):
            self.refresh()
        else:
            self.show_text("update fail !")

    def click_create(self):
        self.cfg.click_create()
        self.show_text("create file :{} ".format(self.cfg.config_path))

    def click_folder(self):
        path = askdirectory()
        self.set_entry(self.folderEntry, path)

    def set_entry(self, entry: tk.Entry, content):
        entry.delete(0, tk.END)
        entry.insert(0, content)

    def on_return_key(self, event):
        self.click_send()

    def click_send(self):
        # config = self.configEntry.get()
        self.cfg.update_by_content(self.keyEntry.get(), self.modelEntry.get(), self.folderEntry.get(),
                                   self.proxyEntry.get())
        content: str = self.sendEntry.get()
        # self.show_text("me: {}\n".format(content))
        if not self.gpt:
            self.gpt: Gpt = Gpt(self.cfg)
        else:
            self.gpt.update_config(self.cfg)
        self.gpt.content_change(content)

    def show_text(self, content):
        self.text.insert(tk.END, "{}".format(content))
        self.text.yview_moveto(1.0)  # auto scroll to new

    def clear(self):
        self.text.delete("1.0", "end")

    def copy(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.text.get("1.0", tk.END))


if __name__ == "__main__":
    root = tk.Tk()
    folder = os.path.dirname(os.path.realpath(sys.argv[0]))
    app = Application(Config(folder), master=root)
    app.mainloop()
