from decimal import Decimal, InvalidOperation
from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk

import db

class Frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_propagate(False)

    @property
    def app(self):
        return self.winfo_toplevel()
        
class Left_Segment(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=300, height=700, **kwargs)
        
        self.WindowTitle = ctk.CTkLabel(self, text="Operations")
        self.WindowTitle.grid(row=0, column=0, padx=20)

        self.WindowSelect = ctk.CTkSegmentedButton(self, values=["1", "2", "3"])
        self.WindowSelect.grid(row=0, column=1, padx=20, pady=10)
        self.WindowSelect.set("1")  

        self.FormField1_label = ctk.CTkLabel(self, text="Value:")
        self.FormField1_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.FormField1_entry = ctk.CTkEntry(self)
        self.FormField1_entry.grid(row=4, column=0, padx=20)

        self.FormField2_label = ctk.CTkLabel(self, text="Savings Goal:")
        self.FormField2_label.grid(row=5, column=0, padx=20, pady=10,sticky="w")
        self.FormField2_optionmenu = ctk.CTkOptionMenu(self, values=list(self.app.modules) or ["No goals available"])
        self.FormField2_optionmenu.grid(row=6, column=0, padx=20)


        self.FormField3_label = ctk.CTkLabel(self, text="Account:")
        self.FormField3_label.grid(row=7, column=0, padx=20, pady=10, sticky="w")
        self.FormField3_optionmenu = ctk.CTkOptionMenu(self, values=list(self.app.accounts) or ["No accounts available"])
        self.FormField3_optionmenu.grid(row=8, column=0, padx=20)

        self.FormField4_label = ctk.CTkLabel(self, text="Comment:")
        self.FormField4_label.grid(row=9, column=0, padx=20, pady=10, sticky="w")
        self.FormField4_entry = ctk.CTkEntry(self, placeholder_text = "Optional")
        self.FormField4_entry.grid(row=10, column=0, padx=20)

        self.SubmitWithdraw_button = ctk.CTkButton(self, text="Withdraw", command=lambda: self.submit_transaction(-1))
        self.SubmitWithdraw_button.grid(row=11, column=0, padx=20, pady=10, sticky="s")
        self.SubmitDeposit_button = ctk.CTkButton(self, text="Deposit", command=lambda: self.submit_transaction(1))
        self.SubmitDeposit_button.grid(row=11, column=1, padx=20, pady=10, sticky="s")

    def submit_transaction(self, sign):
        raw = self.FormField1_entry.get().strip().replace(",", ".")
        try:
            cents = round(Decimal(raw) * 100)
        except InvalidOperation:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")
            return
        if cents <= 0:
            messagebox.showerror("Error", "Please enter a positive amount.")
            return
        
        module_id = self.app.modules[self.FormField2_optionmenu.get()]
        account_id = self.app.accounts[self.FormField3_optionmenu.get()]
        comment = self.FormField4_entry.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db.submit_transaction(self.app.conn, sign * cents, module_id, account_id, comment, date)
        self.FormField1_entry.delete(0, "end")
        self.FormField4_entry.delete(0, "end")
        self.app.event_generate("<<SumsChanged>>")

class Right_Segment(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=700, height=700, **kwargs)

        self.sum_display = self.SumsDisplay(self, width=680, height=200)
        self.sum_display.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    class SumsDisplay(Frame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            self.grid_propagate(False)

            self.boxes = []
            for i in range(3):
                box = self.Sumbox(self, width=200, height=150)
                box.grid(row=0, column=i, padx=10, pady=10)
                self.boxes.append(box)

        class Sumbox(Frame):
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)
                self.grid_propagate(False)

                self.module_select = ctk.CTkOptionMenu(self, values=list(self.app.modules) or ["No goals available"],command=self.update_sum)
                self.module_select.grid(row=0, column=0, padx=20, pady=10, sticky="nw")
                self.Current_module = self.module_select.get()

                self.sum_label = ctk.CTkLabel(self, text="Current sum:")
                self.sum_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
                self.sum = ctk.CTkLabel(self, text="")
                self.sum.grid(row=2, column=0, padx=20, pady=10, sticky="w")
                self.update_sum(self.module_select.get())
                self.app.bind("<<SumsChanged>>", self.refresh, add="+")

            def refresh(self, event=None):
                self.update_sum(self.module_select.get())

            def update_sum(self, module_name):
                module_id = self.app.modules.get(module_name)
                row = None
                if module_id is not None:
                    row = self.app.conn.execute(
                        "SELECT sum FROM module WHERE id = ?", (module_id,)
                    ).fetchone()
                cents = row["sum"] if row else 0
                self.sum.configure(text=f"{cents / 100:.2f} {self.app.currency}")