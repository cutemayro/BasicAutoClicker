import os
import sys
import time
import threading
import keyboard
import pyautogui
from PIL import Image
import customtkinter as ctk

pyautogui.PAUSE = 0.0

class AutoClickerApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Simple Auto Clicker")
        self.window.geometry("800x600")
        self.window.iconbitmap(self.get_asset_path("icon.ico"))
        ctk.set_appearance_mode("Light")
        
        self.is_running = False
        self.delay_entries = {}
        self.selected_click_type = ctk.StringVar(value="None")
        
        self.mouse_assets = {
            "None":   self.load_image("mouse no highlight.png"),
            "Left":   self.load_image("mouse left highlight.png"),
            "Right":  self.load_image("mouse right highlight.png"),
            "Middle": self.load_image("mouse middle highlight.png")
        }

        self.create_delay_section()
        self.create_selection_section()
        self.create_action_section()

        keyboard.add_hotkey('F6', self.toggle_clicker)

    def get_asset_path(self, filename):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, filename)

    def load_image(self, filename):
        full_path = self.get_asset_path(filename)
        return ctk.CTkImage(Image.open(full_path), size=(180, 180))

    def create_delay_section(self):
        delay_f = ctk.CTkFrame(master=self.window, width=750, height=200, corner_radius=15)
        delay_f.pack(padx=20, pady=20, fill="x")
        delay_f.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        delay_l = ctk.CTkLabel(master=delay_f, text="Configure Click Delay", font=("Arial", 16, "bold"))
        delay_l.grid(column=0, row=0, columnspan=8, pady=(15, 10))

        intervals = ["hours", "minutes", "seconds", "miliseconds"]
        for i, text in enumerate(intervals):
            entry = ctk.CTkEntry(master=delay_f, height=30, width=60, justify="center")
            entry.insert(0, "0")
            entry.grid(column=i*2, row=1, padx=(20, 5), pady=(0, 20), sticky="e")
            self.delay_entries[text] = entry

            label = ctk.CTkLabel(master=delay_f, text=text)
            label.grid(column=i*2+1, row=1, padx=(5, 20), pady=(0, 20), sticky="w")

    def create_selection_section(self):
        click_f = ctk.CTkFrame(master=self.window, width=750, height=220, corner_radius=15)
        click_f.pack(padx=20, pady=20, fill="x")

        self.image_canvas = ctk.CTkLabel(master=click_f, text="", image=self.mouse_assets["None"])
        self.image_canvas.pack(side="left", padx=35, pady=20)

        select_container = ctk.CTkFrame(master=click_f, fg_color="transparent")
        select_container.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        select_title = ctk.CTkLabel(master=select_container, text="Select Click Button", font=("Arial", 14, "bold"))
        select_title.pack(anchor="w", pady=(10, 10))

        self.button_selector = ctk.CTkSegmentedButton(
            master=select_container,
            values=["None", "Left", "Right", "Middle"],
            variable=self.selected_click_type,
            command=self.update_mouse_visual
        )
        self.button_selector.pack(fill="x", pady=10, padx=(0, 20))

    def create_action_section(self):
        clicker_button_f = ctk.CTkFrame(master=self.window, width=750, height=150, corner_radius=15)
        clicker_button_f.pack(padx=20, pady=20, fill="x")

        self.button_action = ctk.CTkButton(
            master=clicker_button_f, 
            width=600, 
            height=80, 
            corner_radius=15, 
            text="Start Auto Clicker [F6]", 
            font=("Arial", 16, "bold"),
            fg_color="#228B22",
            hover_color="#1A661A",
            command=self.toggle_clicker
        )
        self.button_action.pack(pady=20)

    def update_mouse_visual(self, value):
        self.image_canvas.configure(image=self.mouse_assets.get(value, self.mouse_assets["None"]))

    def clicker_loop(self):
        try:
            h = float(self.delay_entries["hours"].get()) * 3600
            m = float(self.delay_entries["minutes"].get()) * 60
            s = float(self.delay_entries["seconds"].get())
            ms = float(self.delay_entries["miliseconds"].get()) / 1000
            total_delay = h + m + s + ms
        except ValueError:
            total_delay = 0.1 

        click_choice = self.selected_click_type.get().lower()
        if click_choice == "none":
            click_choice = "left" 

        actual_delay = max(0.001, total_delay)

        while self.is_running:
            pyautogui.click(button=click_choice)
            
            time_slept = 0
            while time_slept < actual_delay:
                if not self.is_running: 
                    return
                time.sleep(0.001)
                time_slept += 0.001

    def toggle_clicker(self):
        if not self.is_running:
            self.is_running = True
            self.button_action.configure(text="Stop Auto Clicker [F6]", fg_color="#CC3333", hover_color="#992222")
            threading.Thread(target=self.clicker_loop, daemon=True).start() 
        else:
            self.is_running = False
            self.button_action.configure(text="Start Auto Clicker [F6]", fg_color="#228B22", hover_color="#1A661A")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = AutoClickerApp()
    app.run()