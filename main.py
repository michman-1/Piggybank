import customtkinter as ctk
import db

from Win1_main import Left_Segment, Right_Segment

class MainWindow(ctk.CTk):
    def __init__(self, conn):
        super().__init__()
        self.geometry("1000x700")
        self.title("Piggybank Organizer")
        self.conn = conn
        self.currency = "zł"
        self.modules = {r["name"]: r["id"] for r in conn.execute("SELECT id, name FROM module")}
        self.accounts = {r["name"]: r["id"] for r in conn.execute("SELECT id, name FROM account")}

        
        self.left_frame = Left_Segment(self)
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.right_frame = Right_Segment(self)
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
     

    def on_close(self):
        self.conn.commit()
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    MainWindow(db.connect()).mainloop()