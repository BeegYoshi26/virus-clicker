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
        self.currency = 10000000
        self.click = 1
        self.cps = 0
        self.spawn_rate = 2600
        self.active_popups = {}
        self.player_purchases = 0
        self.crit_chance = 0.05
        self.crit_multiplier = 10
        self.game_won = False

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

       # Multiplier / VPN Label
        Label(self.create_upgrade_frame, text="VPN:").grid(row=5, column=0, pady=5)

        # Multiplier Button
        self.upgrade_btn4 = Button(self.create_upgrade_frame, text=self.upgrade_4_value, command=lambda:self.purchace_multiplier())
        self.upgrade_btn4.grid(row=5, column=1, padx=5, pady=2)

        # Tech support Label (Upgrade 5 - Critical Strike from Option 2)
        Label(self.create_upgrade_frame, text="Tech Support (Crit):").grid(row=6, column=0, pady=5)

        # Tech support Button
        self.upgrade_btn5 = Button(self.create_upgrade_frame, text=self.upgrade_5_value, command=lambda:self.purchace_tech_support())
        self.upgrade_btn5.grid(row=6, column=1, padx=5, pady=2)

        # Anti-virus Label
        Label(self.create_upgrade_frame, text="Anti-virus:").grid(row=7, column=0, pady=5)
        
        # Anti-virus Button
        self.upgrade_btn6 = Button(self.create_upgrade_frame, text=self.upgrade_6_value, command=lambda:self.purchace_anti_virus())
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


            earned_currency = self.click
            if random.random() < self.crit_chance:
                earned_currency *= self.crit_multiplier

            
            self.currency = self.currency + earned_currency
            self.update_gui()

    def unregister_popup(self, popup_id):
        # Triggers when popup is destroyed
        if popup_id in self.active_popups:
            # Removes popup from active popups
            del self.active_popups[popup_id]

    def spawn_loop(self):
        if not self.game_won:
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
            self.upgrade_btn1.config(text=self.upgrade_1_value)

            # Updates the player currency gui
            self.update_gui()

    def purchace_faster_popups(self):
        # Check if player has enough currency to purchase
        if self.currency >= self.upgrade_2_value:

            # Takes the upgrade value from the players currency
            self.currency = self.currency - self.upgrade_2_value

            # Decreases the popup spawn rate
            self.spawn_rate = self.spawn_rate - 300

            # Increases the value of the upgrade
            self.upgrade_2_value = int(self.upgrade_2_value * 1.5)
            self.upgrade_btn2.config(text=self.upgrade_2_value)

            # Updates the gui
            self.update_gui()

    def purchace_auto_clicker(self):
        # Check if player has enough currency to purchase
        if self.currency >= self.upgrade_3_value:

            # Takes the upgrade value from the players currency
            self.currency = self.currency - self.upgrade_3_value

            # Increases the players clicks per second
            self.cps = self.cps + 1

            # Increases the value of the upgrade
            self.upgrade_3_value = int(self.upgrade_3_value * 1.5)
            self.upgrade_btn3.config(text=self.upgrade_3_value)

            # Updates the gui
            self.update_gui()

    def autoclick(self):
        # Adds cps to player currency when above 0
        if self.cps > 0:
            self.currency += self.cps

        # Updates gui
        self.update_gui()
        # Waits one second then calls then loops the function
        self.root.after(1000, self.autoclick)

    def purchace_multiplier(self):
        if self.currency >= self.upgrade_4_value:
            self.currency = self.currency - self.upgrade_4_value
            
            self.click = int(self.click * 2)
            self.spawn_rate = int(self.spawn_rate * 0.9)
            self.cps = max(1, self.cps * 2)

            self.upgrade_4_value = int(self.upgrade_4_value * 1.5)
            self.upgrade_btn4.config(text=self.upgrade_4_value)
            self.update_gui()

    def purchace_tech_support(self):
        if self.currency >= self.upgrade_5_value:
            self.currency = self.currency - self.upgrade_5_value
            
            self.crit_chance = min(0.50, self.crit_chance + 0.03)
            
            self.upgrade_5_value = int(self.upgrade_5_value * 1.6)
            self.upgrade_btn5.config(text=self.upgrade_5_value)
            self.update_gui()

    def purchace_anti_virus(self):
        if not self.game_won and self.currency >= self.upgrade_6_value:
            self.currency = self.currency - self.upgrade_6_value
            
            self.game_won = True
            self.update_gui()

            
            # Close all currently open popup windows
            for popup in list(self.active_popups.values()):
                try:
                    popup.destroy()
                except:
                    pass
            self.active_popups.clear()



            # Create a victory screen window
            win_win = Toplevel(self.root)
            win_win.title("Victory!")
            win_win.geometry("300x150")
            win_win.attributes('-topmost', True)

            Label(win_win, text="SYSTEM CLEANED!", font=("Arial", 16, "bold"), fg="green").pack(pady=20)
            Label(win_win, text="You successfully installed the Anti-Virus\nand eradicated all viruses!", font=("Arial", 10)).pack(pady=5)
            Button(win_win, text="Close Game", command=self.root.destroy).pack(pady=10)
        
root = Tk()
run = clickerGUI(root)
root.mainloop()