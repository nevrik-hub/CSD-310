"""
Assignment: Module 5.2 - Movies: Setup
File: mysql_test.py
Description: Tests database connection to MySQL using python-dotenv credentials.
"""

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# Load configuration secrets from .env
secrets = dotenv_values(".env")

# Database configuration dictionary
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

db = None

try:
    # Connect to the movies database
    db = mysql.connector.connect(**config)
    
    # Print connection status confirmation
    print(f"\n  Database user {config['user']} connected to MySQL on host {config['host']} with database {config['database']}")
 
    input("\n\n  Press any key to continue...")

except mysql.connector.Error as err:
    # Error handling for common connection issues
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    # Safely close connection if active
    if db is not None and db.is_connected():
        db.close()
