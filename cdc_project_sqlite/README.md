
Trigger-Based CDC Project (SQLite → Snowflake)

This project captures INSERT, UPDATE, and DELETE operations in an SQLite database using triggers, extracts changes using Python, and loads them into Snowflake.



1) Project Folder Structure

cdc_project_sqlite/
│── cdc_sqlite_setup.sql    # SQL script to set up SQLite tables and triggers
│── config.py               # Database credentials
│── extract_cdc.py          # Python script to extract CDC data from SQLite
│── load_to_snowflake.py    # Python script to load CDC data into Snowflake
│── main.py                 # Orchestrates extraction & loading
│── requirements.txt        # Dependencies
│── README.md               # Project documentation



2) Install Dependencies

Run this command in your project directory:

    pip install snowflake-connector-python python-dotenv

Create a requirements.txt file:

    snowflake-connector-python
    python-dotenv



 3) Set Up SQLite Database & Triggers

 Create a file cdc_sqlite_setup.sql:

 -- Create main table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create CDC table to store changes
CREATE TABLE user_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation TEXT,
    changed_data TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for INSERT
CREATE TRIGGER user_insert_trigger
AFTER INSERT ON users
BEGIN
    INSERT INTO user_changes (operation, changed_data)
    VALUES ('INSERT', json_object('id', NEW.id, 'name', NEW.name, 'email', NEW.email));
END;

-- Trigger for UPDATE
CREATE TRIGGER user_update_trigger
AFTER UPDATE ON users
BEGIN
    INSERT INTO user_changes (operation, changed_data)
    VALUES ('UPDATE', json_object('id', NEW.id, 'name', NEW.name, 'email', NEW.email));
END;

-- Trigger for DELETE
CREATE TRIGGER user_delete_trigger
AFTER DELETE ON users
BEGIN
    INSERT INTO user_changes (operation, changed_data)
    VALUES ('DELETE', json_object('id', OLD.id, 'name', OLD.name, 'email', OLD.email));
END;


Run this in SQLite:
    sqlite3 cdc_database.db < cdc_sqlite_setup.sql



4) Store Database Credentials in config.py
Create config.py:

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

SQLITE_DB_PATH = "cdc_database.db"  # SQLite Database File

SNOWFLAKE_CONFIG = {
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),
}

Create a .env file to store credentials:

SNOWFLAKE_USER=your_snowflake_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=YOUR_DB
SNOWFLAKE_SCHEMA=PUBLIC


5) Extract CDC Data from SQLite
Create extract_cdc.py:

import sqlite3
from config import SQLITE_DB_PATH

def extract_cdc_data():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, operation, changed_data, changed_at FROM user_changes ORDER BY id ASC")
    changes = cursor.fetchall()

    cursor.close()
    conn.close()

    return [{"id": c[0], "operation": c[1], "changed_data": c[2], "changed_at": c[3]} for c in changes]



6) Load Data into Snowflake
Create load_to_snowflake.py:

import snowflake.connector
from config import SNOWFLAKE_CONFIG

def load_to_snowflake(changes):
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    cursor = conn.cursor()

    for change in changes:
        cursor.execute("""
            INSERT INTO user_changes_snowflake (operation, changed_data, changed_at)
            VALUES (%s, %s, %s)
        """, (change['operation'], change['changed_data'], change['changed_at']))

    conn.commit()
    cursor.close()
    conn.close()



7) Orchestrate Extraction & Loading
Create main.py:

from extract_cdc import extract_cdc_data
from load_to_snowflake import load_to_snowflake

def run_cdc_pipeline():
    print("Extracting CDC data from SQLite...")
    changes = extract_cdc_data()
    
    if changes:
        print(f"Found {len(changes)} changes. Loading into Snowflake...")
        load_to_snowflake(changes)
        print("CDC Data loaded successfully!")
    else:
        print("No new changes detected.")

if __name__ == "__main__":
    run_cdc_pipeline()



8) Run the CDC Pipeline
    python main.py



9) Expected Output:

Extracting CDC data from SQLite...
Found 3 changes. Loading into Snowflake...
CDC Data loaded successfully!




