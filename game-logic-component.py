from tkinter import *

TITLE_FONT = ("Arial", 14, "bold")

class clickerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Virus Clicker")

        self.currency = 0
        self.click = 1
        self.cps = 0

        self.container = Frame(self.root)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):

        # Upgrade menu, Button values to be changed for better game pacing.

        """ Need to add commands to buttons """

        # Upgrade frame
        self.create_upgrade_frame = Frame(self.container)
        self.create_upgrade_frame.grid(row=0, column=0, sticky="nsew")

        self.create_upgrade_frame.columnconfigure([0,1], minsize=100, weight=1)
        self.create_upgrade_frame.rowconfigure([0,1,2,3,4,5,6,7], minsize=20, weight=1)

        # Upgrade Label
        Label(self.create_upgrade_frame, text="Upgrades", font=TITLE_FONT).grid(row=0, column=0, columnspan=2, pady=5)

        # Currency Label
        self.currency_lbl = Label(self.create_upgrade_frame, text=f"Currency: 0", font=TITLE_FONT)
        self.currency_lbl.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Ad-blocker Label
        Label(self.create_upgrade_frame, text="Ad-blocker:").grid(row=2, column=0, pady=5)

        # Ad-blocker Button
        self.upgrade_btn1 = Button(self.create_upgrade_frame, text="10")
        self.upgrade_btn1.grid(row=2, column=1, padx=5, pady=2)

        # Bigger windows Label
        Label(self.create_upgrade_frame, text="Bigger Windows:").grid(row=3, column=0, pady=5)

        # Bigger windows Button
        self.upgrade_btn2 = Button(self.create_upgrade_frame, text="100")
        self.upgrade_btn2.grid(row=3, column=1, padx=5, pady=2)

        # Double click Label
        Label(self.create_upgrade_frame, text="Double click:").grid(row=4, column=0, pady=5)

        # Double click Button
        self.upgrade_btn3 = Button(self.create_upgrade_frame, text="250")
        self.upgrade_btn3.grid(row=4, column=1, padx=5, pady=2)

        # VPN Label
        Label(self.create_upgrade_frame, text="VPN:").grid(row=5, column=0, pady=5)

        # VPN Button
        self.upgrade_btn4 = Button(self.create_upgrade_frame, text="1000")
        self.upgrade_btn4.grid(row=5, column=1, padx=5, pady=2)

        # Tech support Label
        Label(self.create_upgrade_frame, text="Tech support:").grid(row=6, column=0, pady=5)

        # Tech support Button
        self.upgrade_btn5 = Button(self.create_upgrade_frame, text="2500")
        self.upgrade_btn5.grid(row=6, column=1, padx=5, pady=2)

        # Anti-virus Label
        Label(self.create_upgrade_frame, text="Anti-virus:").grid(row=7, column=0, pady=5)
        
        # Anti-virus Button
        self.upgrade_btn6 = Button(self.create_upgrade_frame, text="10000")
        self.upgrade_btn6.grid(row=7, column=1, padx=5, pady=2)

        self.popup_gui()

    
    def popup_gui(self):

        # Creates the clickable popup windows 

        self.popup = Toplevel()
        self.popup.title("Close me!")

        popup_btn = Button(self.popup, text="[X]", command=lambda:self.close_popup())
        popup_btn.pack(pady=5)

    def close_popup(self):

        # Closes the popup and adds to the player currency
        self.currency = self.currency + self.click
        self.popup.destroy()
        self.update_gui()




    def name_entry_gui(self):

        # Creates the name entry window for saving
        save_win = Toplevel(self.root)
        save_win.title("Save Game")

        save_lbl = Label(save_win, text="Enter your name and save!")
        save_lbl.pack()

        name_entry = Entry(save_win)
        name_entry.pack()

    def update_gui(self):
        self.currency_lbl.config(text=f"Currency: {self.currency}")
        
root = Tk()
run = clickerGUI(root)
root.mainloop()