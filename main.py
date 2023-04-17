import mysql.connector
from dotenv import load_dotenv
from mysql.connector import errorcode
import tkinter as tk
from tkinter import messagebox, ttk
import os

load_dotenv()

# Load environment variables
USER = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
HOST = os.environ.get("HOST")
DATABASE = os.environ.get("DATABASE")
PORT = os.environ.get("PORT")

# Read schema.sql file
with open("schema.sql", "r") as f:
    schema = f.read()


# Establish a connection to the server
def connect_server():
    try:
        cnx = mysql.connector.connect(
            user=USER, password=PASSWORD, host=HOST
        )
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            messagebox.showerror("Error", "Access denied. Check your username and password.")
        else:
            messagebox.showerror("Error", str(err))
        return None


# Create the database if it doesn't exist
def create_database(cnx):
    cursor = cnx.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {DATABASE}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to create database: {err}")
        return False
    cursor.close()
    return True


# Establish a connection to the database
def connect_db():
    cnx = connect_server()
    if cnx:
        cursor = cnx.cursor()
        try:
            cnx.database = DATABASE
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                return None
            else:
                messagebox.showerror("Error", str(err))
                return None
        cursor.close()
    return cnx


# Create tables if they don't exist
def create_tables(cnx, schema, created_db):
    if not created_db:
        return True

    cursor = cnx.cursor()
    for statement in schema.split(";"):
        if statement.strip():
            try:
                cursor.execute(statement)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to create tables: {err}")
                return False
    cursor.close()
    return True


def get_all_records(table_name):
    cursor = cnx.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    cursor.close()
    return rows


# Create the tkinter UI and functions here
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


def add_record(table_name, columns, values):
    cursor = cnx.cursor()
    column_names = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    cursor.execute(query, values)
    cnx.commit()
    cursor.close()


def update_record(table_name, primary_key_column, primary_key_value, column, new_value):
    cursor = cnx.cursor()
    query = f"UPDATE {table_name} SET {column} = %s WHERE {primary_key_column} = %s"
    cursor.execute(query, (new_value, primary_key_value))
    cnx.commit()
    cursor.close()


def delete_record(table_name, primary_key_column, primary_key_value):
    cursor = cnx.cursor()
    query = f"DELETE FROM {table_name} WHERE {primary_key_column} = %s"
    cursor.execute(query, (primary_key_value,))
    cnx.commit()
    cursor.close()


def search_records(table_name, column, value):
    cursor = cnx.cursor()
    query = f"SELECT * FROM {table_name} WHERE {column} LIKE %s"
    cursor.execute(query, (f"%{value}%",))
    rows = cursor.fetchall()
    cursor.close()
    return rows


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


def refresh_tree(tree, table_name, column=None, search_query=None):
    tree.delete(*tree.get_children())
    if column and search_query:
        records = search_records(table_name, column, search_query)
    else:
        records = get_all_records(table_name)
    for row in records:
        tree.insert("", tk.END, values=row)


# Add buttons for the CRUD operations
def add_buttons(tab, tree, table_name, columns, primary_key_column):
    add_button = ttk.Button(tab, text="Add", command=lambda: show_add_dialog(table_name, columns, tree))
    add_button.pack(side=tk.LEFT, padx=10, pady=10)

    delete_button = ttk.Button(tab, text="Delete",
                               command=lambda: delete_record(table_name, primary_key_column, tree.selection()[0]))
    delete_button.pack(side=tk.LEFT, padx=10)

    modify_button = ttk.Button(tab, text="Modify",
                               command=lambda: show_modify_dialog(tab, table_name, primary_key_column, tree))
    modify_button.pack(side=tk.LEFT, padx=10)

    search_label = ttk.Label(tab, text="Search:")
    search_label.pack(side=tk.LEFT, padx=10)

    search_entry = ttk.Entry(tab)
    search_entry.pack(side=tk.LEFT, padx=10)

    search_button = ttk.Button(tab, text="Search",
                               command=lambda: refresh_tree(tree, table_name, columns[1], search_entry.get()))
    search_button.pack(side=tk.LEFT, padx=10)

    clear_search_button = ttk.Button(tab, text="Clear", command=lambda: refresh_tree(tree, table_name))
    clear_search_button.pack(side=tk.LEFT, padx=10)


def show_modify_dialog(parent, table_name, tree, fields, id_field):
    selected_item = tree.selection()[0]
    selected_data = tree.item(selected_item)["values"]
    record_id = selected_data[0]

    top = tk.Toplevel(parent)
    top.title(f"Modify {table_name.capitalize()} Record")

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


def check_database_exists(cnx, database_name):
    cursor = cnx.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [row[0] for row in cursor.fetchall()]
    cursor.close()

    return database_name in databases


if __name__ == "__main__":
    # Connect to the database and create tables
    cnx = connect_db()
    created_db = False
    if cnx:
        if not check_database_exists(cnx, DATABASE):
            created_db = create_database(cnx)
        if create_tables(cnx, schema, created_db):
            main_window()
        cnx.close()
