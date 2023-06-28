from typing import Any, List, Literal, Optional
from msgspec import Struct


class Message(Struct):
    """
    Message is the base class for all messages.
    """
    type: Optional = None
    data: Optional = None


class MessageReceive(Struct):
    """
    MessageReceive is the base class for all messages received by the client.
    """
    bot_id: str = 'Bot'
    bot_self_id: str = ''
    msg_id: str = ''
    user_type: Literal['group', 'direct', 'channel', 'sub_channel'] = 'group'
    user_id: str = ''
    user_pm: int = 3
    group_id: Optional[str] = None
    content: List[Message] = []


class Event(MessageReceive):
    """
    Event is the base class for all events.
    """
    raw_text: str = ''
    command: str = ''
    text: str = ''
    image: Optional[str] = None
    at: Optional[str] = None
    image_list: List[Any] = []
    at_list: List[Any] = []
    is_tome: bool = False
    reply: Optional[str] = None
    file_name: Optional[str] = None
    file: Optional[str] = None
    file_type: Optional[Literal['url', 'base64']] = None


class MessageSend(Struct):
    """
    MessageSend is the base class for all messages sent by the client.
    """
    bot_id: str = 'Bot'
    bot_self_id: str = ''
    msg_id: str = ''
    target_type: Optional[str] = None
    target_id: Optional[str] = None
    content: Optional[List[Message]] = None

