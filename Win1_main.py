import customtkinter as ctk

class Left_Frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=300, height=700, **kwargs)
        self.grid_propagate(False)    

        
        self.WindowTitle = ctk.CTkLabel(self, text="Operacje")
        self.WindowTitle.grid(row=0, column=0, padx=20)

        self.WindowSelect = ctk.CTkSegmentedButton(self, values=["1", "2", "3"])
        self.WindowSelect.grid(row=0, column=1, padx=20, pady=10)
        self.WindowSelect.set("1")  

        self.FormField1_label = ctk.CTkLabel(self, text="Wartość:")
        self.FormField1_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.FormField1_entry = ctk.CTkEntry(self)
        self.FormField1_entry.grid(row=4, column=0, padx=20)

        self.FormField2_label = ctk.CTkLabel(self, text="Cel oszczędnościowy:")
        self.FormField2_label.grid(row=5, column=0, padx=20, pady=10,sticky="w")
        self.FormField2_optionmenu = ctk.CTkOptionMenu(self, values=["Moduł 1", "Moduł 2", "Moduł 3"])
        self.FormField2_optionmenu.grid(row=6, column=0, padx=20)


        self.FormField3_label = ctk.CTkLabel(self, text="Konto:")
        self.FormField3_label.grid(row=7, column=0, padx=20, pady=10, sticky="w")
        self.FormField3_optionmenu = ctk.CTkOptionMenu(self, values=["Konto 1", "Konto 2", "Konto 3"])
        self.FormField3_optionmenu.grid(row=8, column=0, padx=20)

        self.FormField4_label = ctk.CTkLabel(self, text="Komentarz:")
        self.FormField4_label.grid(row=9, column=0, padx=20, pady=10, sticky="w")
        self.FormField4_entry = ctk.CTkEntry(self, placeholder_text = "Opcjonalne")
        self.FormField4_entry.grid(row=10, column=0, padx=20)

        self.SubmitWithdraw_button = ctk.CTkButton(self, text="Wypłać", command=self.submit_withdraw)
        self.SubmitWithdraw_button.grid(row=11, column=0, padx=20, pady=10, sticky="s")
        self.SubmitDeposit_button = ctk.CTkButton(self, text="Wpłać", command=self.submit_deposit)
        self.SubmitDeposit_button.grid(row=11, column=1, padx=20, pady=10, sticky="s")
