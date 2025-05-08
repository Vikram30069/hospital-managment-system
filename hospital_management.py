import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
# Connect to Database
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    contact TEXT,
    address TEXT
)
""")
conn.commit()

def open_hospital_management():
    root = tk.Tk()
    root.title("Hospital Management System")
    root.geometry("800x600")
    root.configure(bg="#f0f8ff")

    def add_patient():
        name = entry_name.get()
        age = entry_age.get()
        gender = var_gender.get()
        contact = entry_contact.get()
        address = entry_address.get()

        if name == "" or contact == "":
            messagebox.showerror("Error", "Name and Contact are mandatory!")
            return

        cursor.execute("INSERT INTO patients (name, age, gender, contact, address) VALUES (?, ?, ?, ?, ?)",
                       (name, age, gender, contact, address))
        conn.commit()
        messagebox.showinfo("Success", "Patient added successfully!")
        clear_fields()
        view_patients()
       
    def view_patients():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM patients")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)

    def delete_patient():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient to delete.")
            return
        pid = tree.item(selected_item)['values'][0]
        cursor.execute("DELETE FROM patients WHERE id=?", (pid,))
        conn.commit()
        messagebox.showinfo("Deleted", "Patient record deleted.")
        view_patients()

    def update_patient():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient to update.")
            return
        pid = tree.item(selected_item)['values'][0]

        name = entry_name.get()
        age = entry_age.get()
        gender = var_gender.get()
        contact = entry_contact.get()
        address = entry_address.get()

        cursor.execute("""
            UPDATE patients
            SET name=?, age=?, gender=?, contact=?, address=?
            WHERE id=?
        """, (name, age, gender, contact, address, pid))
        conn.commit()
        messagebox.showinfo("Success", "Patient record updated!")
        clear_fields()
        view_patients()

    def search_patient():
        query = entry_search.get()
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM patients WHERE name LIKE ?", ('%' + query + '%',))
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)

    def clear_fields():
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        var_gender.set("")
        entry_contact.delete(0, tk.END)
        entry_address.delete(0, tk.END)

    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item)["values"]
            clear_fields()
            entry_name.insert(0, values[1])
            entry_age.insert(0, values[2])
            var_gender.set(values[3])
            entry_contact.insert(0, values[4])
            entry_address.insert(0, values[5])

    # Title
    tk.Label(root, text="Hospital Management System", font=("Arial", 24, "bold"), bg="#f0f8ff").pack(pady=20)

    # Search Bar
    search_frame = tk.Frame(root, bg="#f0f8ff")
    search_frame.pack(pady=10)
    tk.Label(search_frame, text="Search Patient:", font=("Arial", 12), bg="#f0f8ff").pack(side=tk.LEFT, padx=5)
    entry_search = tk.Entry(search_frame)
    entry_search.pack(side=tk.LEFT, padx=5)
    tk.Button(search_frame, text="Search", command=search_patient).pack(side=tk.LEFT, padx=5)
    tk.Button(search_frame, text="Show All", command=view_patients).pack(side=tk.LEFT, padx=5)

    # Entry Form
    form_frame = tk.Frame(root, bg="#f0f8ff")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Name:", bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(form_frame)
    entry_name.grid(row=0, column=1, padx=10)

    tk.Label(form_frame, text="Age:", bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=5)
    entry_age = tk.Entry(form_frame)
    entry_age.grid(row=1, column=1, padx=10)

    tk.Label(form_frame, text="Gender:", bg="#f0f8ff").grid(row=2, column=0, padx=10, pady=5)
    var_gender = tk.StringVar()
    combo_gender = ttk.Combobox(form_frame, textvariable=var_gender, values=["Male", "Female", "Other"])
    combo_gender.grid(row=2, column=1, padx=10)

    tk.Label(form_frame, text="Contact:", bg="#f0f8ff").grid(row=3, column=0, padx=10, pady=5)
    entry_contact = tk.Entry(form_frame)
    entry_contact.grid(row=3, column=1, padx=10)

    tk.Label(form_frame, text="Address:", bg="#f0f8ff").grid(row=4, column=0, padx=10, pady=5)
    entry_address = tk.Entry(form_frame)
    entry_address.grid(row=4, column=1, padx=10)

    # Button Frame
    button_frame = tk.Frame(root, bg="#f0f8ff")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add", command=add_patient, width=10).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Update", command=update_patient, width=10).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Delete", command=delete_patient, width=10).grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="Clear", command=clear_fields, width=10).grid(row=0, column=3, padx=5)

    # Treeview Table
    tree = ttk.Treeview(root, columns=("ID", "Name", "Age", "Gender", "Contact", "Address"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Gender", text="Gender")
    tree.heading("Contact", text="Contact")
    tree.heading("Address", text="Address")
    tree.pack(pady=20)

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    view_patients()

    root.mainloop()
