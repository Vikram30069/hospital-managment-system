import tkinter as tk
from tkinter import messagebox
import hospital_management  # Import next page after login

def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "admin" and password == "1234":
        root.destroy()
        hospital_management.open_hospital_management()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

root = tk.Tk()
root.title("Login - Hospital Management System")
root.geometry("300x200")

tk.Label(root, text="Username:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Password:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

tk.Button(root, text="Login", command=login).pack(pady=20)

root.mainloop()
