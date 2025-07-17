import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Printer import Printables
from Stor import Storer
import datetime

class ServisLabelApp:
    def __init__(self, root):
        self.printer = Printables()
        self.storer = Storer("data.csv")
        self.root = root
        self.root.title("Servis Label Program")

        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("TFrame", background="#f5f6fa")
        style.configure("TLabel", background="#f5f6fa", font=("Segoe UI", 11))
        style.configure("TEntry", relief="flat", padding=5)
        style.configure("TButton", font=("Segoe UI", 11, "bold"), foreground="#fff", background="#273c75")
        style.map("TButton",
            background=[("active", "#40739e"), ("!active", "#273c75")],
            foreground=[("active", "#fff")]
        )

        main_frame = ttk.Frame(self.root, padding=30, style="TFrame", borderwidth=2, relief="groove")
        main_frame.pack(padx=40, pady=30)

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.device_var = tk.StringVar()
        self.problem_var = tk.StringVar()
        self.accessories_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.numer_kopjesh_var = tk.StringVar()

        fields = [
            ("Name", self.name_var),
            ("Phone", self.phone_var),
            ("Address", self.address_var),
            ("Device", self.device_var),
            ("Problem", self.problem_var),
            ("Accessories", self.accessories_var),
            ("Date Of Arrival", self.date_var),
            ("Number of Copies", self.numer_kopjesh_var)
        ]
        self.numer_kopjesh_var.set("1")  # Default number of copies
        self.date_var.set(datetime.datetime.now().strftime("%Y-%m-%d"))  # Default date

        self.entries = []  # Store entry widgets for navigation

        for idx, (label_text, var) in enumerate(fields):
            ttk.Label(main_frame, text=label_text + ":", style="TLabel").grid(row=idx, column=0, padx=(0,10), pady=8, sticky="e")
            entry = ttk.Entry(main_frame, textvariable=var, width=30, style="TEntry")
            entry.grid(row=idx, column=1, padx=(0,0), pady=8, sticky="w")
            self.entries.append(entry)

        # Bind arrow keys for navigation
        for i, entry in enumerate(self.entries):
            entry.bind("<Up>", lambda e, idx=i: self.focus_entry(idx-1))
            entry.bind("<Down>", lambda e, idx=i: self.focus_entry(idx+1))
            entry.bind("<Left>", lambda e, idx=i: self.focus_entry(idx-1))
            entry.bind("<Right>", lambda e, idx=i: self.focus_entry(idx+1))

        submit_btn = ttk.Button(main_frame, text="Submit", command=self.submit, style="TButton")
        submit_btn.grid(row=len(fields), column=0, pady=15, sticky="ew")

        load_btn = ttk.Button(main_frame, text="Load From memory", command=self.load_from_memory, style="TButton")
        load_btn.grid(row=len(fields), column=1, pady=15, sticky="ew")

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

    def focus_entry(self, idx):
        if 0 <= idx < len(self.entries):
            self.entries[idx].focus_set()

    def submit(self):
        Name = self.name_var.get() if self.name_var.get() else None
        Phone = self.phone_var.get() if self.phone_var.get() else None
        Address = self.address_var.get() if self.address_var.get() else None
        Device = self.device_var.get() if self.device_var.get() else None
        Problem = self.problem_var.get() if self.problem_var.get() else None
        Accessories = self.accessories_var.get().split(",") if self.accessories_var.get() else []
        DateOfArrival = self.date_var.get() if self.date_var.get() else datetime.datetime.now().strftime("%Y-%m-%d")
        numer_kopjesh = int(self.numer_kopjesh_var.get())
        ID = self.storer.addAllDatta(Name, Phone, Address, Device, Problem, Accessories, DateOfArrival)
        receipt_text = self.printer.Formaterer(ID, Name, Phone, Address, Device, Problem, Accessories, DateOfArrival)
        for i in range(numer_kopjesh):
            self.printer.printOnPaper(receipt_text)
        # Clear entry boxes
        self.name_var.set("")
        self.phone_var.set("")
        self.address_var.set("")
        self.device_var.set("")
        self.problem_var.set("")
        self.accessories_var.set("")
        self.numer_kopjesh_var.set("1")
        self.date_var.set(datetime.datetime.now().strftime("%Y-%m-%d"))

    def open_data_table_window(self):
        data_window = tk.Toplevel(self.root)
        data_window.title("Data Table App")
        data_window.geometry("900x400")
        data_window.configure(bg="#f5f6fa")

        style = ttk.Style(data_window)
        style.configure("TFrame", background="#f5f6fa")
        style.configure("TLabel", background="#f5f6fa", font=("Segoe UI", 11))
        style.configure("TEntry", relief="flat", padding=5)
        style.configure("TButton", font=("Segoe UI", 11, "bold"), foreground="#fff", background="#273c75")
        style.map("TButton",
            background=[("active", "#40739e"), ("!active", "#273c75")],
            foreground=[("active", "#fff")]
        )

        main_frame = ttk.Frame(data_window, style="TFrame")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        data = self.storer.load()

        columns = ["ID", "Name", "Phone"," Address", "Device","Problem","Acessories","Date Of Arrival"]
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
        for idx, col in enumerate(columns):
            tree.heading(col, text=col)
            tree.column(col, width=90, anchor="center")
        for row in data:
            tree.insert("", "end", values=row)
        tree.pack(pady=10, fill="x")

        entry_frame = ttk.Frame(main_frame, style="TFrame")
        entry_frame.pack(pady=10)
        ttk.Label(entry_frame, text="Number of copies:", style="TLabel").pack(side="left")
        copies_entry = ttk.Entry(entry_frame, width=10, style="TEntry")
        copies_entry.insert(0, "1")
        copies_entry.pack(side="left", padx=5)
        

        def Delete():
            selected = tree.selection()
            if not selected:
                tk.messagebox.showwarning("No selection", "Please select a row in the table.")
                return
            confirm = tk.messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected row?")
            if not confirm:
                return
            item = selected[0]
            item_values = tree.item(item, "values")
            ID = item_values[0]
            self.storer.delete(ID)
            tree.delete(item)

        def on_submit():
            selected = tree.selection()
            if not selected:
                tk.messagebox.showwarning("No selection", "Please select a row in the table.")
                return
            row_data = list(tree.item(selected[0], "values"))

            accessories_str = row_data[6]
            accessories_str = accessories_str.strip("[]")
            accessories_list = [item.strip().strip("'").strip('"') for item in accessories_str.split(",") if item.strip()]
            row_data[6] = accessories_list
            receipt_text = self.printer.Formaterer(row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5], row_data[6], row_data[7])
            for i in range(int(copies_entry.get()) if copies_entry.get() != None else 1):
                self.printer.printOnPaper(receipt_text)
                pass

                # Frame to hold both buttons side by side
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(pady=10)

        submit_btn = ttk.Button(button_frame, text="Submit", style="TButton", command=on_submit)
        submit_btn.pack(side="left", padx=5)

        delete_button = ttk.Button(button_frame, text="Delete", style="TButton", command=Delete)
        delete_button.pack(side="left", padx=5)
    def load_from_memory(self):
        self.open_data_table_window()
if __name__ == "__main__":
    root = tk.Tk()
    app = ServisLabelApp(root)
    root.mainloop()