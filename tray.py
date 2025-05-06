

if __name__ == "__main__":
    print("This is a module. Program exiting...")
    exit()


from pystray import Icon, MenuItem, Menu
from PIL import Image
import threading
from gui import gui
from gsheet import *
from plyer import notification
from conf import conf

class tray:
    def __init__(self, ui:gui, watcher:sheet_cell_watcher, icon_path:str, title:str) -> None:
        self.ui = ui
        self.watcher = watcher
        self.title = title
        self.icon_path = icon_path

        # Create a menu for the tray icon
        menu = Menu(
                MenuItem("Open setting", self.show_ui),
                MenuItem("Exit", self.exit_action)
            )

        # Create the tray icon
        icon_image = Image.open(self.icon_path)
        self.tray_icon = Icon(title, icon_image, menu=menu)

        # Run the tray icon
        self.thread = threading.Thread(target = self.tray_icon.run, daemon=True)
        self.thread.start()

    def show_ui(self):
        self.ui.show()
        
    def exit_action(self):
        self.watcher.stop()
        self.ui.root.quit()
        self.tray_icon.stop()


