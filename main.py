import os
import tkinter as tk
from tkinter import messagebox, ttk

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import errorcode

load_dotenv()

# Load environment variables
USERNAME = os.environ.get("DB_USER")
PASSWORD = os.environ.get("PASSWORD")
HOST = os.environ.get("HOST")
DATABASE = os.environ.get("DATABASE")
PORT = os.environ.get("PORT")


# Establish a connection to the MySQL server
def connect_server():
    try:
        print(f'Logging in as user "{USERNAME}" with password "{PASSWORD}"...')
        conn = mysql.connector.connect(
            user=USERNAME, password=PASSWORD, host=HOST
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            messagebox.showerror("Error", "Access denied. Check your username and password.")
        else:
            messagebox.showerror("Error", str(err))
        return None


# Establish a connection to the database
def connect_db():
    conn = connect_server()
    if conn:
        curr = conn.cursor()
        try:
            conn.database = DATABASE
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                return None
            else:
                messagebox.showerror("Error", str(err))
                return None
        curr.close()
    return conn


# Get all entries in a given table
def get_all_records(table_name):
    curr = conn.cursor()
    curr.execute(f"SELECT * FROM {table_name}")
    rows = curr.fetchall()
    curr.close()
    return rows


# Create interface main window, views, and buttons
def main_window():
    root = tk.Tk()
    root.title("Auto Repair Shop Database")

    # Create a tabbed interface for each table
    tab_control = ttk.Notebook(root)

    # Owners tab
    owner_tab = ttk.Frame(tab_control)
    tab_control.add(owner_tab, text="Owners")

    owner_tree = ttk.Treeview(owner_tab, columns=("owner_id", "first_name", "last_name", "phone", "email"),
                              show="headings")
    owner_tree.heading("owner_id", text="Owner ID")
    owner_tree.heading("first_name", text="First Name")
    owner_tree.heading("last_name", text="Last Name")
    owner_tree.heading("phone", text="Phone")
    owner_tree.heading("email", text="Email")
    owner_tree.pack(fill=tk.BOTH, expand=True)
    add_buttons(owner_tab, owner_tree, "owner", ["first_name", "last_name", "phone", "email"], "owner_id")
    refresh_tree(owner_tree, "owner")

    # Cars tab
    car_tab = ttk.Frame(tab_control)
    tab_control.add(car_tab, text="Cars")

    car_tree = ttk.Treeview(car_tab, columns=("car_id", "make", "model", "year", "owner_id"), show="headings")
    car_tree.heading("car_id", text="Car ID")
    car_tree.heading("make", text="Make")
    car_tree.heading("model", text="Model")
    car_tree.heading("year", text="Year")
    car_tree.heading("owner_id", text="Owner ID")
    car_tree.pack(fill=tk.BOTH, expand=True)
    add_buttons(car_tab, car_tree, "car", ["make", "model", "year", "owner_id"], "car_id")
    refresh_tree(car_tree, "car")

    # Employees tab
    employee_tab = ttk.Frame(tab_control)
    tab_control.add(employee_tab, text="Employees")

    employee_tree = ttk.Treeview(employee_tab, columns=("employee_id", "first_name", "last_name", "hire_date"),
                                 show="headings")
    employee_tree.heading("employee_id", text="Employee ID")
    employee_tree.heading("first_name", text="First Name")
    employee_tree.heading("last_name", text="Last Name")
    employee_tree.heading("hire_date", text="Hire Date")
    employee_tree.pack(fill=tk.BOTH, expand=True)
    add_buttons(employee_tab, employee_tree, "employee", ["first_name", "last_name", "hire_date"], "employee_id")
    refresh_tree(employee_tree, "employee")

    # Services tab
    service_tab = ttk.Frame(tab_control)
    tab_control.add(service_tab, text="Services")

    service_tree = ttk.Treeview(service_tab, columns=("service_id", "service_name", "service_description"),
                                show="headings")
    service_tree.heading("service_id", text="Service ID")
    service_tree.heading("service_name", text="Service Name")
    service_tree.heading("service_description", text="Service Description")
    service_tree.pack(fill=tk.BOTH, expand=True)
    add_buttons(service_tab, service_tree, "service", ["description", "cost", "car_id", "employee_id"], "service_id")
    refresh_tree(service_tree, "service")

    # Repairs tab
    repair_tab = ttk.Frame(tab_control)
    tab_control.add(repair_tab, text="Repairs")

    repair_tree = ttk.Treeview(repair_tab, columns=("repair_id", "car_id", "service_id", "employee_id", "repair_date"),
                               show="headings")
    repair_tree.heading("repair_id", text="Repair ID")
    repair_tree.heading("car_id", text="Car ID")
    repair_tree.heading("service_id", text="Service ID")
    repair_tree.heading("employee_id", text="Employee ID")
    repair_tree.heading("repair_date", text="Repair Date")
    repair_tree.pack(fill=tk.BOTH, expand=True)

    refresh_tree(repair_tree, "repair")

    tab_control.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


# Take fields from the add pop-up dialog and create a new entry
def add_record(table_name, columns, values):
    curr = conn.cursor()
    column_names = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    curr.execute(query, values)
    conn.commit()
    curr.close()


# Take fields from the modify pop-up dialog and update the given entry
def update_record(table_name, id_field, record_id, update_fields):
    set_clause = ', '.join([f"{field} = %s" for field in update_fields])
    query = f"UPDATE {table_name} SET {set_clause} WHERE {id_field} = %s"

    curr = conn.cursor()
    curr.execute(query, list(update_fields.values()) + [record_id])
    conn.commit()


# Delete the selected entry
def delete_record(table_name, primary_key_column, primary_key_value, tree):
    query = f"DELETE FROM {table_name} WHERE {primary_key_column} = %s"
    try:
        curr = conn.cursor()
        curr.execute(query, (primary_key_value,))
        conn.commit()
        refresh_tree(tree, table_name)
    except mysql.connector.errors.IntegrityError as e:
        if e.errno == 1451:
            messagebox.showerror("Error",
                                 "Cannot delete this record because it has related records in another table. Please delete related records first.")
        else:
            messagebox.showerror("Error", f"An error occurred while deleting the record: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while deleting the record: {e}")


# Pop-up dialog for adding a new entry
def show_add_dialog(table_name, columns, tree):
    def submit():
        values = [entry.get() for entry in entries]
        add_record(table_name, columns, values)
        refresh_tree(tree, table_name)
        dialog.destroy()

    dialog = tk.Toplevel()
    dialog.title(f"Add {table_name.capitalize()} Record")
    entries = []
    for i, column in enumerate(columns):
        label = ttk.Label(dialog, text=column.capitalize())
        label.grid(row=i, column=0, padx=10, pady=10)
        entry = ttk.Entry(dialog)
        entry.grid(row=i, column=1, padx=10, pady=10)
        entries.append(entry)
    submit_button = ttk.Button(dialog, text="Submit", command=submit)
    submit_button.grid(row=len(columns), columnspan=2, pady=10)


# Update data in the current tree view
def refresh_tree(tree, table_name):
    tree.delete(*tree.get_children())
    records = get_all_records(table_name)
    for row in records:
        tree.insert("", tk.END, values=row)


# Add buttons for the CRUD operations
def add_buttons(tab, tree, table_name, columns, primary_key_column):
    add_button = ttk.Button(tab, text="Add", command=lambda: show_add_dialog(table_name, columns, tree))
    add_button.pack(side=tk.LEFT, padx=10, pady=10)

    delete_button = ttk.Button(tab, text="Delete",
                               command=lambda: delete_record(table_name, primary_key_column,
                                                             tree.item(tree.selection()[0])['values'][0], tree))
    delete_button.pack(side=tk.LEFT, padx=10)

    modify_button = ttk.Button(tab, text="Modify",
                               command=lambda: show_modify_dialog(tab, table_name, primary_key_column,
                                                                  tree.item(tree.selection()[0])['values'][0], tree))
    modify_button.pack(side=tk.LEFT, padx=10)


# Pop-up dialog for editing the selected entry
def show_modify_dialog(parent, table_name, primary_key_column, id_field, tree):
    selected_item = tree.selection()[0]
    selected_data = tree.item(selected_item)["values"]
    record_id = selected_data[0]

    top = tk.Toplevel(parent)
    top.title(f"Modify {table_name.capitalize()} Record")

    curr = conn.cursor()
    curr.execute(f"DESCRIBE {table_name}")
    column_data = curr.fetchall()
    fields = [column[0] for column in column_data if column[0] != primary_key_column]

    labels = []
    entries = []

    for i, field in enumerate(fields):
        label = ttk.Label(top, text=f"{field.capitalize()}:")
        label.grid(row=i, column=0, sticky=tk.W, padx=(10, 5), pady=(10, 0))

        entry = ttk.Entry(top)
        entry.insert(0, selected_data[i + 1])
        entry.grid(row=i, column=1, sticky=tk.E, padx=(5, 10), pady=(10, 0))

        labels.append(label)
        entries.append(entry)

    def modify_record():
        update_fields = {field: entry.get() for field, entry in zip(fields, entries)}
        update_record(table_name, id_field, record_id, update_fields)
        refresh_tree(tree, table_name)
        top.destroy()

    modify_button = ttk.Button(top, text="Modify", command=modify_record)
    modify_button.grid(row=len(fields), column=0, columnspan=2, pady=(10, 10))

    top.mainloop()


if __name__ == "__main__":
    conn = connect_db()
    if conn:
        main_window()
        conn.close()
