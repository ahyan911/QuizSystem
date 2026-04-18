import tkinter as tk  # Import Tkinter library for creating the GUI
from tkinter import messagebox  # Import messagebox to show pop-up messages (like correct or incorrect answers)

# -----------------------------
# Question Bank (Contains all questions and options)
# -----------------------------
question_bank = {
    "easy": [
        {
            "question": "What is the capital of France?",  # The question text
            "options": ["A. Berlin", "B. Paris", "C. Madrid", "D. Rome"],  # List of answer choices
            "answer": "B",  # The correct answer
            "topic": "Geography"  # Topic of the question
        },
        {
            "question": "Which number is even?",  # Another question
            "options": ["A. 7", "B. 9", "C. 12", "D. 15"],
            "answer": "C",
            "topic": "Math"
        },
        {
            "question": "Python is a _____.",
            "options": ["A. Programming Language", "B. Snake only", "C. Game", "D. Browser"],
            "answer": "A",
            "topic": "Programming"
        }
    ],
    "medium": [
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["A. function", "B. def", "C. fun", "D. define"],
            "answer": "B",
            "topic": "Programming"
        },
        {
            "question": "What is 15 * 3?",
            "options": ["A. 30", "B. 35", "C. 45", "D. 50"],
            "answer": "C",
            "topic": "Math"
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["A. Venus", "B. Earth", "C. Jupiter", "D. Mars"],
            "answer": "D",
            "topic": "Science"
        }
    ],
    "hard": [
        {
            "question": "Which data structure uses FIFO order?",
            "options": ["A. Stack", "B. Queue", "C. Tree", "D. Graph"],
            "answer": "B",
            "topic": "Programming"
        },
        {
            "question": "What is the square root of 144?",
            "options": ["A. 10", "B. 11", "C. 12", "D. 14"],
            "answer": "C",
            "topic": "Math"
        },
        {
            "question": "Which gas is most abundant in Earth's atmosphere?",
            "options": ["A. Oxygen", "B. Carbon Dioxide", "C. Nitrogen", "D. Hydrogen"],
            "answer": "C",
            "topic": "Science"
        }
    ]
}

# -----------------------------
# Global Tracking Variables
# -----------------------------
last_score = -1  # Stores the last score
last_total = 0  # Stores total number of questions in the last quiz
last_correct = 0  # Stores the number of correct answers
last_wrong = 0  # Stores the number of incorrect answers
last_level = ""  # Stores the user's performance level (Beginner, Intermediate, Advanced)
last_topic_stats = {}  # Stores statistics about each topic (correct and incorrect answers)
quiz_attempted = False  # Boolean to check if the user has attempted the quiz

# These variables store the current quiz's data while it is being taken
current_questions = []  # List of questions for the current quiz
current_index = 0  # Keeps track of which question the user is on
current_score = 0  # Keeps track of the user's score
current_correct = 0  # Tracks correct answers
current_wrong = 0  # Tracks incorrect answers
current_topic_stats = {}  # Tracks statistics for each topic in the quiz
current_difficulty = ""  # Stores the difficulty level of the current quiz (easy, medium, hard)

# -----------------------------
# Helper Functions (unchanged)
# -----------------------------
def get_performance_level(percentage):
    """Classifies performance based on score percentage."""
    if percentage >= 80:  # If the score is 80% or above, the performance level is "Advanced"
        return "Advanced"
    elif percentage >= 50:  # If the score is between 50% and 79%, the performance level is "Intermediate"
        return "Intermediate"
    else:  # If the score is below 50%, the performance level is "Beginner"
        return "Beginner"


def get_feedback(level, percentage, weak_topics):
    """Generates feedback based on the performance level and weak topics."""
    if level == "Advanced":
        message = "Excellent work! You have a strong understanding of the quiz topics."
    elif level == "Intermediate":
        message = "Good effort! You understand many concepts, but there is room for improvement."
    else:
        message = "You need more practice. Focus on basics and revise weak areas."

    if len(weak_topics) > 0:
        message += "\nWeak areas: " + ", ".join(weak_topics)  # Lists weak topics

    if percentage == 100:
        message += "\nPerfect score. Outstanding performance!"  # If the user gets a perfect score
    elif percentage < 40:
        message += "\nSuggestion: Practice easier questions first and build confidence."  # If the score is low

    return message


# -----------------------------
# Helper: clear the window before showing a new screen
# -----------------------------
def clear_window():
    """Clears all widgets from the Tkinter window."""
    for widget in window.winfo_children():
        widget.destroy()  # Destroys each widget (label, button, etc.) in the current window


# =========================================================
# SCREEN: Main Menu  (replaces the console main menu)
# =========================================================
def show_menu():
    """Displays the main menu with options to start quiz, view last score, and analyze performance."""
    clear_window()

    # Title of the app
    tk.Label(window, text="Smart Quiz & Performance Analyzer",
             font=("Arial", 16, "bold")).pack(pady=20)

    # Buttons for the main menu
    tk.Button(window, text="1. Start Quiz", width=30, height=2,
              bg="#4CAF50", fg="white", command=choose_difficulty).pack(pady=5)

    tk.Button(window, text="2. View Last Score", width=30, height=2,
              bg="#2196F3", fg="white", command=view_last_score).pack(pady=5)

    tk.Button(window, text="3. Performance Analysis", width=30, height=2,
              bg="#FF9800", fg="black", command=performance_analysis).pack(pady=5)

    tk.Button(window, text="4. Exit", width=30, height=2,
              bg="#f44336", fg="white", command=window.destroy).pack(pady=5)


# =========================================================
# SCREEN: Choose Difficulty  (replaces choose_difficulty console prompt)
# =========================================================
def choose_difficulty():
    """Displays the difficulty level selection screen."""
    clear_window()

    tk.Label(window, text="Select Difficulty Level",
             font=("Arial", 16, "bold")).pack(pady=20)

    # Buttons to select difficulty level
    tk.Button(window, text="1. Easy", width=30, height=2,
              bg="#4CAF50", fg="white", command=lambda: start_quiz("easy")).pack(pady=5)

    tk.Button(window, text="2. Medium", width=30, height=2,
              bg="#2196F3", fg="white", command=lambda: start_quiz("medium")).pack(pady=5)

    tk.Button(window, text="3. Hard", width=30, height=2,
              bg="#FF9800", fg="black", command=lambda: start_quiz("hard")).pack(pady=5)

    # Button to return to the main menu
    tk.Button(window, text="Back to Menu", width=30,
              bg="#f44336", fg="white", command=show_menu).pack(pady=15)


# =========================================================
# Core Feature: start_quiz  (same logic, just uses windows)
# =========================================================
def start_quiz(difficulty):
    """Starts the quiz based on the chosen difficulty."""
    global current_questions, current_index, current_score
    global current_correct, current_wrong, current_topic_stats, current_difficulty

    current_difficulty = difficulty
    current_questions = question_bank[difficulty]
    current_index = 0
    current_score = 0
    current_correct = 0
    current_wrong = 0
    current_topic_stats = {}

    # Initialize topic tracking  (same as original)
    for q in current_questions:
        topic = q["topic"]
        if topic not in current_topic_stats:
            current_topic_stats[topic] = {"correct": 0, "wrong": 0}

    ask_question()


# =========================================================
# Replaces: ask_question() from the console version
# =========================================================
def ask_question():
    """Displays the current question and answer options."""
    clear_window()

    q = current_questions[current_index]
    question_number = current_index + 1

    # Shows question number and score
    tk.Label(window,
             text=f"Question {question_number} of {len(current_questions)}   |   Score: {current_score}",
             font=("Arial", 12)).pack(pady=10)

    # Displays the question text
    tk.Label(window, text=q["question"],
             font=("Arial", 14), wraplength=450, justify="left").pack(pady=15)

    # Buttons for each option (A, B, C, D)
    for option in q["options"]:
        letter = option[0]  # Extracts "A", "B", "C", or "D" from the option
        tk.Button(window, text=option, width=40, height=2,
                  bg="#4CAF50", fg="white", command=lambda L=letter: check_answer(L)).pack(pady=4)


# =========================================================
# Replaces the "if user_answer == q["answer"]" block
# =========================================================
def check_answer(user_answer):
    """Checks if the user's selected answer is correct."""
    global current_index, current_score, current_correct, current_wrong

    q = current_questions[current_index]

    # If the answer is correct, increase score and correct count
    if user_answer == q["answer"]:
        current_score += 1
        current_correct += 1
        current_topic_stats[q["topic"]]["correct"] += 1
        messagebox.showinfo("Result", "Correct!")
    else:
        # If the answer is wrong, deduct marks and increase wrong count
        current_score -= 0.25
        current_wrong += 1
        current_topic_stats[q["topic"]]["wrong"] += 1
        messagebox.showerror(
            "Result",
            f"Wrong! Correct answer is: {q['answer']}"
        )

    # Move to next question or show results if the quiz is over
    current_index += 1
    if current_index < len(current_questions):
        ask_question()
    else:
        finish_quiz()


# =========================================================
# Replaces the "Quiz Completed!" print block
# =========================================================
def finish_quiz():
    """Displays the final score and performance analysis after quiz completion."""
    global last_score, last_total, last_correct, last_wrong
    global last_level, last_topic_stats, quiz_attempted

    total_questions = len(current_questions)
    percentage = (current_correct / total_questions) * 100
    level = get_performance_level(percentage)

    # Save the results for later review
    last_score = current_score
    last_total = total_questions
    last_correct = current_correct
    last_wrong = current_wrong
    last_level = level
    last_topic_stats = current_topic_stats
    quiz_attempted = True

    clear_window()

    tk.Label(window, text="Quiz Completed!",
             font=("Arial", 18, "bold")).pack(pady=15)

    # Displays the result summary
    info = (f"Difficulty     : {current_difficulty.capitalize()}\n"
            f"Correct Answers: {current_correct}\n"
            f"Wrong Answers  : {current_wrong}\n"
            f"Final Score    : {current_score} / {total_questions}\n"
            f"Percentage     : {percentage}%\n"
            f"Performance    : {level}")

    tk.Label(window, text=info, font=("Courier", 12),
             justify="left").pack(pady=10)

    # Back to Menu button
    tk.Button(window, text="Back to Menu", width=25, height=2,
              bg="#f44336", fg="white", command=show_menu).pack(pady=15)


# =========================================================
# Replaces: view_last_score() console output
# =========================================================
def view_last_score():
    """Displays the score of the last quiz attempt."""
    clear_window()

    tk.Label(window, text="Last Quiz Score",
             font=("Arial", 16, "bold")).pack(pady=15)

    if not quiz_attempted:
        tk.Label(window, text="No quiz attempt found.",
                 font=("Arial", 12)).pack(pady=20)
    else:
        percentage = (last_correct / last_total) * 100
        info = (f"Difficulty Level: {last_level}\n"
                f"Correct Answers : {last_correct}\n"
                f"Wrong Answers   : {last_wrong}\n"
                f"Score           : {last_score} / {last_total}\n"
                f"Percentage      : {percentage}%")
        tk.Label(window, text=info, font=("Courier", 12),
                 justify="left").pack(pady=10)

    tk.Button(window, text="Back to Menu", width=25, height=2,
              bg="#f44336", fg="white", command=show_menu).pack(pady=15)


# =========================================================
# Replaces: performance_analysis() console output
# =========================================================
def performance_analysis():
    """Displays detailed performance analysis after quiz completion."""
    clear_window()

    tk.Label(window, text="Performance Analysis",
             font=("Arial", 16, "bold")).pack(pady=15)

    if not quiz_attempted:
        tk.Label(window, text="No quiz attempt found.\nPlease start the quiz first.",
                 font=("Arial", 12)).pack(pady=20)
        tk.Button(window, text="Back to Menu", width=25, height=2,
                  bg="#f44336", fg="white", command=show_menu).pack(pady=15)
        return

    percentage = (last_correct / last_total) * 100
    weak_topics = []
    strong_topics = []

    lines = []
    lines.append(f"Performance Level: {last_level}")
    lines.append(f"Percentage       : {percentage}%")
    lines.append("")

    for topic in last_topic_stats:
        correct = last_topic_stats[topic]["correct"]
        wrong = last_topic_stats[topic]["wrong"]

        lines.append(f"Topic  : {topic}")
        lines.append(f"Correct: {correct}")
        lines.append(f"Wrong  : {wrong}")
        lines.append("")

        if wrong > correct:
            weak_topics.append(topic)
        elif correct > wrong:
            strong_topics.append(topic)

    if len(strong_topics) > 0:
        lines.append("Strong Areas: " + ", ".join(strong_topics))
    else:
        lines.append("Strong Areas: None identified")

    if len(weak_topics) > 0:
        lines.append("Weak Areas  : " + ", ".join(weak_topics))
    else:
        lines.append("Weak Areas  : None")

    lines.append("")
    lines.append("Feedback:")
    lines.append(get_feedback(last_level, percentage, weak_topics))

    tk.Label(window, text="\n".join(lines), font=("Courier", 11),
             justify="left").pack(pady=10, padx=20)

    tk.Button(window, text="Back to Menu", width=25, height=2,
              bg="#f44336", fg="white", command=show_menu).pack(pady=15)


# -----------------------------
# Start the app
# -----------------------------
window = tk.Tk()  # Create the main window for the quiz app
window.title("Smart Quiz & Performance Analyzer")  # Set the title of the window
window.geometry("550x600")  # Set the window size (width x height)

show_menu()  # Display the main menu when the app starts
window.mainloop()  # Start the Tkinter main loop (this keeps the app running)
