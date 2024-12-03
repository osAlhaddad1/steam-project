import tkinter as tk
import json


# Laad data uit steam.json
def load_steam_data():
    with open("steam.json", "r") as file:
        return json.load(file)


steam_data = load_steam_data()

# Lijst voor Mijn Bezittingen
owned_games = []


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

    # Voeg alle beschikbare games toe aan de shop
    for game in steam_data:
        shop_listbox.insert(tk.END, game["name"])

    def buy_game():
        selected_index = shop_listbox.curselection()
        if selected_index:
            game = steam_data.pop(selected_index[0])  # Haal game uit shop-data
            owned_games.append(game)  # Voeg game toe aan bezittingen
            shop_listbox.delete(selected_index)  # Verwijder uit listbox

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

    # Voeg alle bezittingen toe
    for game in owned_games:
        possessions_listbox.insert(tk.END, game["name"])

    back_button = tk.Button(possessions_window, text="Terug naar Dashboard", command=possessions_window.destroy,
                            bg="#81a1c1", fg="white", font=("Helvetica", 10), relief="flat")
    back_button.pack(pady=20)


def open_energy_usage():
    energy_window = tk.Toplevel(root)
    energy_window.title("Energieverbruik")
    energy_window.geometry("600x400")
    energy_window.config(bg="#2e3440")

    energy_title = tk.Label(energy_window, text="Huidig Energieverbruik", font=("Helvetica", 18), fg="white",
                            bg="#2e3440")
    energy_title.pack(pady=20)

    energy_info = tk.Label(energy_window, text="Je huidige energieverbruik is: 50 kWh", font=("Helvetica", 14),
                           fg="white", bg="#2e3440")
    energy_info.pack(pady=20)

    back_button = tk.Button(energy_window, text="Terug naar Dashboard", command=energy_window.destroy, bg="#81a1c1",
                            fg="white", font=("Helvetica", 10), relief="flat")
    back_button.pack(pady=20)


# Hoofdvenster en menu
root = tk.Tk()
root.title("Steam Dashboard")
root.geometry("800x600")
root.config(bg="#2e3440")

navbar = tk.Frame(root, bg="#3b4252", height=50)
navbar.pack(fill="x")

shop_button = tk.Button(navbar, text="Shop", command=open_shop, bg="#88c0d0", fg="black", font=("Helvetica", 10),
                        relief="flat")
shop_button.pack(side="left", padx=10, pady=5)

possessions_button = tk.Button(navbar, text="Mijn Bezittingen", command=open_my_possessions, bg="#88c0d0", fg="black",
                               font=("Helvetica", 10), relief="flat")
possessions_button.pack(side="left", padx=10, pady=5)

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
