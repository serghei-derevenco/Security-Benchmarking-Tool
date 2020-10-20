import subprocess
import tkinter as tk

from json_to_db import *
from parser import Parser
from datetime import datetime
from select_from_db import get_all_description_info, searched_item_to_dict, selected_item_to_dict

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.check_button = tk.Button(self, text='Check system', fg="yellow", bg="green", command=self.check_window)
        self.quit_btn = tk.Button(self, text="QUIT", fg="white", bg="red", command=self.master.destroy)
        self.entry = tk.Entry(self)
        self.search = tk.Label(self, text="Search:")
        self.select_btn = tk.Button(self, text='Select all', fg="green", command=self.select_all_items)
        self.unselect_btn = tk.Button(self, text='Unselect all', fg="red", command=self.unselect_all_items)
        self.export_all_btn = tk.Button(self, text='Export all items in json', fg="yellow", bg="blue", command=self.selected_items_to_json)
        self.export_selected = tk.Button(self, text='Export selected items to json', fg="yellow", bg="blue", command=self.searched_items_to_json)

        self.quit_btn.pack(side="right", padx=40)
        self.check_button.pack(side="right", padx=30)
        self.export_selected.pack(side="right", padx=20)
        self.entry.pack(side="right")
        self.search.pack(side="right")
        self.select_btn.pack(side="left", padx=15)
        self.unselect_btn.pack(side="left", padx=15)
        self.export_all_btn.pack(side="left", padx=15)

        self._list = tk.Listbox(window, selectmode="multiple")
        self._list.pack(expand="yes", fill="both")

        x = get_all_description_info()

        for each_item in range(len(x)):
            self._list.insert(tk.END, x[each_item])

    def select_all_items(self):
        self._list.select_set(0, tk.END)

    def unselect_all_items(self):
        self._list.selection_clear(0, tk.END)

    def return_all_items(self):
        all_items = str(self._list.curselection()).replace('(', '').replace(')', '').split(',')
        return all_items

    def error_message(self):
        error_window = tk.Tk()
        error_window.geometry("500x150")
        error_window.resizable(0, 0)
        error_window.title('Error !')
        # Adding some space from top
        tk.Label(error_window, text='').pack()
        tk.Label(error_window, text='').pack()
        error_label = tk.Label(error_window, text=f"No audit's found by {self.entry.get().strip()}")
        error_label.pack()
        self.entry.delete(0, 'end')
        close_button = tk.Button(error_window, text='Close', fg="white", bg="red", command=error_window.destroy)
        close_button.pack()

    def result_message(self):
        now = datetime.now()
        result_window = tk.Tk()
        result_window.geometry("500x150")
        result_window.resizable(0, 0)
        result_window.title('Searched info')

        # Adding some space from top
        tk.Label(result_window, text='').pack()
        tk.Label(result_window, text='').pack()
        result_label = tk.Label(result_window, text=f"Audits found by {self.entry.get().strip()} was exported to "f"{now.strftime(f'%d_%m_%Y_%H_%M_{self.entry.get().strip()}')}.json")
        result_label.pack()
        close_btn = tk.Button(result_window, text='Close', fg="white", bg="red", command=result_window.destroy)
        close_btn.pack()

    def selected_items_to_json(self):
        if len(self.return_all_items()) == 2 and self.return_all_items()[1] == '':
            now = datetime.now()
            with open(f'{now.strftime("%d_%m_%Y_%H_%M_%s")}.json', 'w') as file_open:
                json.dump(selected_item_to_dict(int(self.return_all_items()[0])), file_open, indent=2)
        else:
            items = []
            for item in self.return_all_items():
                items.append(selected_item_to_dict(int(item)))

            now = datetime.now()
            with open(f'{now.strftime("%d_%m_%Y_%H_%M_%s")}.json', 'w') as file_open:
                json.dump(items, file_open, indent=2)

    def searched_items_to_json(self):
        items = []
        if len(searched_item_to_dict(self.entry.get().strip())) == 0:
            self.error_message()
        else:
            self.result_message()
            search = self.entry.get().strip()
            for item in searched_item_to_dict(self.entry.get().strip()):
                items.append(item)

            now = datetime.now()
            with open(f'{now.strftime(f"%d_%m_%Y_%H_%M_{search}")}.json', 'w') as file_open:
                json.dump(items, file_open, indent=2)
            self.entry.delete(0, 'end')

    def check_items(self):
        with open('tmp.json', 'r') as json_file:
            data = json.load(json_file)

        audit_result = []

        for item in data:
            for i in item:
                if i == 'cmd':
                    if item[i] != 'none' and 'sudo' not in item[i]:
                        try:
                            audit_result.append(f"{item['description']} - {subprocess.run(args=['sudo', 'bash', item[i]], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')}\n")
                        except subprocess.CalledProcessError as error:
                            pass

        output = ""
        for i in audit_result:
            output += i

        results = output.split('\n')

        return results

    def enforce_items(self):
        items = self.check_items()
        for item in items:
            if item == 'none':
                try:
                    subprocess.run(args=['sudo', item], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
                except subprocess.CalledProcessError as error:
                    pass

        x = items

        enforce_window = tk.Tk()
        enforce_window.geometry("1260x740+10+10")
        enforce_window.resizable(True, True)
        enforce_window.title("Enforced items")

        rollback_btn = tk.Button(enforce_window, text="Rallback", fg="white", bg="blue", command=self.rollback_items)
        rollback_btn.pack(side="top")

        _list = tk.Listbox(enforce_window, selectmode="multiple")
        _list.pack(expand="yes", fill="both")

        for each_item in range(len(x)):
            _list.insert(tk.END, x[each_item])

        enforce_window.mainloop()

    def rollback_items(self):
        rollback_window = tk.Tk()
        rollback_window.geometry("1260x740+10+10")
        rollback_window.resizable(True, True)
        rollback_window.title("Rollback result")

        _list = tk.Listbox(rollback_window, selectmode="multiple")
        _list.pack(expand="yes", fill="both")

        x = self.check_items()

        for each_item in range(len(x)):
            _list.insert(tk.END, x[each_item])

        rollback_window.mainloop()

    def check_window(self):
        check_window = tk.Tk()
        check_window.geometry("1260x740+10+10")
        check_window.resizable(True, True)
        check_window.title("Check results")

        _list = tk.Listbox(check_window, selectmode="multiple")
        _list.pack(expand="yes", fill="both")

        enforce_btn = tk.Button(check_window, text="Enforce", fg="white", bg="red", command=self.enforce_items)
        enforce_btn.pack(side="top")

        x = self.check_items()

        for each_item in range(len(x)):
            _list.insert(tk.END, x[each_item])

        check_window.mainloop()

window = tk.Tk(className=' Security Benchmarking Tool')
window.geometry("1260x740+10+10")
window.resizable(True, True)

Parser().push_items_to_json()
json_to_db()

app = App(master=window)
app.mainloop()
