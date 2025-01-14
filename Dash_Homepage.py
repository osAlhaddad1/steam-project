import tkinter as tk
import json
from tkinter import messagebox
import psycopg2
import random
import requests
from bs4 import BeautifulSoup
import psutil
import subprocess
from Nano_app_store import RaadHetNummer, Glagje, Dagboek, WackTheMole


def load_steam_data():
    with open("steam.json", "r") as file:
        return json.load(file)



steam_data = load_steam_data()
games_gekocht = [
    {"name": "Hacker Destroyer 3000", "appid": "Hacker Destroyer 3000"},
    {"name": "Raad het Nummer", "appid": "raad_het_nummer"},
    {"name": "Glagje", "appid": "glagje"},
    {"name": "Dagboek", "appid": "dagboek"},
    {"name": "Wack The Mole", "appid": "wack_the_mole"}
]
# path for the game:
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
file_path = r"D:\CODE HU\projects\steam\Hacker destroyer 3000\game.exe"

# Steam API Key
API_KEY = '329984DFEA6B379EE4B58F3243B8A38E'

# URL to get the list of all apps (games) on Steam
APP_LIST_URL = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'

# URL to get detailed information about a specific app (game)
APP_DETAILS_URL = 'https://store.steampowered.com/api/appdetails'





def top_games():
    # URL of the website to scrape
    url = "https://steamcharts.com/"

    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing the top games
        table = soup.find('table', {'id': 'top-games'})

        # Initialize a list to store the top 3 games
        top_games = []

        # Loop through the first 3 rows of the table
        for row in table.find_all('tr')[1:4]:  # Skip the header row and take the next 3 rows
            # Extract the game name from the row
            game_name = row.find('td', {'class': 'game-name'}).text.strip()
            top_games.append(game_name)


    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")




def get_all_apps():
    response = requests.get(APP_LIST_URL)
    if response.status_code == 200:
        return response.json()['applist']['apps']
    else:
        print(f"Failed to fetch app list. Status code: {response.status_code}")

        return []


gamestest = get_all_apps()



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




# Filter games met average_playtime van 0 en randomiseer ze
def get_promotional_games(steam_data):
    # Filter games die een gemiddelde speeltijd van 0 hebben
    filtered_games = [game for game in steam_data if game.get("average_playtime", 0) == 0]

    # Randomiseer de lijst van games
    random.shuffle(filtered_games)

    # Geef de eerste 5 games
    return filtered_games[:5]



def get_app_details(appid):
    params = {
        'appids': appid,
        'key': API_KEY
    }
    response = requests.get(APP_DETAILS_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data and str(appid) in data and data[str(appid)]['success']:
            return data[str(appid)]['data']
    return None

# Toon de details van een geselecteerde game

def open_game_details(game):
    appid_value = game['appid']
    name_value = game['name']

    details = get_app_details(appid_value)

    if details:
        details_window = tk.Toplevel(root)
        details_window.title(name_value)
        details_window.geometry("600x400")
        details_window.config(bg="#2e3440")

        game_title = tk.Label(details_window, text=name_value, font=("Helvetica", 18), fg="white", bg="#2e3440")
        game_title.pack(pady=10)

        game_info = {
            "appid": appid_value,
            "name": details.get('name', ''),
            "release_date": details.get('release_date', {}).get('date', ''),
            "english": int(details.get('supported_languages', '').lower().find('english') >= 0),
            "developer": ', '.join([dev.strip() for dev in details.get('developers', [])]),
            "publisher": ', '.join([pub.strip() for pub in details.get('publishers', [])]),
            "platforms": ', '.join([platform for platform, supported in details.get('platforms', {}).items() if supported]),
            "required_age": details.get('required_age', 0),
            "categories": ';'.join([cat['description'] for cat in details.get('categories', [])]),
            "genres": ';'.join([genre['description'] for genre in details.get('genres', [])]),
            "steamspy_tags": ';'.join(details.get('steamspy_tags', [])),
            "achievements": details.get('achievements', {}).get('total', 0),
            "average_playtime": details.get('playtime', {}).get('average_forever', 0),
            "median_playtime": details.get('playtime', {}).get('median_forever', 0),
            "owners": '0 - 20000',  # Not directly available in the API
            "price": details.get('price_overview', {}).get('final', 0) / 100 if details.get('price_overview') else 0
        }

        game_details = (
            f"Developer: {game_info['developer']}\n"
            f"Publisher: {game_info['publisher']}\n"
            f"Platforms: {game_info['platforms']}\n"
            f"Genres: {game_info['genres']}\n"
            f"Price: ${game_info['price']:.2f}\n"
            f"Achievements: {game_info['achievements']}\n"
            f"Steam Tags: {game_info['steamspy_tags'] or 'No tags available'}"
        )

        game_info_label = tk.Label(details_window, text=game_details, font=("Helvetica", 12), fg="white", bg="#2e3440")
        game_info_label.pack(padx=20, pady=20)

        back_button = tk.Button(details_window, text="Terug naar Dashboard", command=details_window.destroy, bg="#81a1c1",
                                fg="white", font=("Helvetica", 10), relief="flat")
        back_button.pack(pady=20)
    else:
        messagebox.showerror("Error", "Failed to fetch game details.")

# Maak een functie om de promotionele games te tonen op het dashboard
def show_promotional_games():
    steam_data = load_steam_data()  # Load data from steam.json
    promotional_games = get_promotional_games(steam_data)  # Get promotional games

    # Create a container frame to hold all groups
    container_frame = tk.Frame(root, bg="#2e3440")
    container_frame.pack(expand=True, pady=20)  # Center the container frame

    # Create a frame for promotional games
    promo_frame = tk.Frame(container_frame, bg="#2e3440")
    promo_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    promo_title = tk.Label(promo_frame, text="Promotionele Games", font=("Helvetica", 16), fg="white", bg="#2e3440")
    promo_title.pack(pady=10)

    # Add promotional games to the frame and make them clickable
    for game in promotional_games:
        promo_game_label = tk.Label(promo_frame, text=f"{game['name']} - ${game['price']}", font=("Helvetica", 12),
                                    fg="white", bg="#2e3440")
        promo_game_label.pack(pady=5)

        promo_game_label.bind("<Button-1>", lambda event, game=game: open_game_details(game))  # Make the label clickable

    # Create a frame for top games
    top_games_frame = tk.Frame(container_frame, bg="#2e3440")
    top_games_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Create a frame for trending games
    trending_games_frame = tk.Frame(container_frame, bg="#2e3440")
    trending_games_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    # Fetch and display top games and trending games
    display_top_and_trending_games(top_games_frame, trending_games_frame)

def display_top_and_trending_games(top_games_frame, trending_games_frame):
    # URL of the website to scrape
    url = "https://steamcharts.com/"

    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing the top games by player count
        top_games_table = soup.find('table', {'id': 'top-games'})

        # Initialize a list to store the top 3 games by player count
        top_games = []

        # Loop through the first 3 rows of the table
        for row in top_games_table.find_all('tr')[1:4]:  # Skip the header row and take the next 3 rows
            # Extract the game name from the row
            game_name = row.find('td', {'class': 'game-name'}).text.strip()
            # Extract the current player count from the row
            current_players = row.find('td', {'class': 'num'}).text.strip()
            top_games.append((game_name, current_players))

        # Display the top 3 games by player count
        top_games_label = tk.Label(top_games_frame, text="Top 3 Games by Player Count", font=("Helvetica", 14), fg="white", bg="#2e3440")
        top_games_label.pack(pady=10)

        for i, (game, players) in enumerate(top_games, start=1):
            game_label = tk.Label(top_games_frame, text=f"{i}. {game} - Players: {players}", font=("Helvetica", 12), fg="white", bg="#2e3440")
            game_label.pack(pady=5)

        # Find the table containing the trending games
        trending_games_table = soup.find('table', {'id': 'trending-recent'})

        # Initialize a list to store the top 3 trending games
        trending_games = []

        if trending_games_table:  # Check if the table was found
            # Loop through the first 3 rows of the trending games table
            for row in trending_games_table.find_all('tr')[1:4]:  # Skip the header row and take the next 3 rows
                # Extract the game name from the row
                game_name = row.find('td', {'class': 'game-name'}).text.strip()
                # Extract the current player count from the row
                current_players = row.find('td', {'class': 'num'}).text.strip()
                trending_games.append((game_name, current_players))

            # Display the top 3 trending games
            trending_games_label = tk.Label(trending_games_frame, text="Top 3 Trending Games", font=("Helvetica", 14), fg="white", bg="#2e3440")
            trending_games_label.pack(pady=10)

            for i, (game, players) in enumerate(trending_games, start=1):
                game_label = tk.Label(trending_games_frame, text=f"{i}. {game} - Players: {players}", font=("Helvetica", 12), fg="white", bg="#2e3440")
                game_label.pack(pady=5)
        else:
            trending_games_label = tk.Label(trending_games_frame, text="Trending games table not found.", font=("Helvetica", 14), fg="white", bg="#2e3440")
            trending_games_label.pack(pady=10)
    else:
        error_label = tk.Label(top_games_frame, text=f"Failed to retrieve data. Status code: {response.status_code}", font=("Helvetica", 14), fg="white", bg="#2e3440")
        error_label.pack(pady=10)


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

    # Populate the listbox with games from gamestest
    for game in gamestest:
        if game["name"] != "":
            shop_listbox.insert(tk.END, game["name"])

    def buy_game():
        selected_index = shop_listbox.curselection()
        if selected_index:
            # Get the selected game name from the listbox
            selected_game_name = shop_listbox.get(selected_index)

            # Find the corresponding game in gamestest
            selected_game = next((game for game in gamestest if game["name"] == selected_game_name), None)

            if selected_game:
                # Fetch the game details from the Steam API
                game_details = get_app_details(selected_game["appid"])

                if game_details:
                    # Add the selected game to games_gekocht with all details
                    games_gekocht.append({
                        "appid": selected_game["appid"],
                        "name": selected_game["name"],
                        "release_date": game_details.get('release_date', {}).get('date', ''),
                        "developer": ', '.join(game_details.get('developers', [])),
                        "publisher": ', '.join(game_details.get('publishers', [])),
                        "platforms": ', '.join(
                            [platform for platform, supported in game_details.get('platforms', {}).items() if
                             supported]),
                        "genres": ', '.join([genre['description'] for genre in game_details.get('genres', [])]),
                        "price": game_details.get('price_overview', {}).get('final', 0) / 100 if game_details.get(
                            'price_overview') else 0,
                        "achievements": game_details.get('achievements', {}).get('total', 0),
                        "steamspy_tags": ', '.join(game_details.get('steamspy_tags', []))
                    })

                    # Remove the selected game from the shop_listbox
                    shop_listbox.delete(selected_index)
                    print(f"Game '{selected_game['name']}' added to games_gekocht.")  # Debug statement
                else:
                    print("Error: Failed to fetch game details from Steam API.")  # Debug statement
            else:
                print("Error: Selected game not found in gamestest.")  # Debug statement

    def on_game_select(event):
        selected_index = shop_listbox.curselection()
        if selected_index:
            # Ensure the selected index corresponds to the correct game in gamestest
            selected_game_name = shop_listbox.get(selected_index)
            game = next((g for g in gamestest if g["name"] == selected_game_name), None)

            if game:
                print(f"Selected Game: {game['name']}, AppID: {game['appid']}")  # Debug statement
                open_game_details(game)
            else:
                print("Error: Selected game not found in gamestest.")

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

    # Populate the listbox with games from games_gekocht
    for game in games_gekocht:
        possessions_listbox.insert(tk.END, game["name"])

    def donate_game():
        selected_index = possessions_listbox.curselection()
        if selected_index:
            game = games_gekocht.pop(selected_index[0])
            donated_games.append(game)
            possessions_listbox.delete(selected_index)

    def on_game_select(event):
        selected_index = possessions_listbox.curselection()
        if selected_index:
            # Retrieve the selected game from games_gekocht
            selected_game = games_gekocht[selected_index[0]]
            print(f"Selected Game: {selected_game['name']}, AppID: {selected_game['appid']}")  # Debug statement

            # Start the corresponding game class
            if selected_game["appid"] == "raad_het_nummer":
                RaadHetNummer()  # Start RaadHetNummer independently
            elif selected_game["appid"] == "glagje":
                Glagje()  # Start Glagje independently
            elif selected_game["appid"] == "dagboek":
                Dagboek()  # Start Dagboek independently
            elif selected_game["appid"] == "wack_the_mole":
                WackTheMole()  # Start WackTheMole independently
            elif selected_game["appid"] == "Hacker Destroyer 3000":
                subprocess.run(file_path, check=True)

            else:
                open_game_details(selected_game)

    # Bind double-click event to the listbox
    possessions_listbox.bind("<Double-1>", on_game_select)

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


def get_cpu_power_usage(cpu_usage, tdp=95, idle_power=10):
    """
    Estimate CPU power consumption based on CPU usage, TDP, and idle power.

    :param cpu_usage: CPU usage percentage (from psutil.cpu_percent())
    :param tdp: Thermal Design Power (TDP) of the CPU in watts (default: 95 W)
    :param idle_power: Power consumption when the CPU is idle in watts (default: 10 W)
    :return: Estimated CPU power consumption in watts
    """
    return idle_power + (cpu_usage / 100 * (tdp - idle_power))
def get_total_system_power_usage():
    """
    Calculate the total system power usage, including CPU, screen, and other components.

    :return: Total system power usage in watts
    """
    # Get CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # Estimate CPU power usage
    cpu_power = get_cpu_power_usage(cpu_usage)  # Pass cpu_usage as an argument

    # Screen power usage (average for a laptop screen)
    screen_power = 10  # in watts

    # Other components (RAM, storage, peripherals, etc.)
    other_power = 10  # in watts

    # Total system power usage
    total_power = cpu_power + screen_power + other_power
    total_power = round(total_power, 2)


    return total_power
def open_energy_usage():
    energy_window = tk.Toplevel(root)
    energy_window.title("Energieverbruik")
    energy_window.geometry("600x400")
    energy_window.config(bg="#2e3440")

    energy_title = tk.Label(energy_window, text="Huidig Energieverbruik", font=("Helvetica", 18), fg="white",
                            bg="#2e3440")
    energy_title.pack(pady=20)

    global energy_info
    energy_info = tk.Label(energy_window, text="Je huidige energieverbruik is: 0 W", font=("Helvetica", 14),
                           fg="white", bg="#2e3440")
    energy_info.pack(pady=20)

    back_button = tk.Button(energy_window, text="Terug naar Dashboard", command=energy_window.destroy, bg="#81a1c1",
                            fg="white", font=("Helvetica", 10), relief="flat")
    back_button.pack(pady=20)

    update_live_energy_usage(energy_info)  # Start de dynamische update van het energieverbruik
def update_live_energy_usage(label):
    # Get the current power usage
    power_usage = get_total_system_power_usage()

    # Update the label text
    label.config(text=f"Je huidige energieverbruik is: {power_usage} W")

    # Schedule the function to run again after 1 second
    label.after(1000, update_live_energy_usage, label)





def load_users():
    # Maak verbinding met de database
    connection_string = "host='20.162.218.244' dbname='steamdatabase' user='postgres' password='Diana112????'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # Query om gebruikers op te halen
    query = "SELECT gebruikersnaam, wachtwoord FROM Klant"
    cursor.execute(query)

    # Haal alle gebruikers op en zet ze om in een lijst van dictionaries
    users = cursor.fetchall()
    user_list = [{"username": user[0], "password": user[1]} for user in users]

    # Sluit de verbinding
    conn.close()

    return user_list


def show_signup(parent):
    signup_window = tk.Toplevel(parent)
    signup_window.title("Account Aanmaken")
    signup_window.geometry("300x300")
    signup_window.resizable(False, False)
    signup_window.config(bg="#2e3440")

    username_label = tk.Label(signup_window, text="Username:", fg="#d8dee9", bg="#2e3440")
    username_label.pack(pady=5)
    username_entry = tk.Entry(signup_window, width=25, bg="#3b4252", fg="#d8dee9", insertbackground="#d8dee9")
    username_entry.pack(pady=5)

    password_label = tk.Label(signup_window, text="Password:", fg="#d8dee9", bg="#2e3440")
    password_label.pack(pady=5)
    password_entry = tk.Entry(signup_window, show="*", width=25, bg="#3b4252", fg="#d8dee9", insertbackground="#d8dee9")
    password_entry.pack(pady=5)

    confirm_password_label = tk.Label(signup_window, text="Confirm Password:", fg="#d8dee9", bg="#2e3440")
    confirm_password_label.pack(pady=5)
    confirm_password_entry = tk.Entry(signup_window, show="*", width=25, bg="#3b4252", fg="#d8dee9",
                                      insertbackground="#d8dee9")
    confirm_password_entry.pack(pady=5)

    def create_account():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Fout", "Wachtwoorden komen niet overeen!")
            return

        # Check of de username al bestaat
        users = load_users()
        if any(user['username'] == username for user in users):
            messagebox.showerror("Fout", "Deze gebruikersnaam is al in gebruik!")
            return

        # Voeg de nieuwe gebruiker toe aan de database
        add_user_to_db(username, password)
        messagebox.showinfo("Succes", "Account is succesvol aangemaakt!")
        signup_window.destroy()

    signup_button = tk.Button(signup_window, text="Account Aanmaken", command=create_account, bg="#81a1c1", fg="white")
    signup_button.pack(pady=10)

    back_button = tk.Button(signup_window, text="Terug naar Login", command=signup_window.destroy, bg="#81a1c1",
                            fg="white")
    back_button.pack(pady=10)

import bcrypt

def add_user_to_db(username, password):
    # Verbinding maken met de database
    connection_string = "host='20.162.218.244' dbname='steamdatabase' user='postgres' password='Diana112????'"
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # Voeg de nieuwe gebruiker toe aan de database zonder hashing
    query = "INSERT INTO Klant (gebruikersnaam, wachtwoord) VALUES (%s, %s)"
    cursor.execute(query, (username, password))

    # Commit de wijziging en sluit de verbinding
    conn.commit()
    conn.close()



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
    login_button = tk.Button(login_window, text="Login",
                             command=lambda: validate_login(login_window, username_entry, password_entry), bg="#81a1c1",
                             fg="white", width=10)
    login_button.pack(pady=10)

    # Voeg de "Account Aanmaken" knop toe
    signup_button = tk.Button(login_window, text="Account Aanmaken", command=lambda: show_signup(login_window),
                              bg="#88c0d0", fg="black", width=20)
    signup_button.pack(pady=5)

    forgot_button = tk.Button(login_window, text="Forgot Password?", command=forgot_password, bg="#2e3440",
                              fg="#88c0d0", borderwidth=0)
    forgot_button.pack(pady=5)

    login_window.mainloop()


def start_dashboard():
    global root
    root = tk.Tk()
    root.title("Steam Dashboard")
    root.geometry("1400x600")
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

    show_promotional_games()

    footer = tk.Label(root, text="© 2024 Steam Dashboard", font=("Helvetica", 10), fg="#4c566a",
                      bg="#2e3440")
    footer.pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    show_login()


















