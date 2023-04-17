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
            cursor.execute(f"USE {DATABASE}")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                if create_database(cnx):
                    cursor.execute(f"USE {DATABASE}")
                else:
                    messagebox.showerror("Error", "Failed to create and connect to the database.")
                    return None
            else:
                messagebox.showerror("Error", str(err))
                return None
        cursor.close()
    return cnx


# Create tables if they don't exist
def create_tables(cnx, schema):
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


def refresh_tree(tree, table_name):
    tree.delete(*tree.get_children())
    records = get_all_records(table_name)
    for row in records:
        tree.insert("", tk.END, values=row)


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


# Connect to the database and create tables
cnx = connect_db()
if cnx:
    if create_tables(cnx, schema):
        main_window()
    cnx.close()
