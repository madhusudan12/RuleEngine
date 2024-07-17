

class ActionExecutor:
    def __init__(self, email_service):
        self.email_service = email_service

    def execute_actions(self, email, actions):
        for action in actions:
            action_type = action['action']
            if action_type == 'mark_as_read':
                MarkAsReadAction(self.email_service).execute(email)
            elif action_type == 'move_message':
                label_id = action['params']['label_id']
                MoveMessageAction(self.email_service, label_id).execute(email)