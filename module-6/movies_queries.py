# Author: Nicholas Zankl
# Date: September 13, 2026
# Assignment: CSD-310 Module 6.2 Assignment - Movies: Table Queries
# Purpose: Connects to the MySQL 'movies' database to execute and display 
# four table queries retrieving studios, genres, short films, and films grouped by director.

import mysql.connector
from mysql.connector import errorcode

# MySQL database connection configuration
db_config = {
    'user': 'root',
    'password': '!Dfs033108061078',
    'host': '127.0.0.1',
    'database': 'movies'
}

def execute_movie_queries():
    """Connects to the database and executes all four assignment queries."""
    try:
        # Establish connection to the database and initialize the cursor
        db_connection = mysql.connector.connect(**db_config)
        db_cursor = db_connection.cursor()
        print("Successfully connected to the 'movies' database.\n")
        print("=" * 60)

        # ---------------------------------------------------------------------
        # Query 1: Select all fields from the studio table
        # ---------------------------------------------------------------------
        print("-- DISPLAYING STUDIO RECORDS --")
        select_studios_query = "SELECT studio_id, studio_name FROM studio;"
        db_cursor.execute(select_studios_query)
        studio_records = db_cursor.fetchall()
        
        for studio_row in studio_records:
            print(f"Studio ID: {studio_row[0]} | Studio Name: {studio_row[1]}")
        print("=" * 60 + "\n")

        # ---------------------------------------------------------------------
        # Query 2: Select all fields from the genre table
        # ---------------------------------------------------------------------
        print("-- DISPLAYING GENRE RECORDS --")
        select_genres_query = "SELECT genre_id, genre_name FROM genre;"
        db_cursor.execute(select_genres_query)
        genre_records = db_cursor.fetchall()
        
        for genre_row in genre_records:
            print(f"Genre ID: {genre_row[0]} | Genre Name: {genre_row[1]}")
        print("=" * 60 + "\n")

        # ---------------------------------------------------------------------
        # Query 3: Select movie names with runtime less than 2 hours (120 min)
        # ---------------------------------------------------------------------
        print("-- DISPLAYING MOVIES WITH RUNTIME < 2 HOURS (120 MIN) --")
        select_short_films_query = "SELECT film_name, film_runtime FROM film WHERE film_runtime < 120;"
        db_cursor.execute(select_short_films_query)
        short_film_records = db_cursor.fetchall()
        
        for film_row in short_film_records:
            print(f"Film Name: {film_row[0]} | Runtime: {film_row[1]} mins")
        print("=" * 60 + "\n")

        # ---------------------------------------------------------------------
        # Query 4: List film names and directors grouped by director
        # ---------------------------------------------------------------------
        print("-- DISPLAYING FILMS AND DIRECTORS GROUPED BY DIRECTOR --")
        select_films_by_director_query = "SELECT film_director, film_name FROM film ORDER BY film_director;"
        db_cursor.execute(select_films_by_director_query)
        director_film_records = db_cursor.fetchall()

        for film_row in director_film_records:
            print(f"Director: {film_row[0]:<25} | Film: {film_row[1]}")
        print("=" * 60 + "\n")

    except mysql.connector.Error as err:
        # Handle specific MySQL database and authentication errors
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Invalid username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print(f"Database Error: {err}")
    finally:
        # Safely close the database cursor and connection upon completion
        if 'db_connection' in locals() and db_connection.is_connected():
            db_cursor.close()
            db_connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    execute_movie_queries()
