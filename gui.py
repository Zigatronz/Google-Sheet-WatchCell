

if __name__ == "__main__":
    print("This is a module. Program exiting...")
    exit()

import tkinter as tk
from tkinter import messagebox
from conf import conf
from gsheet import *
import pandas as pd
import pandastable as pt

class gui:
    def __init__(self, config:conf, watcher:sheet_cell_watcher, title:str, icon_path:str) -> None:
        self.config = config
        self.watcher = watcher

        # root window
        self.root = tk.Tk()
        self.root.title(title)

        # window bg color
        win_bg_color = "#252526"
        self.root.configure(bg=win_bg_color)

        # hide on exit
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.hide())

        # position and size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        screen_gap_x, screen_gap_y, win_width, win_height = 50, 75, 400, 535

        x = round(screen_width - win_width - screen_gap_x)
        y = round(screen_height - win_height - screen_gap_y)

        self.root.geometry(f"{win_width}x{win_height}+{x}+{y}")

        # Load the icon image
        icon = tk.PhotoImage(file=icon_path)

        # Set the window icon
        self.root.iconphoto(False, icon)

        # Disable resizing (both width and height)
        self.root.resizable(False, False)

        # Stay top most
        if (self.config.config['App']['Topmost']) == 'True':
            self.root.attributes("-topmost", True)

        # elements

        elements_width = 50

        sid_label = tk.Label(self.root, width=elements_width, text="Sheet ID:", background=win_bg_color, foreground="#FAFAFA", font=("Arial", 11, "bold"))
        sid_label.pack(padx=10, pady=(10, 0))
        sid_var = tk.StringVar()
        sid_entry = tk.Entry(self.root, width=elements_width, textvariable=sid_var)
        sid_entry.pack(padx=10, pady=0)
        sid_var.set(self.config.config['Watcher']['Sheet ID'])

        sna_label = tk.Label(self.root, width=elements_width, text="Sheet name:", background=win_bg_color, foreground="#FAFAFA", font=("Arial", 11, "bold"))
        sna_label.pack(padx=10, pady=(10, 0))
        sna_var = tk.StringVar()
        sna_entry = tk.Entry(self.root, width=elements_width, textvariable=sna_var)
        sna_entry.pack(padx=10, pady=0)
        sna_var.set(self.config.config['Watcher']['Sheet Name'])

        # Empty 3x3
        self.df = pd.DataFrame({
            "1" : ["", "", ""],
            "2" : ["", "", ""],
            "3" : ["", "", ""]
        })
        def get_csv():
            self.df = get_sheet_df(sid_entry.get(), sna_entry.get())
            self.df = get_df_extra_cells(self.df, 3, 3)
            self.table.updateModel(pt.TableModel(self.df))
            self.table.redraw()

        btn_csv = tk.Button(self.root, text="Get CSV", width=33, command=get_csv, font=("Arial", 11, "bold"))
        btn_csv.pack(padx=10, pady=(14, 16))

        self.frame_table = tk.Frame(self.root)
        self.frame_table.pack(padx=46, pady=0)

        self.table = pt.Table(self.frame_table, dataframe=self.df, height=100)
        self.table.show()
        
        def get_cell_pos():
            row = self.table.getSelectedRow()
            col = self.table.getSelectedColumn()
            col_var.set(col + 1)
            row_var.set(row + 1)

        btn_cell_pos = tk.Button(self.root, text="Get cell pos", width=33, command=get_cell_pos, font=("Arial", 11, "bold"))
        btn_cell_pos.pack(padx=10, pady=(12, 0))

        col_label = tk.Label(self.root, width=elements_width, text="Column:", background=win_bg_color, foreground="#FAFAFA", font=("Arial", 11, "bold"))
        col_label.pack(padx=10, pady=(10, 0))
        col_var = tk.StringVar()
        col_entry = tk.Entry(self.root, width=elements_width, textvariable=col_var)
        col_entry.pack(padx=10, pady=0)
        col_var.set(self.config.config['Watcher']['Column'])

        row_label = tk.Label(self.root, width=elements_width, text="Row:", background=win_bg_color, foreground="#FAFAFA", font=("Arial", 11, "bold"))
        row_label.pack(padx=10, pady=(10, 0))
        row_var = tk.StringVar()
        row_entry = tk.Entry(self.root, width=elements_width, textvariable=row_var)
        row_entry.pack(padx=10, pady=0)
        row_var.set(self.config.config['Watcher']['Row'])

        def save():
            try:
                self.config.config['Watcher']['Sheet ID'] = sid_entry.get()
                self.config.config['Watcher']['Sheet Name'] = sna_entry.get()
                self.config.config['Watcher']['Column'] = str(int(col_entry.get()) - 1)
                self.config.config['Watcher']['Row'] = str(int(row_entry.get()) - 1)
                try:
                    self.config.save()
                    messagebox.showinfo(title, "Config saved!")
                    self.watcher.load_config()
                except Exception as e:
                    messagebox.showwarning(repr(e))
            except:
                messagebox.showwarning(title, "Unable to save config.\n\nConsider recheck your input(s).")

        btn_save = tk.Button(self.root, text="Save", width=33, command=save, font=("Arial", 11, "bold"))
        btn_save.pack(padx=10, pady=(25, 16))

    def run_mainloop(self):
        self.root.mainloop()

    def show(self):
        if self.root.state() == "withdrawn":
            self.root.deiconify()

    def hide(self):
        if self.root.state() != "withdrawn":
            self.root.withdraw()
