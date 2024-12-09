import tkinter as tk
import json
from tkinter import messagebox

def load_steam_data():
    with open("steam.json", "r") as file:
        return json.load(file)


steam_data = load_steam_data()

owned_games = []
donated_games = []


def open_game_details(game_data):
    details_window = tk.Toplevel(root)
    details_window.title(game_data["name"])
    details_window.geometry("600x400")
    details_window.config(bg="#2e3440")

    game_title = tk.Label(details_window, text=game_data["name"], font=("Helvetica", 18), fg="white", bg="#2e3440")
    game_title.pack(pady=10)

    game_details = f"Release Date: {game_data['release_date']}\n" \
                   f"Developer: {game_data['developer']}\n" \
                   f"Publisher: {game_data['publisher']}\n" \
                   f"Platforms: {game_data['platforms']}\n" \
                   f"Genres: {game_data['genres']}\n" \
                   f"Price: ${game_data['price']}\n" \
                   f"Achievements: {game_data['achievements']}\n" \
                   f"Positive Ratings: {game_data['positive_ratings']}\n" \
                   f"Negative Ratings: {game_data['negative_ratings']}\n" \
                   f"Steam Tags: {game_data['steamspy_tags']}"

    game_info = tk.Label(details_window, text=game_details, font=("Helvetica", 12), fg="white", bg="#2e3440")
    game_info.pack(padx=20, pady=20)

    back_button = tk.Button(details_window, text="Terug naar Shop", command=details_window.destroy, bg="#81a1c1",
                            fg="white", font=("Helvetica", 10), relief="flat")
    back_button.pack(pady=20)


def open_shop():
    shop_window = tk.Toplevel(root)
    shop_window.title("Shop")
    shop_window.geometry("600x400")
    shop_window.config(bg="#2e3440")

    shop_title = tk.Label(shop_window, text="Shop - Koop nieuwe games!", font=("Helvetica", 18), fg="white",
                          bg="#2e3440")
    shop_title.pack(pady=20)

    shop_listbox = tk.Listbox(shop_window, font=("Helvetica", 12), fg="white", bg="#3b4252", selectbackground="#81a1c1")
    shop_listbox.pack(fill="both", expand=True, padx=20, pady=10)

    for game in steam_data:
        shop_listbox.insert(tk.END, game["name"])

    def buy_game():
        selected_index = shop_listbox.curselection()
        if selected_index:
            game = steam_data.pop(selected_index[0])
            owned_games.append(game)
            shop_listbox.delete(selected_index)

    def on_game_select(event):
        selected_index = shop_listbox.curselection()
        if selected_index:
            game = steam_data[selected_index[0]]
            open_game_details(game)

    shop_listbox.bind("<Double-1>", on_game_select)

    buy_button = tk.Button(shop_window, text="Koop Game", command=buy_game, bg="#81a1c1", fg="white",
                           font=("Helvetica", 10), relief="flat")
    buy_button.pack(pady=10)

    back_button = tk.Button(shop_window, text="Terug naar Dashboard", command=shop_window.destroy, bg="#81a1c1",
                            fg="white", font=("Helvetica", 10), relief="flat")
    back_button.pack(pady=20)


def open_my_possessions():
    possessions_window = tk.Toplevel(root)
    possessions_window.title("Mijn Bezittingen")
    possessions_window.geometry("600x400")
    possessions_window.config(bg="#2e3440")

    possessions_title = tk.Label(possessions_window, text="Mijn Bezittingen", font=("Helvetica", 18), fg="white",
                                 bg="#2e3440")
    possessions_title.pack(pady=20)

    possessions_listbox = tk.Listbox(possessions_window, font=("Helvetica", 12), fg="white", bg="#3b4252",
                                     selectbackground="#81a1c1")
    possessions_listbox.pack(fill="both", expand=True, padx=20, pady=10)

    for game in owned_games:
        possessions_listbox.insert(tk.END, game["name"])

    def donate_game():
        selected_index = possessions_listbox.curselection()
        if selected_index:
            game = owned_games.pop(selected_index[0])
            donated_games.append(game)
            possessions_listbox.delete(selected_index)

    donate_button = tk.Button(possessions_window, text="Doneer Game", command=donate_game, bg="#81a1c1", fg="white",
                              font=("Helvetica", 10), relief="flat")
    donate_button.pack(pady=10)

    back_button = tk.Button(possessions_window, text="Terug naar Dashboard", command=possessions_window.destroy,
                            bg="#81a1c1", fg="white", font=("Helvetica", 10), relief="flat")
    back_button.pack(pady=20)


def open_donations():
    donations_window = tk.Toplevel(root)
    donations_window.title("Donaties")
    donations_window.geometry("600x400")
    donations_window.config(bg="#2e3440")

    donations_title = tk.Label(donations_window, text="Donaties", font=("Helvetica", 18), fg="white", bg="#2e3440")
    donations_title.pack(pady=20)

    donations_listbox = tk.Listbox(donations_window, font=("Helvetica", 12), fg="white", bg="#3b4252",
                                   selectbackground="#81a1c1")
    donations_listbox.pack(fill="both", expand=True, padx=20, pady=10)

    for game in donated_games:
        donations_listbox.insert(tk.END, game["name"])

    back_button = tk.Button(donations_window, text="Terug naar Dashboard", command=donations_window.destroy,
                            bg="#81a1c1", fg="white", font=("Helvetica", 10), relief="flat")
    back_button.pack(pady=20)



def open_energy_usage():
    energy_window = tk.Toplevel(root)
    energy_window.title("Energieverbruik")
    energy_window.geometry("600x400")
    energy_window.config(bg="#2e3440")

    energy_title = tk.Label(energy_window, text="Huidig Energieverbruik", font=("Helvetica", 18), fg="white", bg="#2e3440")
    energy_title.pack(pady=20)

    global energy_info
    energy_info = tk.Label(energy_window, text="Je huidige energieverbruik is: 50 kWh", font=("Helvetica", 14),
                           fg="white", bg="#2e3440")
    energy_info.pack(pady=20)

    back_button = tk.Button(energy_window, text="Terug naar Dashboard", command=energy_window.destroy, bg="#81a1c1",
                            fg="white", font=("Helvetica", 10), relief="flat")
    back_button.pack(pady=20)

    update_energy_usage()  # Start de dynamische update van het energieverbruik


def update_energy_usage():
    energy_usage = 50 + len(owned_games) * 5  # Start met 50 kWh en voeg 5 kWh per game toe
    current_usage = float(
        energy_info.cget("text").split(":")[1].strip().split(" ")[0])  # Haal het huidige energieverbruik op
    target_usage = energy_usage  # Het nieuwe doelenergieverbruik

    if current_usage < target_usage:
        current_usage += 0.5  # Verhoog het energieverbruik met 0.5 kWh per update
    elif current_usage > target_usage:
        current_usage -= 0.5  # Verlaag het energieverbruik met 0.5 kWh per update

    # Werk de labeltekst bij met de nieuwe waarde
    energy_info.config(text=f"Je huidige energieverbruik is: {current_usage:.1f} kWh")

    root.after(500, update_energy_usage)  # Werk het elke 0,5 seconde bij


def load_users():
    with open("users.json", "r") as file:
        return json.load(file)["users"]

def validate_login(parent, username_entry, password_entry):
    users = load_users()
    userid = username_entry.get()
    password = password_entry.get()
    for user in users:
        if user["username"] == userid and user["password"] == password:
            parent.destroy()
            start_dashboard()
            return
    messagebox.showerror("Login Failed", "Invalid username or password")

def toggle_password(password_entry, show_var):
    if show_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

def forgot_password():
    messagebox.showinfo("Forgot Password", "Pech!")

def show_login():
    login_window = tk.Tk()
    login_window.title("Login Form")
    login_window.geometry("300x300")
    login_window.resizable(False, False)
    login_window.config(bg="#2e3440")
    username_label = tk.Label(login_window, text="Username:", fg="#d8dee9", bg="#2e3440")
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_window, width=25, bg="#3b4252", fg="#d8dee9", insertbackground="#d8dee9")
    username_entry.pack(pady=5)
    password_label = tk.Label(login_window, text="Password:", fg="#d8dee9", bg="#2e3440")
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", width=25, bg="#3b4252", fg="#d8dee9", insertbackground="#d8dee9")
    password_entry.pack(pady=5)
    show_var = tk.BooleanVar()
    show_password_check = tk.Checkbutton(
        login_window, text="Show Password", variable=show_var,
        command=lambda: toggle_password(password_entry, show_var), fg="#d8dee9", bg="#2e3440", selectcolor="#3b4252"
    )
    show_password_check.pack(pady=5)
    login_button = tk.Button(login_window, text="Login", command=lambda: validate_login(login_window, username_entry, password_entry), bg="#81a1c1", fg="white", width=10)
    login_button.pack(pady=10)
    forgot_button = tk.Button(login_window, text="Forgot Password?", command=forgot_password, bg="#2e3440", fg="#88c0d0", borderwidth=0)
    forgot_button.pack(pady=5)
    login_window.mainloop()

def start_dashboard():
    global root
    root = tk.Tk()
    root.title("Steam Dashboard")
    root.geometry("800x600")
    root.config(bg="#2e3440")

    navbar = tk.Frame(root, bg="#3b4252", height=50)
    navbar.pack(fill="x")

    shop_button = tk.Button(navbar, text="Shop", command=open_shop, bg="#88c0d0", fg="black", font=("Helvetica", 10),
                            relief="flat")
    shop_button.pack(side="left", padx=10, pady=5)

    possessions_button = tk.Button(navbar, text="Mijn Bezittingen", command=open_my_possessions, bg="#88c0d0",
                                   fg="black",
                                   font=("Helvetica", 10), relief="flat")
    possessions_button.pack(side="left", padx=10, pady=5)

    donations_button = tk.Button(navbar, text="Donaties", command=open_donations, bg="#88c0d0", fg="black",
                                 font=("Helvetica", 10),
                                 relief="flat")
    donations_button.pack(side="left", padx=10, pady=5)

    energy_button = tk.Button(navbar, text="Energieverbruik", command=open_energy_usage, bg="#88c0d0", fg="black",
                              font=("Helvetica", 10), relief="flat")
    energy_button.pack(side="left", padx=10, pady=5)

    dashboard_title = tk.Label(root, text="Welkom op je Steam Dashboard!", font=("Helvetica", 20), fg="#eceff4",
                               bg="#2e3440")
    dashboard_title.pack(pady=20)

    footer = tk.Label(root, text="© 2024 Steam Dashboard", font=("Helvetica", 10), fg="#4c566a",
                      bg="#2e3440")
    footer.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    show_login()
