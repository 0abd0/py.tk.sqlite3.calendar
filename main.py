##pip install sqlite3
##pip install tkcalendar
##
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import csv
from datetime import datetime

# Database Setup
def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            category TEXT,
            priority TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

# Add Task to Database
def add_task():
    task = entry.get()
    category = selected_category.get()
    priority = selected_priority.get()
    task_deadline = deadline.get()
    if task:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task, category, priority, deadline, status) VALUES (?, ?, ?, ?, ?)',
                       (task, category, priority, task_deadline, 'pending'))
        conn.commit()
        conn.close()
        entry.delete(0, tk.END)
        show_tasks()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Show Tasks in the Listbox
def show_tasks():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY priority')
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        task_info = f"{row[1]} | Category: {row[2]} | Priority: {row[3]} | Deadline: {row[4]} | Status: {row[5]}"
        listbox.insert(tk.END, task_info)

# Delete Task from Database
def delete_task():
    try:
        selected_task = listbox.get(listbox.curselection())
        task_text = selected_task.split('|')[0].strip()
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE task = ?', (task_text,))
        conn.commit()
        conn.close()
        show_tasks()
    except tk.TclError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Mark Task as Completed or Pending
def toggle_status():
    try:
        selected_task = listbox.get(listbox.curselection())
        task_text = selected_task.split('|')[0].strip()
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('SELECT status FROM tasks WHERE task = ?', (task_text,))
        status = cursor.fetchone()[0]
        new_status = 'completed' if status == 'pending' else 'pending'
        cursor.execute('UPDATE tasks SET status = ? WHERE task = ?', (new_status, task_text))
        conn.commit()
        conn.close()
        show_tasks()
    except tk.TclError:
        messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")

# Search for a Task
def search_task():
    search_term = search_entry.get()
    listbox.delete(0, tk.END)
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE task LIKE ?', ('%' + search_term + '%',))
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        task_info = f"{row[1]} | Category: {row[2]} | Priority: {row[3]} | Deadline: {row[4]} | Status: {row[5]}"
        listbox.insert(tk.END, task_info)

# Toggle between Light and Dark Mode
def toggle_theme():
    if root['bg'] == 'white':
        root.config(bg='black')
        listbox.config(bg='black', fg='white')
    else:
        root.config(bg='white')
        listbox.config(bg='white', fg='black')

# Export Tasks to CSV File
def export_tasks():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()

    with open('tasks.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Task', 'Category', 'Priority', 'Deadline', 'Status'])
        for task in tasks:
            writer.writerow(task)
# Main Application GUI
def create_gui():
    global entry, listbox, selected_category, selected_priority, deadline, search_entry, root

    root = tk.Tk()
    root.title("Enhanced To-Do List")
    root.config(bg='white')

    # Entry box to input tasks
    entry = tk.Entry(root, width=40)
    entry.pack(pady=10)

    # Categories and Priorities
    categories = ["Work", "Personal", "Shopping", "Other"]
    priorities = ["High", "Medium", "Low"]

    selected_category = tk.StringVar()
    selected_category.set(categories[0])

    selected_priority = tk.StringVar()
    selected_priority.set(priorities[0])

    tk.Label(root, text="Category:").pack()
    category_menu = tk.OptionMenu(root, selected_category, *categories)
    category_menu.pack(pady=5)

    tk.Label(root, text="Priority:").pack()
    priority_menu = tk.OptionMenu(root, selected_priority, *priorities)
    priority_menu.pack(pady=5)

    # Task Deadline
    tk.Label(root, text="Deadline:").pack()
    deadline = DateEntry(root, width=30)
    deadline.pack(pady=5)

    # Add Task Button
    add_button = tk.Button(root, text="Add Task", width=40, command=add_task)
    add_button.pack(pady=5)

    # Search Bar
    search_entry = tk.Entry(root, width=40)
    search_entry.pack(pady=10)
    search_button = tk.Button(root, text="Search Task", width=40, command=search_task)
    search_button.pack(pady=5)

    # Listbox to display tasks
    listbox = tk.Listbox(root, width=80, height=10)
    listbox.pack(pady=10)

    # Task Buttons (Delete, Mark Complete, Export)
    delete_button = tk.Button(root, text="Delete Task", width=40, command=delete_task)
    delete_button.pack(pady=5)

    complete_button = tk.Button(root, text="Toggle Complete", width=40, command=toggle_status)
    complete_button.pack(pady=5)

    export_button = tk.Button(root, text="Export Tasks to CSV", width=40, command=export_tasks)
    export_button.pack(pady=5)

    # Dark Mode Toggle
    theme_button = tk.Button(root, text="Toggle Dark Mode", width=40, command=toggle_theme)
    theme_button.pack(pady=5)

    show_tasks()
    root.mainloop()

# Toggle between Light and Dark Mode
def toggle_theme():
    if root['bg'] == 'white':
        root.config(bg='black')
        listbox.config(bg='black', fg='white')
    else:
        root.config(bg='white')
        listbox.config(bg='white', fg='black')

if __name__ == "__main__":
    init_db()  # Initialize the database
    create_gui()  # Run the GUI application
