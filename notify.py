

if __name__ == "__main__":
    print("This is a module. Program exiting...")
    exit()


from plyer import notification
from conf import conf

class notify:
    def __init__(self, title:str, icon_path:str, config:conf) -> None:
        self.title = title
        self.icon_path = icon_path
        self.config = config

    def notify(self, header:str, msg:str):
        notification.notify(
            title       = header,
            message     = msg,
            app_name    = self.title,
            app_icon    = self.icon_path,
            timeout     = int(self.config.config['App']['Notification Timeout'])
        )
