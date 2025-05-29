import tkinter as tk
from tkinter import ttk

class LedgerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Ledger")

        self.entries = []

        # Input Frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Bill Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Amount:").grid(row=0, column=2)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=0, column=3)

        tk.Button(input_frame, text="Add", command=self.add_entry).grid(row=0, column=4, padx=10)

        # Ledger List
        self.tree = ttk.Treeview(root, columns=("Name", "Amount"), show="headings")
        self.tree.heading("Name", text="Bill Name")
        self.tree.heading("Amount", text="Amount")
        self.tree.pack(pady=10)

        self.tree.bind('<Double-1>', self.edit_entry)

    def add_entry(self):
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        if name and amount:
            self.entries.append((name, amount))
            self.tree.insert("", "end", values=(name, amount))
            self.name_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)

    def edit_entry(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            old_name, old_amount = item["values"]

            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Entry")

            tk.Label(edit_window, text="New Name:").grid(row=0, column=0)
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, old_name)
            name_entry.grid(row=0, column=1)

            tk.Label(edit_window, text="New Amount:").grid(row=1, column=0)
            amount_entry = tk.Entry(edit_window)
            amount_entry.insert(0, old_amount)
            amount_entry.grid(row=1, column=1)

            def save_edit():
                new_name = name_entry.get()
                new_amount = amount_entry.get()
                self.tree.item(selected[0], values=(new_name, new_amount))
                edit_window.destroy()

            tk.Button(edit_window, text="Save", command=save_edit).grid(row=2, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = LedgerApp(root)
    root.mainloop()
