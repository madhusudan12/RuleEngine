from rule_engine.actions.actions import MarkAsReadAction, MoveMessageAction, MarkAsUnreadAction, EmailAction
from rule_engine.actions.action_types import ActionTypes


class ActionFactory:
    def __init__(self, email_service):
        self.email_service = email_service

    def create_action(self, action_data) -> EmailAction:
        action_type = action_data['action']
        if action_type == ActionTypes.MARK_AS_READ.value:
            return MarkAsReadAction(self.email_service)
        elif action_type == ActionTypes.MARK_AS_UNREAD.value:
            return MarkAsUnreadAction(self.email_service)
        elif action_type == ActionTypes.MOVE_MESSAGE.value:
            label_id = action_data['params']['label_id']
            return MoveMessageAction(self.email_service, label_id)
        else:
            raise ValueError(f"Unsupported action type: {action_type}")
