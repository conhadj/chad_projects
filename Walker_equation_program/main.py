# main.py
import customtkinter as ctk
from ui import MainUI

def main():
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Walker Equation Program")
    
    main_ui = MainUI(app)
    main_ui.pack(expand=True, fill="both")
    
    app.mainloop()

if __name__ == "__main__":
    main()
