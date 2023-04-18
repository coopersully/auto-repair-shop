# Auto Repair Shop Database

This project is a simple desktop application to manage an auto repair shop's database. The application is built using Python, Tkinter, and MySQL. Users can perform CRUD operations on different tables, such as owners, cars, employees, services, and repairs.

## Environment Variables

The application requires the following environment variables:

- `DB_USER`: MySQL username
- `PASSWORD`: MySQL password
- `HOST`: MySQL server host (e.g., localhost or an IP address)
- `DATABASE`: The name of the MySQL database to be used
- `PORT`: MySQL server port

These variables should be placed in a `.env` file in the project's root directory.

## Installation

1. Ensure you have Python 3.7 or higher installed. You can check your Python version by running `python --version` in your terminal or command prompt.

2. Install the required Python packages:

```bash
pip install mysql-connector-python python-dotenv sqlparse
```

3. Clone the repository:
```bash
git clone https://github.com/yourusername/auto-repair-shop.git
cd auto-repair-shop
```

4. Create a .env file in the project's root directory and set the required environment variables (see the "Environment Variables" section above).

5. Run the main.py script to start the application:
```bash
python main.py
```
The GUI should now appear, and you can use it to interact with the auto repair shop database.

## Usage
The application's main window contains several tabs representing different tables in the database. To perform CRUD operations on a table, select the corresponding tab and use the "Add", "Delete", and "Modify" buttons.

When adding or modifying a record, a dialog window will appear with fields for entering the necessary data. Fill in the fields and click "Submit" to save the changes.
