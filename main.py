import customtkinter as ctk
import db

from Win1_main import Left_Frame

class MainWindow(ctk.CTk):
    def __init__(self, conn):
        super().__init__()
        self.geometry("1000x700")
        self.title("Piggybank Organizer")
        self.conn = conn

        
        self.left_frame = Left_Frame(self, conn)
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def on_close(self):
        self.conn.commit()
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    MainWindow(db.connect()).mainloop()