

if __name__ == "__main__":
    print("This is a module. Program exiting...")
    exit()


import pandas as pd
from time import sleep
import threading
from notify import notify
from conf import conf

def get_sheet_df(sheet_id : str, sheet_name : str) -> pd.DataFrame:
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    url = url.replace(" ", "%20")   # remove whitespace
    df = pd.read_csv(url, header=None)
    new_df = pd.DataFrame()
    i = 0
    for col in df.columns:
        i += 1
        new_df[str(i)] = df[col]
    return new_df

def get_df_extra_cells(df : pd.DataFrame, rows : int = 3, columns : int = 3) -> pd.DataFrame:
    # Add empty rows
    df = df.reindex(range(df.shape[0] + rows))

    # Add empty columns
    tc = len(df.columns)
    for i in range(columns):
        df[f'{ tc + i + 1 }'] = None

    return df

class sheet_cell_watcher:
    def __init__(self, config:conf, noti:notify) -> None:
        self.config = config
        self.noti = noti
        
        self.running = False
        self.previous_cell_value = None
        self.first_run = True

        self.sheet_id   = None
        self.sheet_name = None
        self.column     = None
        self.row        = None
        self.timer      = None
        self.load_config()

    def load_config(self):
        if (self.sheet_id      != self.config.config['Watcher']['Sheet ID']):
            self.sheet_id       = self.config.config['Watcher']['Sheet ID']
            self.first_run      = True
            self.previous_cell_value = ''
            
        if (self.sheet_name    != self.config.config['Watcher']['Sheet Name']):
            self.sheet_name     = self.config.config['Watcher']['Sheet Name']
            self.first_run      = True
            self.previous_cell_value = ''
            
        if (self.column        != int(self.config.config['Watcher']['Column'])):
            self.column         = int(self.config.config['Watcher']['Column'])
            self.first_run      = True
            self.previous_cell_value = ''
            
        if (self.row           != int(self.config.config['Watcher']['Row'])):
            self.row            = int(self.config.config['Watcher']['Row'])
            self.first_run      = True
            self.previous_cell_value = ''
            
        self.timer              = int(self.config.config['Watcher']['Timer'])

    def mainloop(self):
        while self.running:
            sleep(self.timer)
            if self.sheet_id and self.sheet_name and self.column != '' and self.row != '':
                df = get_sheet_df(self.sheet_id, self.sheet_name)
                try:
                    cell_val = df.iloc[self.row, self.column]
                except IndexError as e:
                    # the cell is not exist yet
                    if self.first_run == True:
                        self.first_run = False
                        continue
                    else:
                        cell_val = ''
                if cell_val != self.previous_cell_value:
                    if self.first_run:
                        self.first_run = False
                    else:
                        self.noti.notify("Cell changed!", f"Previous value: {self.previous_cell_value}\nNew value: {cell_val}")
                    self.previous_cell_value = cell_val

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.mainloop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
