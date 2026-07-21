from tkinter import *

class clickerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Virus Clicker")

        self.container = Frame(self.root)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.rowconfigure(0, minsize=40, weight=1)

        self.create_widgets()

    def create_widgets(self):

        # Upgrade menu, Button values to be changed for better game pacing.

        self.create_upgrade_frame = Frame(self.container)

        Label(self.root, text="Upgrades")
        
        Label(self.root, text="Auto-closer:")
        self.upgrade_btn1 = Button(self.create_upgrade_frame, text="10")

        Label(self.root, text="Bigger Windows:")
        self.upgrade_btn2 = Button(self.create_upgrade_frame, text="100")

        Label(self.root, text=":")
        self.upgrade_btn3 = Button(self.create_upgrade_frame, text="250")

        Label(self.root, text=":")
        self.upgrade_btn4 = Button(self.create_upgrade_frame, text="1000")

        Label(self.root, text=":")
        self.upgrade_btn5 = Button(self.create_upgrade_frame, text="2500")

        Label(self.root, text="Anti-virus:")
        self.upgrade_btn6 = Button(self.create_upgrade_frame, text="10000")
        
root = Tk()
run = clickerGUI(root)
root.mainloop()