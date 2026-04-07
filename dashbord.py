import tkinter as tk
from tkinter import messagebox
import subprocess

# ===== LOGIN =====
def login():
    username = entry_user.get()
    password = entry_pass.get()

    if username == "admin" and password == "1234":
        messagebox.showinfo("Login", "Login Successful ✅")
        open_dashboard()
    else:
        messagebox.showerror("Login", "Invalid Credentials ❌")

# ===== DASHBOARD =====
def open_dashboard():
    root.destroy()

    dash = tk.Tk()
    dash.title("Attendance Dashboard")
    dash.geometry("400x300")

    tk.Label(dash, text="Dashboard", font=("Arial", 18)).pack(pady=20)

    tk.Button(dash, text="Start Attendance", width=20,
              command=start_attendance).pack(pady=10)

    tk.Button(dash, text="View Attendance", width=20,
              command=view_attendance).pack(pady=10)

    dash.mainloop()

def start_attendance():
    subprocess.call(["python", "mark_attendance.py"])

def view_attendance():
    subprocess.call(["notepad", "attendance.csv"])

# ===== LOGIN WINDOW =====
root = tk.Tk()
root.title("Login")
root.geometry("300x200")

tk.Label(root, text="Login", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Username").pack()
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Password").pack()
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()