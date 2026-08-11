from tkinter import *
import random
import time

TITLE_FONT = ("Arial", 14, "bold")
MAX_POPUPS = 10

class clickerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Virus Clicker")
        root.attributes('-topmost', True)

        # Player variables
        self.currency = 100000
        self.click = 1
        self.cps = 0
        self.spawn_rate = 2600
        self.active_popups = {}

        # Upgrade values
        self.upgrade_1_value = 10
        self.upgrade_2_value = 100
        self.upgrade_3_value = 1000
        self.upgrade_4_value = 10000
        self.upgrade_5_value = 100000
        self.upgrade_6_value = 1000000

        self.create_widgets()
        self.spawn_loop()
        self.autoclick()

    def create_widgets(self):

        # Upgrade menu, Button values to be changed for better game pacing.

        """ Need to add commands to buttons """

        # Upgrade frame
        self.create_upgrade_frame = Frame()
        self.create_upgrade_frame.grid(row=0, column=0, sticky="nsew")

        self.create_upgrade_frame.columnconfigure([0,1], minsize=100, weight=1)
        self.create_upgrade_frame.rowconfigure([0,1,2,3,4,5,6,7], minsize=20, weight=1)

        # Upgrade Label
        Label(self.create_upgrade_frame, text="Upgrades", font=TITLE_FONT).grid(row=0, column=0, columnspan=2, pady=5)

        # Currency Label
        self.currency_lbl = Label(self.create_upgrade_frame, text=f"Currency: {self.currency}", font=TITLE_FONT)
        self.currency_lbl.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Extra click Label
        Label(self.create_upgrade_frame, text="Extra click:").grid(row=2, column=0, pady=5)

        # Extra click Button
        self.upgrade_btn1 = Button(self.create_upgrade_frame, text=self.upgrade_1_value, command=lambda:self.purchace_extra_click())
        self.upgrade_btn1.grid(row=2, column=1, padx=5, pady=2)

        # Faster Popups Label
        Label(self.create_upgrade_frame, text="Faster Popups:").grid(row=3, column=0, pady=5)

        # Faster Popups Button
        self.upgrade_btn2 = Button(self.create_upgrade_frame, text=self.upgrade_2_value, command=lambda:self.purchace_faster_popups())
        self.upgrade_btn2.grid(row=3, column=1, padx=5, pady=2)

        # Auto-clicker Label
        Label(self.create_upgrade_frame, text="Auto-clicker:").grid(row=4, column=0, pady=5)

        # Auto-clicker click Button
        self.upgrade_btn3 = Button(self.create_upgrade_frame, text=self.upgrade_3_value, command=lambda:self.purchace_auto_clicker())
        self.upgrade_btn3.grid(row=4, column=1, padx=5, pady=2)

        #  Label
        Label(self.create_upgrade_frame, text="VPN:").grid(row=5, column=0, pady=5)

        #  Button
        self.upgrade_btn4 = Button(self.create_upgrade_frame, text=self.upgrade_4_value)
        self.upgrade_btn4.grid(row=5, column=1, padx=5, pady=2)

        # Tech support Label
        Label(self.create_upgrade_frame, text="Tech support:").grid(row=6, column=0, pady=5)

        # Tech support Button
        self.upgrade_btn5 = Button(self.create_upgrade_frame, text=self.upgrade_5_value)
        self.upgrade_btn5.grid(row=6, column=1, padx=5, pady=2)

        # Anti-virus Label
        Label(self.create_upgrade_frame, text="Anti-virus:").grid(row=7, column=0, pady=5)
        
        # Anti-virus Button
        self.upgrade_btn6 = Button(self.create_upgrade_frame, text=self.upgrade_6_value)
        self.upgrade_btn6.grid(row=7, column=1, padx=5, pady=2)

    
    def popup_gui(self):
        # Checks the amount of active popups is under the max
        if len(self.active_popups) >= MAX_POPUPS:
            return

        # Creates the clickable popup windows 
        popup = Toplevel()
        popup_id = id(popup)
        popup.title("Close me!")
        
        # Set window screen and height
        width = 250
        height = 100

        # Get screen width and height
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        # Generate random x and y coordinates within the screen bounds
        x = random.randint(0, screen_width - width)
        y = random.randint(0, screen_height - height)

        # Set geometry with size and random position (WxH+X+Y)
        popup.geometry(f"{width}x{height}+{x}+{y}")

        popup_btn = Button(popup, text="[X]", command=lambda:self.close_popup(popup_id))
        popup_btn.grid(row=0, column=0, sticky="NSEW")

        # When popup is destroyed
        popup.bind("<Destroy>", lambda e: self.unregister_popup(popup_id))

        self.active_popups[popup_id] = popup

    def close_popup(self, popup_id):
        # Closes the popup and adds to the player currency
        if popup_id in self.active_popups:
            popup = self.active_popups[popup_id]
            popup.destroy()
            self.currency = self.currency + self.click
            self.update_gui()

    def unregister_popup(self, popup_id):
        # Triggers when popup is destroyed
        if popup_id in self.active_popups:
            # Removes popup from active popups
            del self.active_popups[popup_id]

    def spawn_loop(self):
        # Spawns the popup window
        self.popup_gui()
        # Waits specified spawn rate
        spawn_time = self.spawn_rate
        # Restarts the loop
        self.root.after(spawn_time, self.spawn_loop)

    def name_entry_gui(self):
        # Creates the name entry window for saving
        save_win = Toplevel(self.root)
        save_win.title("Save Game")

        save_lbl = Label(save_win, text="Enter your name and save!")
        save_lbl.pack()

        name_entry = Entry(save_win)
        name_entry.pack()

    def update_gui(self):
        # Updates the currency label to players current currency
        self.currency_lbl.config(text=f"Currency: {self.currency}")

    def purchace_extra_click(self):
        # Check if player has enough currency to purchase
        if self.currency >= self.upgrade_1_value:
            # Takes the upgrade value from the players currency
            self.currency = self.currency - self.upgrade_1_value
            # Upgrades the players click
            self.click = self.click + 1
            # Increases the upgrade value 
            self.upgrade_1_value = int(self.upgrade_1_value * 1.5)
            # Updates the upgrade button
            self.upgrade_btn1.config(text=self.upgrade_1_value)
            # Updates the player currency gui
            self.update_gui()

    def purchace_faster_popups(self):
        if self.currency >= self.upgrade_2_value:
            self.currency = self.currency - self.upgrade_2_value
            self.spawn_rate = self.spawn_rate - 300
            self.upgrade_2_value = int(self.upgrade_2_value * 1.5)
            self.upgrade_btn2.config(text=self.upgrade_2_value)
            self.update_gui()

    def purchace_auto_clicker(self):
        if self.currency >= self.upgrade_3_value:
            self.currency = self.currency - self.upgrade_3_value
            self.cps = self.cps + 1
            self.upgrade_3_value = int(self.upgrade_3_value * 1.5)
            self.upgrade_btn3.config(text=self.upgrade_3_value)
            self.update_gui()
            


    def autoclick(self):
        if self.cps > 0:
            self.currency += self.cps
        self.update_gui()
        self.root.after(1000, self.autoclick)

            
        
root = Tk()
run = clickerGUI(root)
root.mainloop()