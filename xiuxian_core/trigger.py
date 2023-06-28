import re
from typing import Literal, Callable

from xiuxian_core.models import Event


def _check_command(command: str, msg: str) -> bool:
    if msg.startswith(command):
        return True
    return False


def _check_keyword(keyword: str, msg: str) -> bool:
    if keyword in msg:
        return True
    return False


def _check_file(file_type: str, ev: Event) -> bool:
    if ev.file:
        if ev.file_name and ev.file_name.split('.')[-1] == file_type:
            return True
    return False


def _check_regex(pattern: str, msg: str) -> bool:
    command_list = re.findall(pattern, msg)
    if command_list:
        return True
    return False


def _check_fullmatch(keyword: str, msg: str) -> bool:
    if msg == keyword:
        return True
    return False


def _check_suffix(suffix: str, msg: str) -> bool:
    if msg.endswith(suffix) and not _check_fullmatch(suffix, msg):
        return True
    return False


def _check_prefix(prefix: str, msg: str) -> bool:
    if msg.startswith(prefix) and not _check_fullmatch(prefix, msg):
        return True
    return False


class Trigger:
    """
    触发器，用于匹配消息并执行函数。
    """
    def __init__(
            self,
            type: Literal[
                'prefix',
                'suffix',
                'keyword',
                'fullmatch',
                'command',
                'file',
                'regex',
            ],
            keyword: str,
            func: Callable,
            block: bool = False,
            to_me: bool = False,
    ):
        self.type = type
        self.keyword = keyword
        self.func = func
        self.block = block
        self.to_me = to_me

    def check_command(self, ev: Event) -> bool:
        """
        检查是否是命令
        :param ev:
        :return:
        """
        msg = ev.raw_text
        if self.to_me:
            if ev.is_tome:
                pass
            else:
                return False
        if self.type == 'file':
            return _check_file(self.keyword, ev)
        return getattr(self, f'_check_{self.type}')(self.keyword, msg)

    def _check_prefix(self, prefix: str, msg: str) -> bool:
        if msg.startswith(prefix) and not self._check_fullmatch(prefix, msg):
            return True
        return False

    @staticmethod
    def _check_command(command: str, msg: str) -> bool:
        """
        检查是否是命令
        :param command:
        :param msg:
        :return:
        """
        if msg.startswith(command):
            return True
        return False

    def _check_suffix(self, suffix: str, msg: str) -> bool:
        """
        检查是否是后缀
        :param suffix:
        :param msg:
        :return:
        """
        if msg.endswith(suffix) and not self._check_fullmatch(suffix, msg):
            return True
        return False

    @staticmethod
    def _check_keyword(keyword: str, msg: str) -> bool:
        """
        检查是否是关键词
        :param keyword:
        :param msg:
        :return:
        """
        if keyword in msg:
            return True
        return False

    @staticmethod
    def _check_fullmatch(keyword: str, msg: str) -> bool:
        """
        检查是否是全匹配
        :param keyword:
        :param msg:
        :return:
        """
        if msg == keyword:
            return True
        return False

    @staticmethod
    def _check_file(file_type: str, ev: Event) -> bool:
        """
        检查是否是文件
        :param file_type:
        :param ev:
        :return:
        """
        if ev.file:
            if ev.file_name and ev.file_name.split('.')[-1] == file_type:
                return True
        return False

    @staticmethod
    def _check_regex(pattern: str, msg: str) -> bool:
        """
        检查是否为正则
        :param pattern:
        :param msg:
        :return:
        """
        command_list = re.findall(pattern, msg)
        if command_list:
            return True
        return False

    async def get_command(self, msg: Event) -> Event:
        """
        获取命令
        :param msg:
        :return:
        """
        if self.type != 'regex':
            msg.command = self.keyword
            msg.text = msg.raw_text.replace(self.keyword, '')
        else:
            command_list = re.findall(self.keyword, msg.raw_text)
            msg.command = '|'.join(command_list)
            text_list = re.split(self.keyword, msg.raw_text)
            msg.text = '|'.join(text_list)
        return msg
