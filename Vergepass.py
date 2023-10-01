from tkinter import *
import tkinter as tk
from tkinter import Tk, Label, Entry, Button, LabelFrame
import tkinter.messagebox as messagebox
import hashlib

# Function to handle user registration
def register():
    username = reg_username_entry.get()
    password = reg_password_entry.get()

    if username and password:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        record = f"{username}|{hashed_password}\n"
        try:
            with open("passwords.txt", "a") as file:
                file.write(record)
            messagebox.showinfo("Success", "Registration successful. You can now log in.")
            clear_registration_entries()
        except IOError:
            messagebox.showerror("Error", "Failed to write to file.")
    else:
        messagebox.showwarning("Warning", "Please fill in all the fields.")

# Function to handle user login
def login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if username and password:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            with open("passwords.txt", "r") as file:
                users = file.readlines()

            for user in users:
                stored_username, stored_password = user.strip().split("|")
                if username == stored_username and hashed_password == stored_password:
                    messagebox.showinfo("Login Successful", "Welcome, " + username)
                    enable_password_manager()
                    return

            messagebox.showerror("Login Failed", "Invalid username or password.")
        except IOError:
            messagebox.showerror("Error", "Failed to read from file.")
    else:
        messagebox.showwarning("Warning", "Please fill in all the fields.")

# Function to enable password manager features
def enable_password_manager():
    register_frame.pack_forget()
    login_frame.pack_forget()
    password_manager_frame.pack()

# Function to handle password storage
def store_password():
    website = website_entry.get()
    password = password_entry.get()

    if website and password:
        record = f"{website}|{password}\n"
        try:
            with open("passwords.txt", "a") as file:
                file.write(record)
            messagebox.showinfo("Success", "Password stored successfully.")
            clear_password_entries()
        except IOError:
            messagebox.showerror("Error", "Failed to write to file.")
    else:
        messagebox.showwarning("Warning", "Please fill in all the fields.")

# Function to search for a password
def search_password():
    website = website_entry.get()

    if website:
        try:
            with open("passwords.txt", "r") as file:
                passwords = file.readlines()

            for line in passwords:
                stored_website, stored_password = line.strip().split("|")
                if website == stored_website:
                    messagebox.showinfo("Password Found", f"Website: {stored_website}\nPassword: {stored_password}")
                    clear_password_entries()
                    return

            messagebox.showerror("Password Not Found", "No password found for the given website.")
        except IOError:
            messagebox.showerror("Error", "Failed to read from file.")
    else:
        messagebox.showwarning("Warning", "Please enter a website name.")

# Function to delete a password
def delete_password():
    website = website_entry.get()

    if website:
        try:
            with open("passwords.txt", "r") as file:
                passwords = file.readlines()

            with open("passwords.txt", "w") as file:
                for line in passwords:
                    stored_website, _ = line.strip().split("|")
                    if website != stored_website:
                        file.write(line)

            messagebox.showinfo("Success", "Password deleted successfully.")
            clear_password_entries()
        except IOError:
            messagebox.showerror("Error", "Failed to write to file.")
    else:
        messagebox.showwarning("Warning", "Please enter a website name.")

# Function to edit a password
def edit_password():
    website = website_entry.get()
    new_password = password_entry.get()

    if website and new_password:
        try:
            with open("passwords.txt", "r") as file:
                passwords = file.readlines()

            with open("passwords.txt", "w") as file:
                for line in passwords:
                    stored_website, _ = line.strip().split("|")
                    if website == stored_website:
                        line = f"{website}|{new_password}\n"
                    file.write(line)

            messagebox.showinfo("Success", "Password updated successfully.")
            clear_password_entries()
        except IOError:
            messagebox.showerror("Error", "Failed to write to file.")
    else:
        messagebox.showwarning("Warning", "Please fill in all the fields.")

# Function to display all passwords
def display_passwords():
    try:
        with open("passwords.txt", "r") as file:
            passwords = file.readlines()

        if passwords:
            messagebox.showinfo("All Passwords", "Website\tPassword\n" + "-"*30 + "\n" + "".join(passwords))
        else:
            messagebox.showinfo("No Passwords", "No passwords saved.")
    except IOError:
        messagebox.showerror("Error", "Failed to read from file.")

# Function to clear registration entries
def clear_registration_entries():
    reg_username_entry.delete(0, END)
    reg_password_entry.delete(0, END)

# Function to clear login entries
def clear_login_entries():
    login_username_entry.delete(0, END)
    login_password_entry.delete(0, END)

# Function to clear password manager entries
def clear_password_entries():
    website_entry.delete(0, END)
    password_entry.delete(0, END)

# Create the main window
root = Tk()
root.configure(bg='#E0C097')
root.title("Access to all passwords in one place")

# Set window size and position
window_width = 850
window_height = 590
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create and place widgets for user registration
register_frame = LabelFrame(root, text="User Registration", padx=58, pady=30, bg='#E0C097', fg='black', bd=0)
register_frame.pack(pady=48)
register_frame.config(highlightthickness=0, borderwidth=7, highlightbackground='#E0C097')

reg_username_label = Label(register_frame, text="Username:", bg='#E0C097', fg='black')
reg_username_label.grid(row=0, column=0, sticky='e')

reg_username_entry = Entry(register_frame)
reg_username_entry.grid(row=0, column=1)

reg_password_label = Label(register_frame, text="Password:", bg='#E0C097', fg='black')
reg_password_label.grid(row=1, column=0, sticky='e')

reg_password_entry = Entry(register_frame, show="*")
reg_password_entry.grid(row=1, column=1)

register_button = Button(register_frame, text="Register", command=register, bg='#B85C38', fg='white', relief='raised', bd=0)
register_button.grid(row=2, column=1, pady=8)
register_button.config(width=10, height=1, highlightthickness=0, borderwidth=0, highlightbackground='#E0C097')

# Create and place widgets for user login
login_frame = LabelFrame(root, text="User Login", padx=58, pady=30, bg='#E0C097', fg='black', bd=0)
login_frame.pack(pady=20)
login_frame.config(highlightthickness=0, borderwidth=7, highlightbackground='#E0C097')

login_username_label = Label(login_frame, text="Username:", bg='#E0C097', fg='black')
login_username_label.grid(row=0, column=0, sticky='e')

login_username_entry = Entry(login_frame)
login_username_entry.grid(row=0, column=1)

login_password_label = Label(login_frame, text="Password:", bg='#E0C097', fg='black')
login_password_label.grid(row=1, column=0, sticky='e')

login_password_entry = Entry(login_frame, show="*")
login_password_entry.grid(row=1, column=1)

login_button = Button(login_frame, text="Login", command=login, bg='#B85C38', fg='white', relief='raised', bd=0)
login_button.grid(row=2, column=1, pady=8)
login_button.config(width=10, height=1, highlightthickness=0, borderwidth=0, highlightbackground='#E0C097')

# Create and place widgets for password management
password_manager_frame = LabelFrame(root, text="Password Manager", padx=79, pady=54, bg='#E0C097', fg='black', bd=0)
password_manager_frame.pack(pady=130)
password_manager_frame.config(highlightthickness=0, borderwidth=7, highlightbackground='#E0C097')

website_label = Label(password_manager_frame, text="Website:", bg='#E0C097', fg='black')
website_label.grid(row=0, column=0, sticky='e')

website_entry = Entry(password_manager_frame)
website_entry.grid(row=0, column=1)

password_label = Label(password_manager_frame, text="Password:", bg='#E0C097', fg='black')
password_label.grid(row=1, column=0, sticky='e')

password_entry = Entry(password_manager_frame, show="*")
password_entry.grid(row=1, column=1)

store_button = Button(password_manager_frame, text="Store Password", command=store_password, bg='#B85C38', fg='white', relief='raised', bd=0)
store_button.grid(row=2, column=0, pady=18)
store_button.config(width=15, height=1, highlightthickness=0, borderwidth=0, highlightbackground='#E0C097')

search_button = Button(password_manager_frame, text="Search Password", command=search_password, bg='#B85C38', fg='white', relief='raised', bd=0)
search_button.grid(row=2, column=1, pady=18)
search_button.config(width=15, height=1, highlightthickness=0, borderwidth=0, highlightbackground='#E0C097')

delete_button = Button(password_manager_frame, text="Delete Password", command=delete_password, bg='#B85C38', fg='white', relief='raised', bd=0)
delete_button.grid(row=2, column=2, pady=18)
delete_button.config(width=15, height=1, highlightthickness=0, borderwidth=0, highlightbackground='#E0C097')

edit_button = Button(password_manager_frame, text="Edit Password", command=edit_password, bg='#B85C38', fg='white', relief='raised', bd=0)
edit_button.grid(row=3, column=0, pady=8)
edit_button.config(width=15, height=1, highlightthickness=0, borderwidth=0, highlightbackground='#E0C097')

display_button = Button(password_manager_frame, text="View All Passwords", command=display_passwords, bg='#B85C38', fg='white', relief='raised', bd=0)
display_button.grid(row=3, column=1, pady=8, padx=20)
display_button.config(width=18, height=1, highlightthickness=0, borderwidth=0, highlightbackground='#E0C097')

# Run the main event loop
root.mainloop()
