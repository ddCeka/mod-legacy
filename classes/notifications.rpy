
init -1 python:
    class modNotifications(NonPicklable):
        def __init__(self):
            self.notifications = []
        
        def add(self, **kwargs):
            self.notifications.append(modNotification(self, **kwargs))
            renpy.restart_interaction()
        
        def remove(self, notif):
            if notif in self.notifications:
                self.notifications.remove(notif)
                renpy.restart_interaction()

    class modNotification(NonPicklable):
        def __init__(self, notifCls, label, text=None, action=None):
            self.notifCls = notifCls
            self.label = label
            self.text = text
            self.action = action
        
        def close(self):
            self.notifCls.remove(self)
        
        def __call__(self):
            if self.action:
                if isinstance(self.action, list):
                    [action() for action in self.action]
                else:
                    self.action()
            self.close()
