import os
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTabWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QPushButton
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
import mysql.connector
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTabWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QHeaderView
from PyQt5.uic.properties import QtCore
from dotenv import load_dotenv
from mysql.connector import errorcode

load_dotenv()

# Load environment variables
USERNAME = os.environ.get("DB_USER", "root")
PASSWORD = os.environ.get("PASSWORD")
HOST = os.environ.get("HOST", "localhost")
DATABASE = os.environ.get("DATABASE")
PORT = os.environ.get("PORT", "3306")


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
            print("Error: Access denied. Check your username and password.")
        else:
            print(f"Error: {err}")
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
                print(f"Error: {err}")
                return None
        curr.close()
    return conn


class AutoRepairDatabase(QMainWindow):
    def __init__(self, conn, *args, **kwargs):
        super(AutoRepairDatabase, self).__init__(*args, **kwargs)
        self.setWindowTitle("Auto Repair Shop Database")
        self.conn = conn
        self.initUI()

    def initUI(self):
        tab_widget = QTabWidget()
        tab_widget.addTab(OwnersTab(self.conn), "Owners")
        tab_widget.addTab(CarsTab(self.conn), "Cars")
        tab_widget.addTab(EmployeesTab(self.conn), "Employees")
        tab_widget.addTab(ServicesTab(self.conn), "Services")
        tab_widget.addTab(RepairsTab(self.conn), "Repairs")

        vbox = QVBoxLayout()
        vbox.addWidget(tab_widget)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)


class BaseTab(QWidget):
    def __init__(self, conn, *args, **kwargs):
        super(BaseTab, self).__init__(*args, **kwargs)
        self.conn = conn
        self.initUI()

    def initUI(self):
        self.table = QTableWidget()
        self.layout = QVBoxLayout()

        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.modify_button = QPushButton("Modify")
        self.delete_button = QPushButton("Delete")

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.modify_button)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addWidget(self.table)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        self.refresh_table()

    def refresh_table(self):
        raise NotImplementedError("Must be implemented in a subclass")

    def get_all_records(self, table_name):
        curr = self.conn.cursor()
        curr.execute(f"SELECT * FROM {table_name}")
        rows = curr.fetchall()
        curr.close()
        return rows

    def set_table_data(self, data):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))

        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                item = QTableWidgetItem(str(cell))
                item.setForeground(Qt.white)
                self.table.setItem(i, j, item)

            self.table.setAlternatingRowColors(True)
            self.table.setStyleSheet("alternate-background-color: #393939; background-color: #313131;")

class OwnersTab(BaseTab):
    def __init__(self, conn, *args, **kwargs):
        super(OwnersTab, self).__init__(conn, *args, **kwargs)

    def initUI(self):
        super(OwnersTab, self).initUI()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Owner ID", "First Name", "Last Name", "Phone", "Email"])

    def refresh_table(self):
        records = self.get_all_records("owner")
        self.set_table_data(records)

class CarsTab(BaseTab):
    def __init__(self, conn, *args, **kwargs):
        super(CarsTab, self).__init__(conn, *args, **kwargs)

    def initUI(self):
        super(CarsTab, self).initUI()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Car ID", "Make", "Model", "Year", "Owner ID"])

    def refresh_table(self):
        records = self.get_all_records("car")
        self.set_table_data(records)

class EmployeesTab(BaseTab):
    def __init__(self, conn, *args, **kwargs):
        super(EmployeesTab, self).__init__(conn, *args, **kwargs)

    def initUI(self):
        super(EmployeesTab, self).initUI()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Employee ID", "First Name", "Last Name", "Hire Date"])

    def refresh_table(self):
        records = self.get_all_records("employee")
        self.set_table_data(records)

class ServicesTab(BaseTab):
    def __init__(self, conn, *args, **kwargs):
        super(ServicesTab, self).__init__(conn, *args, **kwargs)

    def initUI(self):
        super(ServicesTab, self).initUI()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Service ID", "Service Name", "Service Description"])

    def refresh_table(self):
        records = self.get_all_records("service")
        self.set_table_data(records)

class RepairsTab(BaseTab):
    def __init__(self, conn, *args, **kwargs):
        super(RepairsTab, self).__init__(conn, *args, **kwargs)

    def initUI(self):
        super(RepairsTab, self).initUI()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Repair ID", "Car ID", "Service ID", "Employee ID", "Repair Date"])

    def refresh_table(self):
        records = self.get_all_records("repair")
        self.set_table_data(records)

if __name__ == "__main__":
    conn = connect_db()
    if conn:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        dark_palette = app.palette()
        dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.WindowText, Qt.white)
        dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
        dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QtGui.QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QtGui.QPalette.Text, Qt.white)
        dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        dark_palette.setColor(QtGui.QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QtGui.QPalette.BrightText, Qt.red)
        dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
        dark_palette.setColor(QtGui.QPalette.HighlightedText, Qt.black)

        app.setPalette(dark_palette)
        app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

        main_window = AutoRepairDatabase(conn)
        main_window.show()
        sys.exit(app.exec_())
        conn.close()
