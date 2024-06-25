import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import json
from customtkinter import CTk, CTkButton, CTkLabel, CTkFrame, set_appearance_mode, set_default_color_theme

class SoftwareLauncher(CTk):
    def __init__(self):
        super().__init__()

        self.title("Software Launcher")
        self.geometry("1280x720")
        self.programs = []

        set_appearance_mode("System")  # Set appearance mode
        set_default_color_theme("blue")  # Set default color theme

        # Sidebar frame
        self.sidebar_frame = CTkFrame(self, width=140)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = CTkLabel(self.sidebar_frame, text="Software Launcher", font=("Arial", 16, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.add_button = CTkButton(self.sidebar_frame, text="Add Program", command=self.add_program)
        self.add_button.grid(row=1, column=0, padx=20, pady=10)

        self.toggle_theme_button = CTkButton(self.sidebar_frame, text="Toggle Theme", command=self.toggle_theme)
        self.toggle_theme_button.grid(row=2, column=0, padx=20, pady=10)

        # Main content area
        self.main_frame = CTkFrame(self)
        self.main_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Start auto-save
        self.start_auto_save()

        # Load saved data
        self.load_data()

    def add_program(self):
        program_path = filedialog.askopenfilename(
            title="Select a program to run", filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if program_path:
            display_name = os.path.basename(program_path)  # Use original filename as display name
            self.create_program_box(display_name, program_path)

    def create_program_box(self, display_name, program_path):
        program_box = CTkFrame(self.main_frame)
        program_box.pack(padx=10, pady=10, fill=tk.X)

        name_label = CTkLabel(program_box, text=display_name)
        name_label.pack(side='left', padx=10, pady=10)

        rename_button = CTkButton(program_box, text='Rename', command=lambda box=program_box, label=name_label: self.rename_program(box, label))
        rename_button.pack(side='right', padx=10, pady=10)

        launch_button = CTkButton(program_box, text='Launch', command=lambda: self.launch_program(program_path))
        launch_button.pack(side='right', padx=10, pady=10)

        self.programs.append((program_box, name_label, display_name, program_path))

    def rename_program(self, box, label):
        current_name = label.cget("text")
        new_name = simpledialog.askstring("Rename Program", f"Enter new name for '{current_name}':")
        if new_name:
            label.configure(text=new_name)
            for idx, program in enumerate(self.programs):
                if program[0] == box:
                    self.programs[idx] = (program[0], label, new_name, program[3])

    def launch_program(self, program_path):
        try:
            os.startfile(program_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch program: {e}")

    def toggle_theme(self):
        current_theme = set_default_color_theme()
        if current_theme == "blue":
            set_default_color_theme("dark-blue")
        else:
            set_default_color_theme("blue")

    def save_data(self):
        data = []
        for program in self.programs:
            data.append({
                'display_name': program[2],
                'program_path': program[3]
            })

        # Save data to a file (example: 'saved_data.json')
        with open('saved_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        try:
            with open('saved_data.json', 'r') as f:
                data = json.load(f)
                for item in data:
                    self.create_program_box(item['display_name'], item['program_path'])
        except FileNotFoundError:
            messagebox.showwarning("No Data Found", "No saved data found.")

    def start_auto_save(self):
        # Schedule auto-save every 1000 ms (1 second)
        self.after(1000, self.auto_save)

    def auto_save(self):
        self.save_data()
        # Reschedule auto-save
        self.after(1000, self.auto_save)

if __name__ == "__main__":
    app = SoftwareLauncher()
    app.mainloop()