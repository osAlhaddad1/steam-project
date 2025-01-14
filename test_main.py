import tkinter as tk
from tkinter import messagebox
import json
import os


class SteamDashboardApp:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Steam Dashboard")
        self.root.geometry("800x600")
        self.root.config(bg="#2e3440")


        self.setup_navbar()
        self.setup_dashboard()

    def setup_navbar(self):
        navbar = tk.Frame(self.root, bg="#3b4252", height=50)
        navbar.pack(fill="x")

        dashboard_button = tk.Button(navbar, text="Dashboard", bg="#88c0d0", fg="black", font=("Helvetica", 10),
                                     relief="flat")
        dashboard_button.pack(side="left", padx=10, pady=5)

        recycling_button = tk.Button(navbar, text="Game Recycling", command=self.open_recycling_dashboard,
                                     bg="#88c0d0", fg="black", font=("Helvetica", 10), relief="flat")
        recycling_button.pack(side="left", padx=10, pady=5)

        energy_button = tk.Button(navbar, text="Energieverbruik", command=self.open_energy_usage,
                                  bg="#88c0d0", fg="black", font=("Helvetica", 10), relief="flat")
        energy_button.pack(side="left", padx=10, pady=5)

        possessions_button = tk.Button(navbar, text="Mijn Bezittingen", command=self.open_my_possessions,
                                       bg="#88c0d0", fg="black", font=("Helvetica", 10), relief="flat")
        possessions_button.pack(side="left", padx=10, pady=5)

        shop_button = tk.Button(navbar, text="Shop", command=self.open_shop,
                                bg="#88c0d0", fg="black", font=("Helvetica", 10), relief="flat")
        shop_button.pack(side="left", padx=10, pady=5)

    def setup_dashboard(self):
        dashboard_title = tk.Label(self.root, text="Welkom op je Steam Dashboard!", font=("Helvetica", 20),
                                   fg="#eceff4", bg="#2e3440")
        dashboard_title.pack(pady=20)

        games = ["Grand Theft Auto V", "Fortnite", "Call of Duty: Modern Warfare", "Minecraft",
                 "Cyberpunk 2077", "The Witcher 3", "Valorant", "Apex Legends", "Overwatch 2", "League of Legends"]

        games_frame = tk.Frame(self.root, bg="#2e3440")
        games_frame.pack(pady=20)

        for game in games:
            game_label = tk.Label(games_frame, text=game, font=("Helvetica", 14), fg="#d8dee9", bg="#2e3440",
                                  relief="flat")
            game_label.pack(anchor="w", padx=20, pady=5)

        footer = tk.Label(self.root, text="© 2024 Steam Dashboard - Lotfi Zizaoui", font=("Helvetica", 10),
                          fg="#4c566a", bg="#2e3440")
        footer.pack(side="bottom", pady=10)

    def open_recycling_dashboard(self):
        recycling_window = tk.Toplevel(self.root)
        recycling_window.title("Game Recycling Dashboard")
        recycling_window.geometry("600x400")
        recycling_window.config(bg="#2e3440")

        recycling_title = tk.Label(recycling_window, text="Recycle je games!", font=("Helvetica", 18), fg="white",
                                   bg="#2e3440")
        recycling_title.pack(pady=20)

        recycled_games_listbox = tk.Listbox(recycling_window, font=("Helvetica", 12), fg="white", bg="#3b4252",
                                            selectbackground="#81a1c1")
        recycled_games_listbox.pack(fill="both", expand=True, padx=20, pady=10)

        back_button = tk.Button(recycling_window, text="Terug naar Dashboard", command=recycling_window.destroy,
                                bg="#81a1c1", fg="white", font=("Helvetica", 10), relief="flat")
        back_button.pack(pady=20)

    def open_energy_usage(self):
        energy_window = tk.Toplevel(self.root)
        energy_window.title("Energieverbruik")
        energy_window.geometry("600x400")
        energy_window.config(bg="#2e3440")

        energy_title = tk.Label(energy_window, text="Huidig Energieverbruik", font=("Helvetica", 18), fg="white",
                                bg="#2e3440")
        energy_title.pack(pady=20)

        energy_info = tk.Label(energy_window, text="Je huidige energieverbruik is: 50 kWh", font=("Helvetica", 14),
                               fg="white", bg="#2e3440")
        energy_info.pack(pady=20)

        back_button = tk.Button(energy_window, text="Terug naar Dashboard", command=energy_window.destroy,
                                bg="#81a1c1", fg="white", font=("Helvetica", 10), relief="flat")
        back_button.pack(pady=20)

    def open_my_possessions(self):
        possessions_window = tk.Toplevel(self.root)
        possessions_window.title("Mijn Bezittingen")
        possessions_window.geometry("600x400")
        possessions_window.config(bg="#2e3440")

        possessions_title = tk.Label(possessions_window, text="Wat ik in bezit heb", font=("Helvetica", 18), fg="white",
                                     bg="#2e3440")
        possessions_title.pack(pady=20)

        my_possessions_listbox = tk.Listbox(possessions_window, font=("Helvetica", 12), fg="white", bg="#3b4252",
                                            selectbackground="#81a1c1")
        my_possessions_listbox.pack(fill="both", expand=True, padx=20, pady=10)

        my_possessions = ["Grand Theft Auto V", "Fortnite", "Minecraft"]
        for possession in my_possessions:
            my_possessions_listbox.insert(tk.END, possession)

        back_button = tk.Button(possessions_window, text="Terug naar Dashboard", command=possessions_window.destroy,
                                bg="#81a1c1", fg="white", font=("Helvetica", 10), relief="flat")
        back_button.pack(pady=20)

    def open_shop(self):
        shop_window = tk.Toplevel(self.root)
        shop_window.title("Shop")
        shop_window.geometry("600x400")
        shop_window.config(bg="#2e3440")

        shop_title = tk.Label(shop_window, text="Shop - Koop nieuwe games!", font=("Helvetica", 18), fg="white",
                              bg="#2e3440")
        shop_title.pack(pady=20)

        shop_listbox = tk.Listbox(shop_window, font=("Helvetica", 12), fg="white", bg="#3b4252",
                                  selectbackground="#81a1c1")
        shop_listbox.pack(fill="both", expand=True, padx=20, pady=10)

        available_games = ["Cyberpunk 2077", "The Witcher 3", "Valorant", "Apex Legends", "Overwatch 2"]
        for game in available_games:
            shop_listbox.insert(tk.END, game)

        back_button = tk.Button(shop_window, text="Terug naar Dashboard", command=shop_window.destroy,
                                bg="#81a1c1", fg="white", font=("Helvetica", 10), relief="flat")
        back_button.pack(pady=20)




def checker():
    # Load users from the JSON file
    def load_users():
        try:
            with open("users.json", "r") as file:
                data = json.load(file)
                return data["users"]
        except FileNotFoundError:
            messagebox.showerror("Error", "User data file not found.")
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format in users.json.")
            return []

    # Function to validate the login
    def validate_login():
        userid = username_entry.get()
        password = password_entry.get()

        # Check credentials
        for user in users:
            if user["username"] == userid and user["password"] == password:
                parent.destroy()
                root = tk.Tk()
                app = SteamDashboardApp(root)
                root.mainloop()
                return
        messagebox.showerror("Login Failed", "Invalid username or password")

    # Function to toggle password visibility
    def toggle_password():
        if show_password_var.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    # Function for forgot password (Placeholder functionality)
    def forgot_password():
        messagebox.showinfo("Forgot Password", "Password recovery is not implemented yet.")

    # Load user credentials
    users = load_users()

    # Create the main window
    parent = tk.Tk()
    parent.title("Login Form")
    parent.geometry("300x250")
    parent.resizable(False, False)
    parent.config(bg="#2e3440")  # Match background color with SteamDashboardApp

    # Title label
    title_label = tk.Label(parent, text="Welcome", font=("Arial", 16, "bold"), fg="#eceff4", bg="#2e3440")
    title_label.pack(pady=10)

    # Username label and entry
    username_label = tk.Label(parent, text="Username:", fg="#d8dee9", bg="#2e3440")
    username_label.pack(pady=5)
    username_entry = tk.Entry(parent, width=25, bg="#3b4252", fg="#d8dee9", insertbackground="#d8dee9")
    username_entry.pack(pady=5)

    # Password label and entry
    password_label = tk.Label(parent, text="Password:", fg="#d8dee9", bg="#2e3440")
    password_label.pack(pady=5)
    password_entry = tk.Entry(parent, show="*", width=25, bg="#3b4252", fg="#d8dee9", insertbackground="#d8dee9")
    password_entry.pack(pady=5)

    # Show password checkbox
    show_password_var = tk.BooleanVar()
    show_password_checkbox = tk.Checkbutton(
        parent, text="Show Password", variable=show_password_var, command=toggle_password,
        fg="#eceff4", bg="#2e3440", selectcolor="#3b4252"
    )
    show_password_checkbox.pack(pady=5)

    # Login button
    login_button = tk.Button(parent, text="Login", command=validate_login, bg="#81a1c1", fg="white", width=10)
    login_button.pack(pady=10)

    # Forgot password button
    forgot_password_button = tk.Button(
        parent, text="Forgot Password?", command=forgot_password, fg="#88c0d0", bg="#2e3440", borderwidth=0
    )
    forgot_password_button.pack(pady=5)

    # Start the Tkinter event loop
    parent.mainloop()





if __name__ == "__main__":
    checker()
