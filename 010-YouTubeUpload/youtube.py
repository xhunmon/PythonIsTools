#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/9 09:10
@Author  : xhunmon
@Email   : xhunmon@126.com
@File    : youtube.py
@Desc    :
1. 关闭所有浏览器：
2. 命令格式：浏览器名称 --remote-debugging-port=端口号
例：
windows：chrome --remote-debugging-port=9222
mac：/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
"""

import logging
import platform
import time
from datetime import datetime
from typing import Optional, Tuple

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

logging.basicConfig()


class YtbConst:
    """A class for storing constants for YoutubeUploader class"""
    YOUTUBE_URL = 'https://www.youtube.com'
    YOUTUBE_STUDIO_URL = 'https://studio.youtube.com'
    YOUTUBE_UPLOAD_URL = 'https://www.youtube.com/upload'
    USER_WAITING_TIME = 1
    VIDEO_TITLE = 'title'
    VIDEO_DESCRIPTION = 'description'
    VIDEO_EDIT = 'edit'
    VIDEO_TAGS = 'tags'
    TEXTBOX_ID = 'textbox'
    TEXT_INPUT = 'text-input'
    RADIO_LABEL = 'radioLabel'
    UPLOADING_STATUS_CONTAINER = '//*[@id="dialog"]/div[2]/div/ytcp-video-upload-progress/span'
    NOT_MADE_FOR_KIDS_LABEL = 'VIDEO_MADE_FOR_KIDS_NOT_MFK'

    UPLOAD_DIALOG = '//ytcp-uploads-dialog'
    ADVANCED_BUTTON_ID = 'toggle-button'
    TAGS_CONTAINER_ID = 'tags-container'

    TAGS_INPUT = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[4]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input'
    NEXT_BUTTON = '//*[@id="next-button"]/div'
    PUBLIC_BUTTON = '//*[@id="done-button"]/div'
    VIDEO_URL_CONTAINER = "//span[@class='video-url-fadeable style-scope ytcp-video-info']"
    VIDEO_URL_ELEMENT = '//*[@id="share-url"]'
    HREF = 'href'
    ERROR_CONTAINER = '//*[@id="error-message"]'
    VIDEO_NOT_FOUND_ERROR = 'Could not find video_id'
    DONE_BUTTON = 'done-button'
    INPUT_FILE_VIDEO = "//input[@type='file']"
    INPUT_FILE_THUMBNAIL = "//input[@id='file-loader']"

    # Playlist
    VIDEO_PLAYLIST = 'playlist_title'
    PL_DROPDOWN_CLASS = 'ytcp-video-metadata-playlists'
    PL_SEARCH_INPUT_ID = 'search-input'
    PL_ITEMS_CONTAINER_ID = 'items'
    PL_ITEM_CONTAINER = '//span[text()="{}"]'
    PL_NEW_BUTTON_CLASS = 'new-playlist-button'
    PL_CREATE_PLAYLIST_CONTAINER_XPATH = '//*[@id="text-item-0"]/ytcp-ve'
    PL_CREATE_BUTTON_XPATH = '//*[@id="create-button"]/div'
    PL_DONE_BUTTON_CLASS = 'done-button'

    # Schedule 发布时间
    VIDEO_SCHEDULE = 'schedule'
    SCHEDULE_CONTAINER_ID = 'schedule-radio-button'
    SCHEDULE_DATE_ID = 'datepicker-trigger'
    SCHEDULE_DATE_TEXTBOX = '/html/body/ytcp-date-picker/tp-yt-paper-dialog/div/form/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/div/iron-input/input'
    SCHEDULE_TIME = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[3]/ytcp-visibility-scheduler/div[1]/ytcp-datetime-picker/div/div[2]/form/ytcp-form-input-container/div[1]/div/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/div/iron-input/input"


class YtbUploader:
    """
    YouTube上传
    """

    def __init__(self) -> None:
        """

        @param video_path:    视频路径
        @param metadata_json: 字典数据
                            meta = {
                                "title": "标题",
                                "description": "描述",
                                "tags": ["标签1","标签2"],
                                "edit": False,
                                "playlist_title": "分栏标题",
                                "schedule": ""
                        }
        @param new_window:     在现有的的浏览器中打开新的页面，没做登录。需要配置先启动浏览器。
        @param thumbnail_path:
        """
        self.video_path = None
        self.thumbnail_path = None
        self.metadata_dict = None
        self.browser: Chrome = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.is_mac = False
        if not any(os_name in platform.platform() for os_name in ["Windows", "Linux"]):
            self.is_mac = True

    def __login(self):
        self.browser.get(YtbConst.YOUTUBE_URL)
        time.sleep(YtbConst.USER_WAITING_TIME)

    def __clear_field(self, field):
        field.click()
        time.sleep(YtbConst.USER_WAITING_TIME)
        if self.is_mac:
            field.send_keys(Keys.COMMAND + 'a')
        else:
            field.send_keys(Keys.CONTROL + 'a')
        time.sleep(YtbConst.USER_WAITING_TIME)
        field.send_keys(Keys.BACKSPACE)

    def __write_in_field(self, field, string, select_all=False):
        if select_all:
            self.__clear_field(field)
        else:
            field.click()
            time.sleep(YtbConst.USER_WAITING_TIME)

        field.send_keys(string)

    def __get_video_id(self) -> Optional[str]:
        video_id = None
        try:
            video_url_element = self.browser.find_element(By.XPATH, YtbConst.VIDEO_URL_ELEMENT)
            video_id = video_url_element.get_attribute(
                YtbConst.HREF).split('/')[-1]
        except:
            self.logger.warning(YtbConst.VIDEO_NOT_FOUND_ERROR)
            pass
        return video_id

    def upload(self, browser, path, meta, thumbnail=None):
        self.browser = browser
        self.video_path = path
        self.thumbnail_path = thumbnail
        self.metadata_dict = meta
        # self.__login()
        return self.__upload()

    def exit(self):
        self.browser.close()

    def __wait_loading(self):
        count = 1
        while count <= 10:
            time.sleep(YtbConst.USER_WAITING_TIME)
            try:
                uploading_status_container = self.browser.find_element(By.XPATH,
                                                                       YtbConst.UPLOADING_STATUS_CONTAINER)
                uploading_progress = uploading_status_container.text
                self.logger.debug('Upload video progress: {}'.format(uploading_progress))
                if uploading_progress is None or len(uploading_progress) < 5:
                    break
            except:
                self.logger.debug('Upload loading trying {}'.format(count))
                count += 1

    def __upload(self) -> Tuple[bool, Optional[str]]:
        edit_mode = self.metadata_dict[YtbConst.VIDEO_EDIT]
        if edit_mode:
            self.browser.get(edit_mode)
            time.sleep(YtbConst.USER_WAITING_TIME)
        else:
            # 切换到最新的开的页面，然后在该页面直接加载地址
            self.browser.switch_to.window(self.browser.window_handles[0])
            self.browser.get(YtbConst.YOUTUBE_URL)
            time.sleep(YtbConst.USER_WAITING_TIME)
            self.browser.get(YtbConst.YOUTUBE_UPLOAD_URL)
            time.sleep(YtbConst.USER_WAITING_TIME)
            absolute_video_path = self.video_path
            self.browser.find_element(By.XPATH, YtbConst.INPUT_FILE_VIDEO).send_keys(
                absolute_video_path)
            self.logger.debug('Attached video {}'.format(self.video_path))

            # Find status container
            # self.__wait_loading()
            time.sleep(YtbConst.USER_WAITING_TIME * 2)

        if self.thumbnail_path is not None:
            absolute_thumbnail_path = self.thumbnail_path
            self.browser.find_element(By.XPATH, YtbConst.INPUT_FILE_THUMBNAIL).send_keys(
                absolute_thumbnail_path)
            change_display = "document.getElementById('file-loader').style = 'display: block! important'"
            self.browser.execute_script(change_display)
            self.logger.debug(
                'Attached thumbnail {}'.format(self.thumbnail_path))

        textboxs = self.browser.find_elements(By.ID, YtbConst.TEXTBOX_ID)
        title_field, description_field = textboxs[0], textboxs[1]
        # //*[@id="textbox"]
        self.__write_in_field(
            title_field, self.metadata_dict[YtbConst.VIDEO_TITLE], select_all=True)
        self.logger.debug('The video title was set to \"{}\"'.format(
            self.metadata_dict[YtbConst.VIDEO_TITLE]))

        video_description = self.metadata_dict[YtbConst.VIDEO_DESCRIPTION]
        video_description = video_description.replace("\n", Keys.ENTER)
        if video_description:
            self.__write_in_field(description_field, video_description, select_all=True)
            self.logger.debug('Description filled.')

        kids_section = self.browser.find_element(By.NAME, YtbConst.NOT_MADE_FOR_KIDS_LABEL)
        kids_section.location_once_scrolled_into_view
        time.sleep(YtbConst.USER_WAITING_TIME)

        self.browser.find_element(By.ID, YtbConst.RADIO_LABEL).click()
        self.logger.debug('Selected \"{}\"'.format(YtbConst.NOT_MADE_FOR_KIDS_LABEL))

        # Playlist
        playlist = self.metadata_dict[YtbConst.VIDEO_PLAYLIST]
        if playlist:
            self.browser.find_element(By.CLASS_NAME, YtbConst.PL_DROPDOWN_CLASS).click()  # 点击播放列表
            time.sleep(YtbConst.USER_WAITING_TIME)
            self.logger.debug('Playlist xpath: "{}".'.format(YtbConst.PL_ITEM_CONTAINER.format(playlist)))
            try:
                playlist_item = self.browser.find_element(By.XPATH, YtbConst.PL_ITEM_CONTAINER.format(playlist))
            except:
                playlist_item = None
            if playlist_item:
                self.logger.debug('Playlist found.')
                playlist_item.click()
                time.sleep(YtbConst.USER_WAITING_TIME)
            else:
                self.logger.debug('Playlist not found. Creating')
                # self.__clear_field(search_field)
                time.sleep(YtbConst.USER_WAITING_TIME)

                new_playlist_button = self.browser.find_element(By.CLASS_NAME, YtbConst.PL_NEW_BUTTON_CLASS)
                new_playlist_button.click()

                self.browser.find_element(By.XPATH, YtbConst.PL_CREATE_PLAYLIST_CONTAINER_XPATH).click()
                playlist_title_textbox = self.browser.find_element(By.XPATH,
                                                                   '/html/body/ytcp-playlist-creation-dialog/ytcp-dialog/tp-yt-paper-dialog/div[2]/div/ytcp-playlist-metadata-editor/div/div[1]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
                self.__write_in_field(playlist_title_textbox, playlist)

                # //*[@id="textbox"]
                time.sleep(YtbConst.USER_WAITING_TIME)
                # //*[@id="create-button"]/div   //*[@id="dialog"]/div[3]/div/ytcp-button[1]/div
                create_playlist_button = self.browser.find_element(By.XPATH, YtbConst.PL_CREATE_BUTTON_XPATH)
                create_playlist_button.click()
                time.sleep(YtbConst.USER_WAITING_TIME)

            time.sleep(YtbConst.USER_WAITING_TIME * 2)
            done_button = self.browser.find_element(By.CLASS_NAME, YtbConst.PL_DONE_BUTTON_CLASS)
            self.browser.execute_script("arguments[0].click();", done_button)  # js注入实现点击
            # done_button.click()

        # Advanced options
        time.sleep(YtbConst.USER_WAITING_TIME)
        self.browser.find_element(By.ID, YtbConst.ADVANCED_BUTTON_ID).click()
        self.logger.debug('Clicked MORE OPTIONS')
        time.sleep(YtbConst.USER_WAITING_TIME)

        # Tags
        tags = self.metadata_dict[YtbConst.VIDEO_TAGS]
        if tags:
            # tags_container = self.browser.find_element(By.ID, Constant.TAGS_CONTAINER_ID)
            self.browser.find_element(By.XPATH, '//*[@id="toggle-button"]/div')  # 展开
            tags_field = self.browser.find_element(By.XPATH, YtbConst.TAGS_INPUT)
            self.__write_in_field(tags_field, ','.join(tags))
            self.logger.debug('The tags were set to \"{}\"'.format(tags))

        self.browser.find_element(By.XPATH, YtbConst.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} one'.format(YtbConst.NEXT_BUTTON))
        time.sleep(YtbConst.USER_WAITING_TIME)
        self.browser.find_element(By.XPATH, YtbConst.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} two'.format(YtbConst.NEXT_BUTTON))
        time.sleep(YtbConst.USER_WAITING_TIME)
        self.browser.find_element(By.XPATH, YtbConst.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} three'.format(YtbConst.NEXT_BUTTON))
        time.sleep(YtbConst.USER_WAITING_TIME)

        schedule = self.metadata_dict[YtbConst.VIDEO_SCHEDULE]
        if schedule:  # 发布时间，暂不设置
            upload_time_object = datetime.strptime(schedule, "%m/%d/%Y, %H:%M")
            self.browser.find_element(By.ID, YtbConst.SCHEDULE_CONTAINER_ID).click()
            self.browser.find_element(By.ID, YtbConst.SCHEDULE_DATE_ID).click()
            self.browser.find_element(By.XPATH, YtbConst.SCHEDULE_DATE_TEXTBOX).clear()
            self.browser.find_element(By.XPATH, YtbConst.SCHEDULE_DATE_TEXTBOX).send_keys(
                datetime.strftime(upload_time_object, "%b %e, %Y"))
            self.browser.find_element(By.XPATH, YtbConst.SCHEDULE_DATE_TEXTBOX).send_keys(Keys.ENTER)
            self.browser.find_element(By.XPATH, YtbConst.SCHEDULE_TIME).click()
            self.browser.find_element(By.XPATH, YtbConst.SCHEDULE_TIME).clear()
            self.browser.find_element(By.XPATH, YtbConst.SCHEDULE_TIME).send_keys(
                datetime.strftime(upload_time_object, "%H:%M"))
            self.browser.find_element(By.XPATH, YtbConst.SCHEDULE_TIME).send_keys(Keys.ENTER)
            self.logger.debug(f"Scheduled the video for {schedule}")
        else:
            self.browser.find_element(By.XPATH, YtbConst.PUBLIC_BUTTON).click()
            self.logger.debug('Made the video {}'.format(YtbConst.PUBLIC_BUTTON))

        # Check status container and upload progress
        self.__wait_loading()
        self.logger.debug('Upload container gone.')

        video_id = self.__get_video_id()

        # done_button = self.browser.find_element(By.ID, Constant.DONE_BUTTON)
        #
        # # Catch such error as
        # # "File is a duplicate of a video you have already uploaded"
        # if done_button.get_attribute('aria-disabled') == 'true':
        #     error_message = self.browser.find_element(By.XPATH, Constant.ERROR_CONTAINER).text
        #     self.logger.error(error_message)
        #     return False, None
        #
        # done_button.click()
        self.logger.debug(
            "Published the video with video_id = {}".format(video_id))
        time.sleep(YtbConst.USER_WAITING_TIME)
        # self.browser.get(Constant.YOUTUBE_URL)
        return True, video_id
