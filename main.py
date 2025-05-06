
from tray import tray
from gui import gui
from gsheet import *
from conf import conf
from notify import notify

def main():
    icon_path = "icon.png"
    icon_path_ico = "icon.ico"
    title = "Google Sheet WatchCell"
    config_path = "config.ini"

    config = conf(title=title, path=config_path)
    config.load()
    noti = notify(title=title, icon_path=icon_path_ico, config=config)
    watcher = sheet_cell_watcher(config=config, noti=noti)
    watcher.start()
    ui = gui(config, watcher=watcher, title=title, icon_path=icon_path)
    tray_icon = tray(ui, watcher, icon_path=icon_path, title=title)
    ui.run_mainloop()

if __name__ == "__main__":
    main()
