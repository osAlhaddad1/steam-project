import customtkinter as ctk
import tkinter as tk
from datetime import datetime
import os
import random

# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class WackTheMole:
    def __init__(self, parent_frame=None):
        if parent_frame is None:
            # Initialize a new Tkinter root window
            self.root = ctk.CTk()
            self.root.title("Wack The Mole")
            self.root.geometry("800x600")
            self.root.resizable(False, False)

            # Use the root window as the parent frame
            self.parent_frame = self.root
        else:
            # Use the provided parent frame
            self.parent_frame = parent_frame

        self.grid_size = 3
        self.buttons_matrix = ctk.CTkFrame(self.parent_frame)
        self.mole_speed = 1000
        self.buttons = []
        self.mole_position = None
        self.score = 0
        self.game_running = True

        self.difficulty_label = ctk.CTkLabel(self.parent_frame, text="Select Difficulty", font=("Arial", 16))
        self.difficulty_label.pack(pady=10)

        # Difficulty buttons
        self.easy_button = ctk.CTkButton(self.parent_frame, text="Easy", command=lambda: self.start_game(3, 2000))
        self.medium_button = ctk.CTkButton(self.parent_frame, text="Medium", command=lambda: self.start_game(5, 700))
        self.hard_button = ctk.CTkButton(self.parent_frame, text="Hard", command=lambda: self.start_game(7, 500))

        self.easy_button.pack(pady=5)
        self.medium_button.pack(pady=5)
        self.hard_button.pack(pady=5)

        # Start the Tkinter main loop if running independently
        if parent_frame is None:
            self.root.mainloop()

    def start_game(self, grid_size, mole_speed):
        self.grid_size = grid_size
        self.mole_speed = mole_speed

        self.difficulty_label.pack_forget()
        self.easy_button.pack_forget()
        self.medium_button.pack_forget()
        self.hard_button.pack_forget()

        self.score_label = ctk.CTkLabel(self.parent_frame, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.place(relx=0.03, rely=0.08, anchor="nw")

        self.buttons_matrix.place(relx=0.5, rely=0.5, anchor="c")

        for row in range(self.grid_size):
            button_row = []
            for col in range(self.grid_size):
                button = ctk.CTkButton(self.buttons_matrix, text="", width=80, height=80, fg_color="grey", command=lambda r=row, c=col: self.whack(r, c))
                button.grid(row=row+1, column=col, padx=5, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

        self.move_mole()

    def move_mole(self):
        if not self.game_running:
            return

        if self.mole_position:
            self.buttons[self.mole_position[0]][self.mole_position[1]].configure(text="", fg_color="grey")

        row, col = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
        self.mole_position = (row, col)

        self.buttons[row][col].configure(text="Mole", fg_color="brown")

        self.parent_frame.after(self.mole_speed, self.move_mole)

    def whack(self, row, col):
        if (row, col) == self.mole_position:
            self.score += 1
            self.score_label.configure(text=f"Score: {self.score}")
            self.buttons[row][col].configure(text="", fg_color="grey")
        else:
            self.game_over()

    def game_over(self):
        self.game_running = False
        for row in self.buttons:
            for button in row:
                button.configure(state="disabled")
        self.score_label.configure(text=f"Game Over! Final Score: {self.score}")

    def back_to_main(self):
        # Destroy the game frame and switch back to the main menu
        self.buttons_matrix.destroy()
        if hasattr(self, 'root'):
            self.root.destroy()  # Close the independent window
class Dagboek:
    def __init__(self, parent_frame=None):
        if parent_frame is None:
            # Initialize a new Tkinter root window
            self.root = ctk.CTk()
            self.root.title("Dagboek")
            self.root.geometry("800x600")
            self.root.resizable(False, False)

            # Use the root window as the parent frame
            self.parent_frame = self.root
        else:
            # Use the provided parent frame
            self.parent_frame = parent_frame

        # Initialize diary variables
        self.notes = []
        self.notes_file = "notes.txt"

        # Dagboek Frame
        self.dagboek_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.dagboek_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        self.dagboek_title = ctk.CTkLabel(
            self.dagboek_frame,
            text="Dagboek",
            font=("fixedsys", 20, "bold")
        )
        self.dagboek_title.pack(pady=(0, 10))

        # Notes Frame
        self.notes_frame = ctk.CTkScrollableFrame(self.dagboek_frame, height=200)
        self.notes_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Entry for new note
        self.note_entry = ctk.CTkTextbox(self.dagboek_frame, height=100, wrap='word', font=("fixedsys", 14))
        self.note_entry.pack(fill="x", padx=10, pady=10)

        # Add Note Button
        self.add_note_button = ctk.CTkButton(
            self.dagboek_frame,
            text="Add Note",
            command=self.save_note,
            font=("fixedsys", 14)
        )
        self.add_note_button.pack(pady=10)

        # Back Button
        # self.dagboek_back_button = ctk.CTkButton(
        #     self.dagboek_frame,
        #     text="Back to Main Menu",
        #     command=self.back_to_main,
        #     font=("fixedsys", 12)
        # )
        # self.dagboek_back_button.pack(pady=10)

        # Load notes from file after initializing notes_frame
        self.load_notes()

        # Start the Tkinter main loop if running independently
        if parent_frame is None:
            self.root.mainloop()

    def load_notes(self):
        if os.path.exists(self.notes_file):
            with open(self.notes_file, "r", encoding="utf-8") as file:
                note_text = ""
                for line in file:
                    line = line.strip()
                    if " || " not in line:
                        note_text += line + "\n"
                        continue
                    else:
                        note_text += line.split(" || ")[0]
                        timestamp = line.split(" || ")[1]
                        self.notes.append((note_text.strip(), timestamp))
                        note_text = ""
        self.display_notes()

    def display_notes(self):
        for widget in self.notes_frame.winfo_children():
            widget.destroy()

        for i, (note, timestamp) in enumerate(self.notes):
            note_box = ctk.CTkFrame(self.notes_frame, corner_radius=10, fg_color="#2b2b2b", width=250, height=150)
            note_box.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

            first_line = note.split("\n", 1)[0]
            display_text = first_line[:50] + "..." if len(first_line) > 50 else first_line
            note_label = ctk.CTkLabel(note_box, text=display_text, anchor="w", font=("fixedsys", 14))
            note_label.pack(fill="x", padx=10, pady=5)

            time_label = ctk.CTkLabel(note_box, text=f"Last edited: {timestamp}", anchor="e", font=("fixedsys", 10))
            time_label.pack(fill="x", padx=10, pady=5)

            open_button = ctk.CTkButton(note_box, text="Open", command=lambda n=i: self.open_note_window(n), font=("fixedsys", 12))
            open_button.pack(pady=2)

            delete_button = ctk.CTkButton(note_box, text="Delete", command=lambda n=i: self.delete_note(n), font=("fixedsys", 12))
            delete_button.pack(pady=2)

    def open_note_window(self, note_index):
        note, timestamp = self.notes[note_index]

        note_window = ctk.CTkToplevel(self.parent_frame)
        note_window.geometry("400x350")
        note_window.title("Edit Note")

        note_window.grab_set()
        note_window.focus_force()

        title_label = ctk.CTkLabel(note_window, text="Edit Note", font=("fixedsys", 16, "bold"))
        title_label.pack(pady=10)

        note_textbox = ctk.CTkTextbox(note_window, wrap='word', font=("fixedsys", 14))
        note_textbox.insert("1.0", note)
        note_textbox.pack(fill="both", expand=True, padx=10, pady=10)

        save_button = ctk.CTkButton(
            note_window,
            text="Save",
            command=lambda: self.save_edits(note_index, note_window, note_textbox),
            font=("fixedsys", 14)
        )
        save_button.pack(pady=10)

    def save_notes_to_file(self):
        with open(self.notes_file, "w", encoding="utf-8") as file:
            for note, timestamp in self.notes:
                file.write(f"{note} || {timestamp}\n")

    def save_note(self):
        note_text = self.note_entry.get("1.0", tk.END).strip()
        if note_text:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.notes.append((note_text, timestamp))
            self.note_entry.delete("1.0", tk.END)
            self.save_notes_to_file()
            self.display_notes()

    def save_edits(self, note_index, window, textbox):
        edited_note = textbox.get("1.0", tk.END).strip()
        if edited_note:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.notes[note_index] = (edited_note, timestamp)
            self.save_notes_to_file()
            self.display_notes()
            window.destroy()

    def delete_note(self, note_index):
        del self.notes[note_index]
        self.save_notes_to_file()
        self.display_notes()

    def back_to_main(self):
        # Destroy the game frame and switch back to the main menu
        self.dagboek_frame.destroy()
        if hasattr(self, 'root'):
            self.root.destroy()  # Close the independent window
class Glagje:
    def __init__(self, parent_frame=None):
        if parent_frame is None:
            # Initialize a new Tkinter root window
            self.root = ctk.CTk()
            self.root.title("Glagje")
            self.root.geometry("800x600")
            self.root.resizable(False, False)

            # Use the root window as the parent frame
            self.parent_frame = self.root
        else:
            # Use the provided parent frame
            self.parent_frame = parent_frame

        # Initialize the game frame
        self.glagje_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.glagje_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Try to load the words file
        try:
            with open("words.txt", "r", encoding="utf-8") as words_file:
                self.list_of_possible_words = [line.strip() for line in words_file if line.strip()]
        except FileNotFoundError:
            self.show_error_message("words.txt file not found.")
            return

        if not self.list_of_possible_words:
            self.show_error_message("No words found in words.txt.")
            return

        self.selected_word = random.choice(self.list_of_possible_words).lower()

        # Title
        self.glagje_title = ctk.CTkLabel(
            self.glagje_frame,
            text="Glagje",
            font=("fixedsys", 20, "bold")
        )
        self.glagje_title.pack(pady=(0, 10))

        # Display for current guess state
        self.current_guess_var = ctk.StringVar(value="_ " * len(self.selected_word))
        self.current_guess_label = ctk.CTkLabel(
            self.glagje_frame,
            textvariable=self.current_guess_var,
            font=("fixedsys", 16)
        )
        self.current_guess_label.pack(pady=10)

        # Input Frame
        self.glagje_input_frame = ctk.CTkFrame(self.glagje_frame, fg_color="transparent")
        self.glagje_input_frame.pack(pady=10)

        # Entry for letter guess
        self.glagje_entry = ctk.CTkEntry(
            self.glagje_input_frame,
            placeholder_text="Enter a letter",
            width=200,
            font=("fixedsys", 14)
        )
        self.glagje_entry.grid(row=0, column=0, padx=5, pady=5)

        # Guess Button
        self.glagje_guess_button = ctk.CTkButton(
            self.glagje_input_frame,
            text="Guess",
            command=self.process_glagje_guess,
            font=("fixedsys", 14)
        )
        self.glagje_guess_button.grid(row=0, column=1, padx=5, pady=5)

        # Feedback Label
        self.glagje_feedback_var = ctk.StringVar(value="")
        self.glagje_feedback_label = ctk.CTkLabel(
            self.glagje_frame,
            textvariable=self.glagje_feedback_var,
            font=("fixedsys", 12),
            text_color="yellow"
        )
        self.glagje_feedback_label.pack(pady=5)

        # Back Button
        # self.glagje_back_button = ctk.CTkButton(
        #     self.glagje_frame,
        #     text="Back to Main Menu",
        #     command=self.back_to_main,
        #     font=("fixedsys", 12)
        # )
        # self.glagje_back_button.pack(pady=10)

        # Initialize game state
        self.glagje_display = ["_"] * len(self.selected_word)
        self.guessed_letters = set()
        self.glagje_feedback_var.set(f"Word has {len(self.selected_word)} letters.")

        # Start the Tkinter main loop if running independently
        if parent_frame is None:
            self.root.mainloop()

    def process_glagje_guess(self):
        user_input = self.glagje_entry.get().strip().lower()
        if not user_input or len(user_input) != 1 or not user_input.isalpha():
            self.glagje_feedback_var.set("Please enter a single letter.")
            return

        if user_input in self.guessed_letters:
            self.glagje_feedback_var.set(f"You already guessed '{user_input}'.")
            return

        self.guessed_letters.add(user_input)

        if user_input in self.selected_word:
            for idx, letter in enumerate(self.selected_word):
                if letter == user_input:
                    self.glagje_display[idx] = user_input
            self.current_guess_var.set(" ".join(self.glagje_display))
            self.glagje_feedback_var.set(f"Good job! '{user_input}' is in the word.")

            if "_" not in self.glagje_display:
                self.glagje_feedback_var.set("Congratulations! You guessed the word.")
                self.end_glagje_game(won=True)
        else:
            self.glagje_feedback_var.set(f"'{user_input}' is not in the word.")

    def end_glagje_game(self, won):
        self.glagje_entry.configure(state="disabled")
        self.glagje_guess_button.configure(state="disabled")
        if won:
            final_message = ctk.CTkLabel(
                self.glagje_frame,
                text="Congratulations! You won!",
                font=("fixedsys", 16, "bold"),
                text_color="green"
            )
            final_message.pack(pady=10)
        else:
            final_message = ctk.CTkLabel(
                self.glagje_frame,
                text=f"You lost! The word was '{self.selected_word}'.",
                font=("fixedsys", 16, "bold"),
                text_color="red"
            )
            final_message.pack(pady=10)

    def back_to_main(self):
        # Destroy the game frame and switch back to the main menu
        self.glagje_frame.destroy()
        if hasattr(self, 'root'):
            self.root.destroy()  # Close the independent window

    def show_error_message(self, message):
        error_label = ctk.CTkLabel(
            self.glagje_frame,
            text=message,
            text_color="red",
            font=("fixedsys", 14)
        )
        error_label.pack(pady=10)
class RaadHetNummer:
    def __init__(self, parent_frame=None):
        if parent_frame is None:
            # Initialize a new Tkinter root window
            self.root = ctk.CTk()
            self.root.title("Raad het Nummer")
            self.root.geometry("800x600")
            self.root.resizable(False, False)

            # Use the root window as the parent frame
            self.parent_frame = self.root
        else:
            # Use the provided parent frame
            self.parent_frame = parent_frame

        # Initialize game variables
        self.number_to_guess = random.randint(1, 6)
        self.lives = 3
        self.points = 600

        # Game Frame
        self.game_frame = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        self.game_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        self.game_title = ctk.CTkLabel(
            self.game_frame,
            text="Raad het Nummer",
            font=("fixedsys", 20, "bold")
        )
        self.game_title.pack(pady=(0, 10))

        # Description
        self.description = ctk.CTkLabel(
            self.game_frame,
            text="We have thrown a dice that has six numbers, from 1 to 6.\nTry to guess the number!",
            font=("fixedsys", 14),
            justify="center"
        )
        self.description.pack(pady=(0, 20))

        # Lives Counter
        self.lives_var = ctk.StringVar(value=f"Lives: {self.lives}")
        self.lives_label = ctk.CTkLabel(
            self.game_frame,
            textvariable=self.lives_var,
            font=("fixedsys", 14)
        )
        self.lives_label.pack(pady=(0, 10))

        # Points Counter
        self.points_var = ctk.StringVar(value=f"Points: {self.points}")
        self.points_label = ctk.CTkLabel(
            self.game_frame,
            textvariable=self.points_var,
            font=("fixedsys", 14)
        )
        self.points_label.pack(pady=(0, 10))

        # Entry for bet amount
        self.bet_entry = ctk.CTkEntry(
            self.game_frame,
            placeholder_text="Enter your bet",
            width=200,
            font=("fixedsys", 14)
        )
        self.bet_entry.pack(pady=10)

        # Input Frame
        self.input_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        self.input_frame.pack(pady=10)

        # Entry for guess
        self.guess_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter your guess (1-6)",
            width=200,
            font=("fixedsys", 14)
        )
        self.guess_entry.grid(row=0, column=0, padx=5, pady=5)

        # Easy Mode Checkbox
        self.easy_mode_var = ctk.IntVar(value=1)
        self.easy_mode_checkbox = ctk.CTkCheckBox(
            self.input_frame,
            text="Easy Mode",
            variable=self.easy_mode_var,
            font=("fixedsys", 12)
        )
        self.easy_mode_checkbox.grid(row=0, column=1, padx=5, pady=5)

        # Guess Button
        self.guess_button = ctk.CTkButton(
            self.game_frame,
            text="Guess",
            command=self.process_guess_with_bet,
            font=("fixedsys", 14)
        )
        self.guess_button.pack(pady=10)

        # Feedback Label
        self.feedback_var = ctk.StringVar(value="")
        self.feedback_label = ctk.CTkLabel(
            self.game_frame,
            textvariable=self.feedback_var,
            font=("fixedsys", 12),
            text_color="yellow"
        )
        self.feedback_label.pack(pady=5)

        # Back Button
        # self.back_button = ctk.CTkButton(
        #     self.game_frame,
        #     text="Back to Main Menu",
        #     command=self.back_to_main,
        #     font=("fixedsys", 12)
        # )
        # self.back_button.pack(pady=10)

        # Start the Tkinter main loop if running independently
        if parent_frame is None:
            self.root.mainloop()

    def process_guess_with_bet(self):
        if self.lives <= 0:
            self.feedback_var.set("No lives left. You lost!")
            return

        try:
            bet = int(self.bet_entry.get())
            if bet <= 0 or bet > self.points:
                self.feedback_var.set("Please enter a valid bet within your points.")
                return
        except ValueError:
            self.feedback_var.set("Invalid bet. Please enter a number.")
            return

        try:
            guess = int(self.guess_entry.get())
            if guess < 1 or guess > 6:
                self.feedback_var.set("Please enter a number between 1 and 6.")
                return
        except ValueError:
            self.feedback_var.set("Invalid input. Please enter a number.")
            return

        if guess == self.number_to_guess:
            self.feedback_var.set("Good Job!! You guessed correctly!")
            self.points += bet
            self.end_game(won=True)
        else:
            self.lives -= 1
            self.lives_var.set(f"Lives: {self.lives}")
            if self.lives == 0:
                self.points -= bet
                self.feedback_var.set(f"You Lost!! The number was {self.number_to_guess}.")
                self.end_game(won=False)
            else:
                if self.easy_mode_var.get():
                    hint = "too high" if guess > self.number_to_guess else "too low"
                    self.feedback_var.set(f"Incorrect! You are {hint}.")
                else:
                    self.feedback_var.set("Incorrect! Try again!")

        self.points_var.set(f"Points: {self.points}")

    def end_game(self, won):
        self.guess_entry.configure(state="disabled")
        self.guess_button.configure(state="disabled")
        self.bet_entry.configure(state="disabled")
        if won:
            final_message = ctk.CTkLabel(
                self.game_frame,
                text="Congratulations! You won!",
                font=("fixedsys", 16, "bold"),
                text_color="green"
            )
            final_message.pack(pady=10)
        else:
            final_message = ctk.CTkLabel(
                self.game_frame,
                text="Better luck next time!",
                font=("fixedsys", 16, "bold"),
                text_color="red"
            )
            final_message.pack(pady=10)

    def back_to_main(self):
        # Destroy the game frame and switch back to the main menu
        self.game_frame.destroy()
        if hasattr(self, 'root'):
            self.root.destroy()  # Close the independent window
class NanoAppStore:
    def __init__(self):
        # Initialize the main window
        self.root = ctk.CTk()
        self.root.title("O.S. App Store")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Main container frame
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both")

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Nano App Store",
            font=("fixedsys", 90, "bold"),
            pady=50
        )
        self.title_label.pack()

        # Instruction Text
        self.instruction_label = ctk.CTkLabel(
            self.main_frame,
            text="Select the application you want:",
            font=("fixedsys", 16)
        )
        self.instruction_label.pack(pady=(0, 10))

        # Option Menu for selecting applications
        self.app_options = ["Raad het Nummer", "Glagje", "Dagboek", "Wack The Mole"]
        self.app_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=self.app_options,
            command=self.load_app,
            font=("fixedsys", 14)
        )
        self.app_menu.pack(pady=10)

        # The Start Button
        self.start_button = ctk.CTkButton(
            self.main_frame,
            text="Start",
            command=self.start_selected_app,
            font=("fixedsys", 14)
        )
        self.start_button.pack(pady=20)

        self.selected_app = self.app_options[0]

        self.root.mainloop()

    def load_app(self, choice):
        self.selected_app = choice

    def start_selected_app(self):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if self.selected_app == "Raad het Nummer":
            RaadHetNummer(self.main_frame)
        elif self.selected_app == "Glagje":
            Glagje(self.main_frame)
        elif self.selected_app == "Dagboek":
            Dagboek(self.main_frame)
        elif self.selected_app == "Wack The Mole":
            WackTheMole(self.main_frame)

    def back_to_main(self):
        # Clear the current frame and reinitialize the main menu
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.__init__()


if __name__ == "__main__":
    NanoAppStore()