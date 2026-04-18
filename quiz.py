import random
import tkinter as tk                  # Tkinter is Python's built-in library for making windows
from tkinter import messagebox         # messagebox shows popup alerts (Correct/Wrong)

# -----------------------------
# Question Bank (grouped by difficulty)
# -----------------------------
# Each difficulty has its own list of (question, correct_answer) pairs.
question_bank = {
    "easy": [
        ("1. What is the capital of Pakistan?\nA) Lahore\nB) Karachi\nC) Islamabad\nD) Peshawar", "C"),
        ("2. 2 + 2 = ?\nA) 3\nB) 4\nC) 5\nD) 6", "B"),
        ("3. Which color is a primary color?\nA) Green\nB) Orange\nC) Red\nD) Purple", "C"),
    ],
    "medium": [
        ("1. Which language is used for AI?\nA) Python\nB) HTML\nC) CSS\nD) Java", "A"),
        ("2. 12 x 5 = ?\nA) 55\nB) 60\nC) 65\nD) 70", "B"),
        ("3. Which planet is known as the Red Planet?\nA) Venus\nB) Earth\nC) Jupiter\nD) Mars", "D"),
    ],
    "hard": [
        ("1. Which data structure uses FIFO order?\nA) Stack\nB) Queue\nC) Tree\nD) Graph", "B"),
        ("2. Square root of 144 = ?\nA) 10\nB) 11\nC) 12\nD) 14", "C"),
        ("3. Which gas is most abundant in Earth's atmosphere?\nA) Oxygen\nB) CO2\nC) Nitrogen\nD) Hydrogen", "C"),
    ],
}

last_score = 0
last_difficulty = ""       # remembers what difficulty the last quiz used

# Variables that hold the quiz while it is running
current_combined = []       # shuffled list of (question, correct_answer) pairs
current_index = 0           # which question we're on
current_score = 0           # running score for the active quiz
current_difficulty = ""     # which difficulty was picked this round


# -----------------------------
# Helper: clear the window before showing a new screen
# -----------------------------
def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


# -----------------------------
# SCREEN: Main Menu
# -----------------------------
def show_menu():
    clear_window()

    tk.Label(window, text="===== QUIZ SYSTEM =====",
             font=("Arial", 16, "bold")).pack(pady=20)

    tk.Button(window, text="1. Start Quiz", width=30, height=2,
              command=choose_difficulty).pack(pady=5)

    tk.Button(window, text="2. View Last Score", width=30, height=2,
              command=view_last_score).pack(pady=5)

    tk.Button(window, text="3. Performance Analysis", width=30, height=2,
              command=performance_analysis).pack(pady=5)

    tk.Button(window, text="4. Exit", width=30, height=2,
              command=window.destroy).pack(pady=5)


# -----------------------------
# SCREEN: Choose Difficulty  (Custom Feature: difficulty levels ✅)
# -----------------------------
def choose_difficulty():
    clear_window()

    tk.Label(window, text="Select Difficulty Level",
             font=("Arial", 16, "bold")).pack(pady=20)

    tk.Button(window, text="1. Easy", width=30, height=2,
              command=lambda: start_quiz("easy")).pack(pady=5)

    tk.Button(window, text="2. Medium", width=30, height=2,
              command=lambda: start_quiz("medium")).pack(pady=5)

    tk.Button(window, text="3. Hard", width=30, height=2,
              command=lambda: start_quiz("hard")).pack(pady=5)

    tk.Button(window, text="Back to Menu", width=30,
              command=show_menu).pack(pady=15)


# -----------------------------
# start_quiz — resets everything and picks the right question list
# -----------------------------
def start_quiz(difficulty):
    global current_combined, current_index, current_score, current_difficulty

    current_difficulty = difficulty
    current_score = 0

    # Randomize questions (Custom Feature 1 ✅)
    current_combined = list(question_bank[difficulty])
    random.shuffle(current_combined)

    current_index = 0
    show_question()


# Show the current question with 4 answer buttons
def show_question():
    clear_window()

    q, ans = current_combined[current_index]

    tk.Label(window,
             text=f"Question {current_index + 1} of {len(current_combined)}   |   Score: {current_score}",
             font=("Arial", 12)).pack(pady=10)

    # Show the full question text (includes the options in the string)
    tk.Label(window, text=q, font=("Arial", 13),
             justify="left", anchor="w").pack(pady=15, padx=30, fill="x")

    # Four answer buttons (A / B / C / D). The user can ONLY click one of these,
    # so input validation is automatic.
    for letter in ["A", "B", "C", "D"]:
        tk.Button(window, text=letter, width=30, height=2,
                  command=lambda L=letter: check_answer(L)).pack(pady=3)


def check_answer(user):
    global current_index, current_score

    q, ans = current_combined[current_index]

    if user == ans:
        current_score += 1
        messagebox.showinfo("Result", "Correct!")
    else:
        current_score -= 0.5   # Negative marking (Custom Feature 2 ✅)
        messagebox.showerror("Result", f"Wrong! Correct answer: {ans}")

    # Move to next question OR finish the quiz
    current_index += 1
    if current_index < len(current_combined):
        show_question()
    else:
        finish_quiz()


def finish_quiz():
    global last_score, last_difficulty

    last_score = current_score
    last_difficulty = current_difficulty

    clear_window()

    tk.Label(window, text="Quiz Finished!",
             font=("Arial", 18, "bold")).pack(pady=20)

    tk.Label(window, text=f"Difficulty: {current_difficulty.capitalize()}",
             font=("Arial", 13)).pack(pady=5)

    tk.Label(window, text=f"Your Score: {current_score}",
             font=("Arial", 14)).pack(pady=10)

    tk.Button(window, text="Back to Menu", width=25, height=2,
              command=show_menu).pack(pady=20)


# -----------------------------
# View Last Score
# -----------------------------
def view_last_score():
    clear_window()

    tk.Label(window, text="Last Score",
             font=("Arial", 16, "bold")).pack(pady=20)

    if last_difficulty == "":
        tk.Label(window, text="No quiz attempt yet.",
                 font=("Arial", 13)).pack(pady=10)
    else:
        tk.Label(window, text=f"Difficulty: {last_difficulty.capitalize()}",
                 font=("Arial", 13)).pack(pady=5)
        tk.Label(window, text=f"Your Last Score: {last_score}",
                 font=("Arial", 14)).pack(pady=10)

    tk.Button(window, text="Back to Menu", width=25, height=2,
              command=show_menu).pack(pady=20)


# -----------------------------
# performance_analysis — same thresholds as before
# -----------------------------
def performance_analysis():
    clear_window()

    tk.Label(window, text="--- Performance Analysis ---",
             font=("Arial", 16, "bold")).pack(pady=15)

    if last_difficulty == "":
        tk.Label(window, text="No quiz attempt yet.\nPlease play a quiz first.",
                 font=("Arial", 13)).pack(pady=15)
        tk.Button(window, text="Back to Menu", width=25, height=2,
                  command=show_menu).pack(pady=20)
        return

    if last_score <= 1:
        level = "Beginner"
        feedback = "Practice basic concepts."
    elif last_score <= 2:
        level = "Intermediate"
        feedback = "You're improving, keep going!"
    else:
        level = "Advanced"
        feedback = "Excellent work!"

    tk.Label(window, text=f"Difficulty: {last_difficulty.capitalize()}",
             font=("Arial", 13)).pack(pady=5)
    tk.Label(window, text=f"Level: {level}",
             font=("Arial", 14, "bold")).pack(pady=8)
    tk.Label(window, text=f"Feedback: {feedback}",
             font=("Arial", 12), wraplength=450).pack(pady=8)

    tk.Button(window, text="Back to Menu", width=25, height=2,
              command=show_menu).pack(pady=20)


# -----------------------------
# Start the app
# -----------------------------
window = tk.Tk()                        # create the main window
window.title("Quiz System")             # title bar text
window.geometry("550x550")              # window size (width x height)

show_menu()                             # draw the first screen
window.mainloop()                       # keep the window open and handle clicks
