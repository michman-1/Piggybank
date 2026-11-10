from decimal import Decimal, InvalidOperation
from datetime import datetime

import customtkinter as ctk

import db

class Left_Frame(ctk.CTkFrame):
    def __init__(self, master, conn, **kwargs):
        super().__init__(master, width=300, height=700, **kwargs)
        self.conn = conn
        self.grid_propagate(False)    

        self.modules = {r["name"]: r["id"] for r in conn.execute("SELECT id, name FROM module")}
        self.accounts = {r["name"]: r["id"] for r in conn.execute("SELECT id, name FROM account")}

        
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
        self.FormField2_optionmenu = ctk.CTkOptionMenu(self, values=list(self.modules) or ["No goals available"])
        self.FormField2_optionmenu.grid(row=6, column=0, padx=20)


        self.FormField3_label = ctk.CTkLabel(self, text="Account:")
        self.FormField3_label.grid(row=7, column=0, padx=20, pady=10, sticky="w")
        self.FormField3_optionmenu = ctk.CTkOptionMenu(self, values=list(self.accounts) or ["No accounts available"])
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
        try:
            cents = round(Decimal(self.FormField1_entry.get().replace(",", ".")) * 100)
        except InvalidOperation:
            self.showError("Invalid input. Please enter a valid number.")
            return
        if cents <= 0:
            self.showError("Please enter a positive amount.")
            return

        module_id = self.modules[self.FormField2_optionmenu.get()]
        account_id = self.accounts[self.FormField3_optionmenu.get()]
        comment = self.FormField4_entry.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        db.submit_transaction(self.conn, sign * cents, module_id, account_id, comment, date)
        self.FormField1_entry.delete(0, "end")
        self.FormField4_entry.delete(0, "end")