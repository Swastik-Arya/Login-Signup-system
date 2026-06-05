import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

def signup():
    username = entry_user.get()
    password = entry_pass.get()
    if username == "" or password == "":
        messagebox.showwarning("Error", "All fields are required!")
        return
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

def login():
    username = entry_user.get()
    password = entry_pass.get()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    result = cursor.fetchone()
    if result:
        messagebox.showinfo("Login Success", "Welcome " + username)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials!")

root = tk.Tk()
root.title("Login & Signup System")
root.geometry("350x250")
root.resizable(False, False)

tk.Label(root, text="Login / Signup", font=("Arial", 16)).pack(pady=10)
tk.Label(root, text="Username").pack()
entry_user = tk.Entry(root, width=30)
entry_user.pack()
tk.Label(root, text="Password").pack()
entry_pass = tk.Entry(root, width=30, show="*")
entry_pass.pack()
tk.Button(root, text="Login", command=login, width=12, bg="blue", fg="white").pack(pady=5)
tk.Button(root, text="Signup", command=signup, width=12, bg="green", fg="white").pack(pady=5)

root.mainloop()
conn.close()