import tkinter as tk
from tkinter import messagebox

def submit_form():
    name = name_entry.get()
    email = email_entry.get()
    message = message_entry.get("1.0", tk.END).strip()
    
    if not name or not email or not message:
        messagebox.showwarning("Warning", "All fields are required!")
        return
    
    messagebox.showinfo("Success", f"Form submitted!\nName: {name}\nEmail: {email}\nMessage: {message}")
    
    # Clear fields after submission
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    message_entry.delete("1.0", tk.END)

# Create main window
root = tk.Tk()
root.title("Simple Form")
root.geometry("300x250")

# Labels and Entry fields
tk.Label(root, text="Name:").pack(pady=5)
name_entry = tk.Entry(root, width=30)
name_entry.pack()

tk.Label(root, text="Email:").pack(pady=5)
email_entry = tk.Entry(root, width=30)
email_entry.pack()

tk.Label(root, text="Message:").pack(pady=5)
message_entry = tk.Text(root, width=30, height=5)
message_entry.pack()

# Submit Button
submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.pack(pady=10)

# Run the application
root.mainloop()
