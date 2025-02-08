import tkinter as tk
from tkinter import messagebox, Text
import speech_recognition as sr
import pyttsx3
import time
import threading

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Function to Speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to Recognize Voice
def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand.")
            return None
        except sr.RequestError:
            speak("Error connecting to speech service.")
            return None

# Function to Add Task
def add_task():
    task = entry.get() or recognize_voice()
    if task:
        listbox.insert(tk.END, task)
        speak(f"Task {task} added.")
        entry.delete(0, tk.END)

# Function to Delete Selected Task
def delete_task():
    try:
        selected_task = listbox.get(tk.ACTIVE)
        listbox.delete(tk.ACTIVE)
        speak(f"Task {selected_task} deleted.")
    except:
        speak("No task selected to delete.")

# Function to Delete All Tasks
def delete_all_tasks():
    listbox.delete(0, tk.END)
    speak("All tasks deleted.")

# Function to Exit the App
def exit_app():
    speak("Closing the application")
    root.quit()

# Function to Start Timer
def start_timer():
    time_input = timer_entry.get() or recognize_voice()
    
    if time_input:
        try:
            # Extract number of seconds from input (supports "10 seconds" or just "10")
            seconds = int("".join(filter(str.isdigit, time_input)))
            
            if seconds > 0:
                speak(f"Timer set for {seconds} seconds.")
                threading.Thread(target=countdown, args=(seconds,), daemon=True).start()
            else:
                speak("Please enter a valid time.")
        except ValueError:
            speak("Invalid time input.")

# Function to Run Countdown
def countdown(seconds):
    while seconds:
        minutes, secs = divmod(seconds, 60)
        time_format = f"{minutes:02d}:{secs:02d}"
        timer_label.config(text=time_format)
        time.sleep(1)
        seconds -= 1
    speak("Time is up!")
    timer_label.config(text="00:00")
    messagebox.showinfo("Timer Alert", "Time is up!")
    buzzer()

# Function to Play Buzzer Sound
def buzzer():
    for _ in range(5):
        print('\a')
        time.sleep(1)

# Function to Change Color Theme
def change_color_theme(color):
    root.configure(bg=color)
    frame_entry.configure(bg=color)
    frame_listbox.configure(bg=color)
    frame_buttons.configure(bg=color)
    frame_timer.configure(bg=color)
    label_title.configure(bg=color)
    label_timer.configure(bg=color)
    timer_label.configure(bg=color)

# Placeholder functions for menu items
def focus_mode():
    speak("Focus Mode activated!")

def set_alarm():
    speak("Set your alarm!")

# Function to Open Notepad
def open_notepad():
    # Create a new Toplevel window
    notepad_window = tk.Toplevel(root)
    notepad_window.title("Notepad")
    notepad_window.geometry("400x400")

    # Create Text widget for note-taking
    text_widget = Text(notepad_window, font=("Helvetica", 14), wrap="word")
    text_widget.pack(expand=True, fill="both")

# Create GUI Window
root = tk.Tk()
root.title("Voice-Controlled To-Do List with Timer")
root.geometry("600x600")
root.configure(bg="#f0f4f7")

# Create Menu Button
menu_button = tk.Menubutton(root, text="⚙", font=("Helvetica", 18), bg="#42a5f5", fg="white", bd=0, relief="flat")
menu_button.pack(pady=20, padx=20, anchor="ne")  # Adjusted to place in top-right corner

menu = tk.Menu(menu_button, tearoff=0)
menu_button.config(menu=menu)

menu.add_command(label="Focus Mode", command=focus_mode)
menu.add_command(label="Timer", command=start_timer)
menu.add_command(label="Alarm", command=set_alarm)
menu.add_command(label="Notepad", command=open_notepad)  # New menu option for Notepad

# Add Color Theme Options
color_theme_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Color Theme", menu=color_theme_menu)
color_theme_menu.add_command(label="White", command=lambda: change_color_theme("white"))
color_theme_menu.add_command(label="Black", command=lambda: change_color_theme("black"))
color_theme_menu.add_command(label="Blue", command=lambda: change_color_theme("blue"))
color_theme_menu.add_command(label="Navy Blue", command=lambda: change_color_theme("navyblue"))
color_theme_menu.add_command(label="Orange", command=lambda: change_color_theme("orange"))
color_theme_menu.add_command(label="Pink", command=lambda: change_color_theme("pink"))
color_theme_menu.add_command(label="Purple", command=lambda: change_color_theme("purple"))
color_theme_menu.add_command(label="sky blue", command=lambda: change_color_theme("sky blue"))
color_theme_menu.add_command(label="light green", command=lambda: change_color_theme("light green"))
color_theme_menu.add_command(label="beige", command=lambda: change_color_theme("beige"))
color_theme_menu.add_command(label="#F4C2C2", command=lambda: change_color_theme("#F4C2C2"))
color_theme_menu.add_command(label="fuchsia", command=lambda: change_color_theme("fuchsia"))
color_theme_menu.add_command(label="Aquamarine", command=lambda: change_color_theme("Aquamarine"))


# Title Label
label_title = tk.Label(root, text="The To-Do List", font=("Helvetica", 20, "bold"), fg="#2196f3", bg="#f0f4f7")
label_title.pack(pady=20)

# Task Entry Frame
frame_entry = tk.Frame(root, bg="#f0f4f7")
frame_entry.pack(pady=10)

entry = tk.Entry(frame_entry, width=30, font=("Helvetica", 14), bd=2, relief="groove")
entry.grid(row=0, column=0, padx=10)

btn_add = tk.Button(frame_entry, text="Add Task", command=add_task, bg="#42a5f5", fg="white", font=("Helvetica", 12, "bold"), bd=0, padx=10, pady=5)
btn_add.grid(row=0, column=1, padx=10)

# Task Listbox Frame
frame_listbox = tk.Frame(root, bg="#f0f4f7")
frame_listbox.pack(pady=20)

scrollbar = tk.Scrollbar(frame_listbox, orient="vertical")
listbox = tk.Listbox(frame_listbox, width=40, height=10, font=("Helvetica", 14), yscrollcommand=scrollbar.set, bg="#ffffff", bd=2, relief="sunken")
scrollbar.config(command=listbox.yview)
scrollbar.pack(side="right", fill="y")
listbox.pack(side="left", fill="both", expand=True)

# Button Frame
frame_buttons = tk.Frame(root, bg="#f0f4f7")
frame_buttons.pack(pady=10)

btn_delete = tk.Button(frame_buttons, text="Delete Task", command=delete_task, bg="#ef5350", fg="white", font=("Helvetica", 12, "bold"), bd=0, padx=10, pady=5)
btn_delete.grid(row=0, column=0, padx=10)

btn_delete_all = tk.Button(frame_buttons, text="Delete All Tasks", command=delete_all_tasks, bg="#ef5350", fg="white", font=("Helvetica", 12, "bold"), bd=0, padx=10, pady=5)
btn_delete_all.grid(row=0, column=1, padx=10)

btn_exit = tk.Button(frame_buttons, text="Exit", command=exit_app, bg="#bdbdbd", fg="white", font=("Helvetica", 12, "bold"), bd=0, padx=10, pady=5)
btn_exit.grid(row=0, column=2, padx=10)

# Timer Section
label_timer = tk.Label(root, text="Set Timer (in seconds):", font=("Helvetica", 14), bg="#f0f4f7")
label_timer.pack(pady=10)

frame_timer = tk.Frame(root, bg="#f0f4f7")
frame_timer.pack(pady=5)

timer_entry = tk.Entry(frame_timer, width=10, font=("Helvetica", 14), bd=2, relief="groove")
timer_entry.grid(row=0, column=0, padx=10)

btn_timer = tk.Button(frame_timer, text="Start Timer", command=start_timer, bg="#42a5f5", fg="white", font=("Helvetica", 12, "bold"), bd=0, padx=10, pady=5)
btn_timer.grid(row=0, column=1, padx=10)

# Timer Display Label
timer_label = tk.Label(root, text="00:00", font=("Helvetica", 24, "bold"), bg="#f0f4f7", fg="#d32f2f")
timer_label.pack(pady=20)

# Run the GUI
speak("Welcome to your voice-controlled to-do list with a timer.")
root.mainloop()
