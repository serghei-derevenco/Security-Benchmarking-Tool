import time
import tkinter as tk
from tkinter import filedialog
from json_to_db import *
from parser import *

class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.parse_btn = tk.Button(self, text="Parse file", fg="yellow", bg="blue", command=self.parse_file)
        self.parse_btn.pack(side="bottom")

        self.choose_btn = tk.Button(self, text="Choose a file", command=self.choose_file)
        self.choose_btn.pack(side="bottom")

    def choose_file(self):
        file_name = filedialog.askopenfilename(initialdir='.', title='Select file', filetypes=(('Audit files', '*.audit'), ('all files', '*.*')))
        print(file_name)

    def parse_file(self):
        print("parsing file started...")
        Parser().push_items_to_json()
        json_to_db()
        time.sleep(1)
        print("parsing file finished!")


window = tk.Tk(className=' Security Benchmarking Tool')
window.geometry("200x200")

