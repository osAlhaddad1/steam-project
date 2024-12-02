import tkinter as tk

def open_recycling_dashboard():
    def add_to_recycling(event):
        widget = event.widget
        game = widget.cget("text")
        widget.destroy()
        recycled_games_listbox.insert(tk.END, game)

    recycling_window = tk.Toplevel(root)
    recycling_window.title("Game Recycling Dashboard")
    recycling_window.geometry("600x400")
    recycling_window.config(bg="#2e3440")

    recycling_title = tk.Label(recycling_window, text="Recycle je games!", font=("Helvetica", 18), fg="white", bg="#2e3440")
    recycling_title.pack(pady=20)

    recycled_games_listbox = tk.Listbox(recycling_window, font=("Helvetica", 12), fg="white", bg="#3b4252", selectbackground="#81a1c1")
    recycled_games_listbox.pack(fill="both", expand=True, padx=20, pady=10)

    back_button = tk.Button(recycling_window, text="Terug naar Dashboard", command=recycling_window.destroy,
                            bg="#81a1c1", fg="white", font=("Helvetica", 10), relief="flat")
    back_button.pack(pady=20)

def open_energy_usage():
    energy_window = tk.Toplevel(root)
    energy_window.title("Energieverbruik")
    energy_window.geometry("600x400")
    energy_window.config(bg="#2e3440")

    energy_title = tk.Label(energy_window, text="Huidig Energieverbruik", font=("Helvetica", 18), fg="white", bg="#2e3440")
    energy_title.pack(pady=20)

    energy_info = tk.Label(energy_window, text="Je huidige energieverbruik is: 50 kWh", font=("Helvetica", 14), fg="white", bg="#2e3440")
    energy_info.pack(pady=20)

    back_button = tk.Button(energy_window, text="Terug naar Dashboard", command=energy_window.destroy, bg="#81a1c1", fg="white", font=("Helvetica", 10), relief="flat")
    back_button.pack(pady=20)

def open_my_possessions():
    possessions_window = tk.Toplevel(root)
    possessions_window.title("Mijn Bezittingen")
    possessions_window.geometry("600x400")
    possessions_window.config(bg="#2e3440")

    possessions_title = tk.Label(possessions_window, text="Wat ik in bezit heb", font=("Helvetica", 18), fg="white", bg="#2e3440")
    possessions_title.pack(pady=20)

    my_possessions_listbox = tk.Listbox(possessions_window, font=("Helvetica", 12), fg="white", bg="#3b4252", selectbackground="#81a1c1")
    my_possessions_listbox.pack(fill="both", expand=True, padx=20, pady=10)

    # Toevoegen van voorbeeldbezigheden (games die je bezit)
    my_possessions = ["Grand Theft Auto V", "Fortnite", "Minecraft"]
    for possession in my_possessions:
        my_possessions_listbox.insert(tk.END, possession)

    back_button = tk.Button(possessions_window, text="Terug naar Dashboard", command=possessions_window.destroy, bg="#81a1c1", fg="white", font=("Helvetica", 10), relief="flat")
    back_button.pack(pady=20)

def open_shop():
    shop_window = tk.Toplevel(root)
    shop_window.title("Shop")
    shop_window.geometry("600x400")
    shop_window.config(bg="#2e3440")

    shop_title = tk.Label(shop_window, text="Shop - Koop nieuwe games!", font=("Helvetica", 18), fg="white", bg="#2e3440")
    shop_title.pack(pady=20)

    shop_listbox = tk.Listbox(shop_window, font=("Helvetica", 12), fg="white", bg="#3b4252", selectbackground="#81a1c1")
    shop_listbox.pack(fill="both", expand=True, padx=20, pady=10)

    # Toevoegen van games die beschikbaar zijn in de winkel
    available_games = ["Cyberpunk 2077", "The Witcher 3", "Valorant", "Apex Legends", "Overwatch 2"]
    for game in available_games:
        shop_listbox.insert(tk.END, game)

    back_button = tk.Button(shop_window, text="Terug naar Dashboard", command=shop_window.destroy, bg="#81a1c1", fg="white", font=("Helvetica", 10), relief="flat")
    back_button.pack(pady=20)

root = tk.Tk()
root.title("Steam Dashboard")
root.geometry("800x600")
root.config(bg="#2e3440")

navbar = tk.Frame(root, bg="#3b4252", height=50)
navbar.pack(fill="x")

dashboard_button = tk.Button(navbar, text="Dashboard", bg="#88c0d0", fg="black", font=("Helvetica", 10), relief="flat")
dashboard_button.pack(side="left", padx=10, pady=5)

recycling_button = tk.Button(navbar, text="Game Recycling", command=open_recycling_dashboard,
                             bg="#88c0d0", fg="black", font=("Helvetica", 10), relief="flat")
recycling_button.pack(side="left", padx=10, pady=5)

energy_button = tk.Button(navbar, text="Energieverbruik", command=open_energy_usage,
                          bg="#88c0d0", fg="black", font=("Helvetica", 10), relief="flat")
energy_button.pack(side="left", padx=10, pady=5)

possessions_button = tk.Button(navbar, text="Mijn Bezittingen", command=open_my_possessions,
                               bg="#88c0d0", fg="black", font=("Helvetica", 10), relief="flat")
possessions_button.pack(side="left", padx=10, pady=5)

shop_button = tk.Button(navbar, text="Shop", command=open_shop,
                        bg="#88c0d0", fg="black", font=("Helvetica", 10), relief="flat")
shop_button.pack(side="left", padx=10, pady=5)

dashboard_title = tk.Label(root, text="Welkom op je Steam Dashboard!", font=("Helvetica", 20), fg="#eceff4", bg="#2e3440")
dashboard_title.pack(pady=20)

games = ["Grand Theft Auto V", "Fortnite", "Call of Duty: Modern Warfare", "Minecraft",
         "Cyberpunk 2077", "The Witcher 3", "Valorant", "Apex Legends", "Overwatch 2", "League of Legends"]

games_frame = tk.Frame(root, bg="#2e3440")
games_frame.pack(pady=20)

for game in games:
    game_label = tk.Label(games_frame, text=game, font=("Helvetica", 14), fg="#d8dee9", bg="#2e3440", relief="flat")
    game_label.pack(anchor="w", padx=20, pady=5)

footer = tk.Label(root, text="© 2024 Steam Dashboard - Lotfi Zizaoui", font=("Helvetica", 10), fg="#4c566a", bg="#2e3440")
footer.pack(side="bottom", pady=10)

root.mainloop()
