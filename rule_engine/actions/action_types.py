from enum import Enum


class ActionTypes(Enum):
    MARK_AS_READ = "mark_as_read"
    MARK_AS_UNREAD = "mark_as_unread"
    MOVE_MESSAGE = "move_message"