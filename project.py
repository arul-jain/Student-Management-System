import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database Connection Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'student_db'
}

def connect_to_db():
    # Establishes a connection to the MySQL database
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
        return None

# CRUD Operations
def add_student():
    # Adds a new student to the database from GUI inputs.
    name = name_entry.get()
    age = age_entry.get()
    major = major_entry.get()

    if not all([name, age, major]):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Input Error", "Age must be a number.")
        return

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO students (name, age, major) VALUES (%s, %s, %s)"
        values = (name, age, major)
        try:
            cursor.execute(sql, values)
            conn.commit()
            messagebox.showinfo("Success", f"Student '{name}' added successfully.")
            clear_entries()
            view_students()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error adding student: {err}")
        finally:
            cursor.close()
            conn.close()

def view_students():
    # Displays all students in the GUI
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM students"
        try:
            cursor.execute(sql)
            records = cursor.fetchall()
            students_list.delete(1.0, tk.END)
            students_list.insert(tk.END, "ID\tName\t\t\tAge\tMajor\n")
            students_list.insert(tk.END, "-" * 60 + "\n")
            for row in records:
                students_list.insert(tk.END, f"{row[0]}\t{row[1]}\t\t\t{row[2]}\t{row[3]}\n")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error viewing students: {err}")
        finally:
            cursor.close()
            conn.close()

def delete_student(student_id):
    # Deletes a student record from the database.
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM students WHERE id = %s"
        try:
            cursor.execute(sql, (student_id,))
            conn.commit()
            messagebox.showinfo("Success", f"Student with ID {student_id} deleted successfully.")
            view_students()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting student: {err}")
        finally:
            cursor.close()
            conn.close()

def on_delete_click():
    # Gets the ID from the input field and calls the delete function.
    try:
        student_id_to_delete = int(delete_id_entry.get())
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student with ID {student_id_to_delete}?"):
            delete_student(student_id_to_delete)
            delete_id_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid student ID.")

def clear_entries():
    # Clears the input fields in the GUI.
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    major_entry.delete(0, tk.END)

# GUI Setup using Tkinter
root = tk.Tk()
root.title("Student Management System")

# Create and place widgets
tk.Label(root, text="Student Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

tk.Label(root, text="Student Age:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

tk.Label(root, text="Student Major:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
major_entry = tk.Entry(root)
major_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

add_button = tk.Button(root, text="Add Student", command=add_student)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

tk.Label(root, text="Current Students:").grid(row=4, column=0, columnspan=2, pady=5)
students_list = tk.Text(root, height=10, width=60)
students_list.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

view_button = tk.Button(root, text="Refresh List", command=view_students)
view_button.grid(row=6, column=0, columnspan=2, pady=5)

tk.Label(root, text="Delete by ID:").grid(row=7, column=0, padx=5, pady=5, sticky='e')
delete_id_entry = tk.Entry(root)
delete_id_entry.grid(row=7, column=1, padx=5, pady=5, sticky='w')

delete_button = tk.Button(root, text="Delete Student", command=on_delete_click)
delete_button.grid(row=8, column=0, columnspan=2, pady=10)

# Initial data load
view_students()

# Start the GUI event loop
root.mainloop()