

if __name__ == "__main__":
    print("This is a module. Program exiting...")
    exit()


import configparser, os
from tkinter import messagebox

class conf:
    def __init__(self, title:str, path='config.ini') -> None:
        self.title = title
        self.path = path
        self.config = configparser.ConfigParser()
        self.config['Watcher'] = {
            'Sheet ID' : '',
            'Sheet Name' : '',
            'Column' : 0,
            'Row' : 0,
            'Timer' : 5
        }
        self.config['App'] = {
            'Topmost' : True,
            'Extra Column' : 3,
            'Extra Row' : 3,
            'Notification Timeout' : 5
        }

    def save(self):
        try:
            with open(self.path, 'w') as f:
                self.config.write(f)
        except:
            raise IOError("Unable to save message to config file.\n\nConsider checking file permission.")

    def load(self):
        try:
            if os.path.exists(self.path):
                new_config = configparser.ConfigParser()
                new_config.read(self.path)
                self.config['Watcher']['Sheet ID']          = new_config['Watcher']['Sheet ID']
                self.config['Watcher']['Sheet Name']        = new_config['Watcher']['Sheet Name']
                self.config['Watcher']['Column']            = new_config['Watcher']['Column']
                self.config['Watcher']['Row']               = new_config['Watcher']['Row']
                self.config['Watcher']['Timer']             = new_config['Watcher']['Timer']

                self.config['App']['Topmost']               = new_config['App']['Topmost']
                self.config['App']['Extra Column']          = new_config['App']['Extra Column']
                self.config['App']['Extra Row']             = new_config['App']['Extra Row']
                self.config['App']['Notification Timeout']  = new_config['App']['Notification Timeout']
        except:
            messagebox.showwarning(self.title, "Unable to load config from config file.\n\nConsider checking file permission or its content. Deleting config file will probably solve the issue (this will reset the settings).")
