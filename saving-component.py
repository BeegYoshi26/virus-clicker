from tkinter import *
import random
import json
import os

TITLE_FONT = ("Arial", 14, "bold")
MAX_POPUPS = 10
SAVE_FILE = "saves.json"

class StartMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Virus Clicker - Select Save")
        self.root.geometry("320x260")
        self.root.attributes('-topmost', True)

        Label(self.root, text="Virus Clicker", font=("Arial", 16, "bold")).pack(pady=15)

        Button(self.root, text="New Game", width=20, command=self.open_new_game).pack(pady=5)
        Button(self.root, text="Load Game", width=20, command=self.open_load_game).pack(pady=5)
        Button(self.root, text="Quit", width=20, command=self.root.destroy).pack(pady=5)

    def open_new_game(self):
        # Opens a window prompting the user to enter a name.
        name_win = Toplevel(self.root)
        name_win.title("New Game")
        name_win.geometry("300x200")
        name_win.attributes('-topmost', True)

        Label(name_win, text="Enter your name:", font=TITLE_FONT).pack(pady=5)
        Label(name_win, text="(Letters only, under 12 characters)", font=("Arial", 8), fg="gray").pack(pady=2)
        
        name_entry = Entry(name_win)
        name_entry.pack(pady=5)
        name_entry.focus()

        error_lbl = Label(name_win, text="", font=("Arial", 9), fg="red")
        error_lbl.pack(pady=2)

        def confirm_name():
            # Validates the input and creates a default save dictionary
            name = name_entry.get().strip()
            
            if not name:
                error_lbl.config(text="Name cannot be empty!")
                return
            if len(name) >= 12:
                error_lbl.config(text="Name must be under 12 characters!")
                return
            if not name.isalpha():
                error_lbl.config(text="Name can only contain letters!")
                return
            
            data = {
                "name": name,
                "currency": 0,
                "click": 1,
                "cps": 0,
                "spawn_rate": 2600,
                "player_purchases": 0,
                "crit_chance": 0.01,
                "crit_multiplier": 10,
                "upgrade_1_value": 10,
                "upgrade_2_value": 100,
                "upgrade_3_value": 250,
                "upgrade_4_value": 500,
                "upgrade_5_value": 1000,
                "upgrade_6_value": 1000000
            }
            
            self.save_to_file(data)
            name_win.destroy()
            self.root.destroy()
            
            main_root = Tk()
            clickerGUI(main_root, data)

        Button(name_win, text="Start", command=confirm_name).pack(pady=10)

    def open_load_game(self):
        # Checks for existing save files
        if not os.path.exists(SAVE_FILE):
            load_win = Toplevel(self.root)
            load_win.title("Error")
            load_win.geometry("200x100")
            load_win.attributes('-topmost', True)
            Label(load_win, text="No save files found!").pack(padx=20, pady=20)
            return

        try:
            with open(SAVE_FILE, "r") as f:
                saves = json.load(f)
        except:
            saves = {}

        if not saves:
            load_win = Toplevel(self.root)
            load_win.title("Error")
            load_win.geometry("200x100")
            load_win.attributes('-topmost', True)
            Label(load_win, text="No save files found!").pack(padx=20, pady=20)
            return

        # Opens a load game window
        load_win = Toplevel(self.root)
        load_win.title("Load Game")
        load_win.geometry("280x320")
        load_win.attributes('-topmost', True)

        Label(load_win, text="Select a Save:", font=TITLE_FONT).pack(pady=10)

        listbox_frame = Frame(load_win)
        listbox_frame.pack(fill=BOTH, expand=True, padx=10)

        # Listbox for all saves
        save_listbox = Listbox(listbox_frame)
        for name in saves.keys():
            save_listbox.insert(END, name)
        save_listbox.pack(side=LEFT, fill=BOTH, expand=True)

        def refresh_listbox():
            save_listbox.delete(0, END)
            for name in saves.keys():
                save_listbox.insert(END, name)

        def confirm_load():
            # Checks if a name has been selected
            selected = save_listbox.curselection()
            if not selected:
                return
        
            # Gets the selected name
            name = save_listbox.get(selected[0])
            # Loads data from the json file
            data = saves[name]
            
            # Destroys the windows
            load_win.destroy()
            self.root.destroy()
            
            main_root = Tk()
            clickerGUI(main_root, data)

        def delete_save():
            # Checks if a name has been selected
            selected = save_listbox.curselection()
            if not selected:
                return
            name = save_listbox.get(selected[0])
            
            # Remove from dictionary and update file
            if name in saves:
                del saves[name]
                with open(SAVE_FILE, "w") as f:
                    json.dump(saves, f, indent=4)
                
                refresh_listbox()

                # Close load window if no saves are left
                if not saves:
                    load_win.destroy()

        btn_frame = Frame(load_win)
        btn_frame.pack(pady=10)

        Button(btn_frame, text="Load Profile", width=10, command=confirm_load).pack(side=LEFT, padx=5)
        Button(btn_frame, text="Delete Save", width=10, bg="lightcoral", command=delete_save).pack(side=LEFT, padx=5)

    def save_to_file(self, data):
        saves = {}
        # Checks if save file already exists (if not then creates a new file)
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    saves = json.load(f)
            except:
                saves = {}
        
        # Saves player data to save file name
        saves[data["name"]] = data
        with open(SAVE_FILE, "w") as f:
            json.dump(saves, f, indent=4)


class clickerGUI:
    def __init__(self, root, player_data):
        self.root = root
        self.player_name = player_data["name"]
        root.title(f"Virus Clicker - {self.player_name}")
        root.attributes('-topmost', True)

        # Player variables
        self.currency = player_data["currency"]
        self.click = player_data["click"]
        self.cps = player_data["cps"]
        self.spawn_rate = player_data["spawn_rate"]
        self.active_popups = {}
        self.player_purchases = player_data["player_purchases"]
        self.crit_chance = player_data["crit_chance"]
        self.crit_multiplier = player_data["crit_multiplier"]
        self.game_won = False

        # Upgrade values
        self.upgrade_1_value = player_data["upgrade_1_value"]
        self.upgrade_2_value = player_data["upgrade_2_value"]
        self.upgrade_3_value = player_data["upgrade_3_value"]
        self.upgrade_4_value = player_data["upgrade_4_value"]
        self.upgrade_5_value = player_data["upgrade_5_value"]
        self.upgrade_6_value = player_data["upgrade_6_value"]

        self.create_widgets()
        self.spawn_loop()
        self.autoclick()

    def create_widgets(self):

        # Upgrade menu, Button values to be changed for better game pacing.

        # Upgrade frame
        self.create_upgrade_frame = Frame()
        self.create_upgrade_frame.grid(row=0, column=0, sticky="nsew")

        self.create_upgrade_frame.columnconfigure([0,1], minsize=100, weight=1)
        self.create_upgrade_frame.rowconfigure([0,1,2,3,4,5,6,7,8], minsize=20, weight=1)

        # Upgrade Label
        Label(self.create_upgrade_frame, text=f"Upgrades ({self.player_name})", font=TITLE_FONT).grid(row=0, column=0, columnspan=2, pady=5)

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
        Label(self.create_upgrade_frame, text="VPN (Multiplier):").grid(row=5, column=0, pady=5)

        # Multiplier Button
        self.upgrade_btn4 = Button(self.create_upgrade_frame, text=self.upgrade_4_value, command=lambda:self.purchace_multiplier())
        self.upgrade_btn4.grid(row=5, column=1, padx=5, pady=2)

        # Tech support Label (Upgrade 5 - Critical Strike from Option 2)
        Label(self.create_upgrade_frame, text="Tech Support (Crit):").grid(row=6, column=0, pady=5)

        # Tech support Button
        self.upgrade_btn5 = Button(self.create_upgrade_frame, text=self.upgrade_5_value, command=lambda:self.purchace_tech_support())
        self.upgrade_btn5.grid(row=6, column=1, padx=5, pady=2)

        # Anti-virus Label
        Label(self.create_upgrade_frame, text="Anti-virus (Win):").grid(row=7, column=0, pady=5)
        
        # Anti-virus Button
        self.upgrade_btn6 = Button(self.create_upgrade_frame, text=self.upgrade_6_value, command=lambda:self.purchace_anti_virus())
        self.upgrade_btn6.grid(row=7, column=1, padx=5, pady=2)

        # Save Button
        self.save_btn = Button(self.create_upgrade_frame, text="Save Game", bg="lightblue", command=self.save_game)
        self.save_btn.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")

    def save_game(self):

        # Gets the current player data
        data = {
            "name": self.player_name,
            "currency": self.currency,
            "click": self.click,
            "cps": self.cps,
            "spawn_rate": self.spawn_rate,
            "player_purchases": self.player_purchases,
            "crit_chance": self.crit_chance,
            "crit_multiplier": self.crit_multiplier,
            "upgrade_1_value": self.upgrade_1_value,
            "upgrade_2_value": self.upgrade_2_value,
            "upgrade_3_value": self.upgrade_3_value,
            "upgrade_4_value": self.upgrade_4_value,
            "upgrade_5_value": self.upgrade_5_value,
            "upgrade_6_value": self.upgrade_6_value
        }

        # Creates a new "saves" file (if not already created)
        saves = {}
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    saves = json.load(f)
            except:
                saves = {}

        # Writes the player variables to saves.json under player name
        saves[self.player_name] = data
        with open(SAVE_FILE, "w") as f:
            json.dump(saves, f, indent=4)

        # Confirms the save with the player
        notif = Toplevel(self.root)
        notif.title("Saved")
        notif.geometry("200x100")
        notif.attributes('-topmost', True)
        Label(notif, text="Game Saved Successfully!", font=("Arial", 10)).pack(pady=20)
        Button(notif, text="OK", command=notif.destroy).pack()

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
            # rolls random number to see if its a crit
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
        # Check if player has enough currency to purchase
        if self.currency >= self.upgrade_4_value:

            # Takes the upgrade value from the players currency
            self.currency = self.currency - self.upgrade_4_value

            # Multiplies all the players current upgrades
            self.click = int(self.click * 2)
            self.spawn_rate = int(self.spawn_rate * 0.9)
            self.cps = max(1, self.cps * 2)
            self.crit_chance = self.crit_chance * 1.25

            # Increases the value of the upgrade
            self.upgrade_4_value = int(self.upgrade_4_value * 1.5)
            self.upgrade_btn4.config(text=self.upgrade_4_value)

            # Updates the gui
            self.update_gui()

    def purchace_tech_support(self):
        # Check if player has enough currency to purchase
        if self.currency >= self.upgrade_5_value:

            # Takes the upgrade value from the players currency
            self.currency = self.currency - self.upgrade_5_value

            # Increases the players crit chance stat
            self.crit_chance = min(0.50, self.crit_chance + 0.05)

            # Increases the value of the upgrade
            self.upgrade_5_value = int(self.upgrade_5_value * 1.5)
            self.upgrade_btn5.config(text=self.upgrade_5_value)

            # Updates the gui
            self.update_gui()

    def purchace_anti_virus(self):
        # Checks if player can buy upgrade and has not already won the game
        if not self.game_won and self.currency >= self.upgrade_6_value:
            # Takes the upgrade value from the players currency
            self.currency = self.currency - self.upgrade_6_value
            # Set players win state
            self.game_won = True
            # Updates GUI
            self.update_gui()

            # Destroys all active popups
            for popup in list(self.active_popups.values()):
                try:
                    popup.destroy()
                except:
                    pass
            self.active_popups.clear()

            # Create Win window
            win_win = Toplevel(self.root)
            win_win.title("Victory!")
            win_win.geometry("300x150")
            win_win.attributes('-topmost', True)

            Label(win_win, text="SYSTEM CLEANED!", font=("Arial", 16, "bold"), fg="green").pack(pady=20)
            Label(win_win, text="You successfully installed the Anti-Virus\nand eradicated all viruses!", font=("Arial", 10)).pack(pady=5)
            Button(win_win, text="Close Game", command=self.root.destroy).pack(pady=10)

if __name__ == "__main__":
    root = Tk()
    StartMenu(root)
    root.mainloop()