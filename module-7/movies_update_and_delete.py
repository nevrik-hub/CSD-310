# Name: Nicholas Zankl
# Date: August 16, 2026
# Assignment: CSD-310 Module 7.2 Assignment - Movies: Update & Deletes
# Purpose: Connects to a MySQL database to execute SELECT, INSERT, UPDATE, and DELETE operations 
# on movie records while displaying formatted results.

import mysql.connector
from mysql.connector import errorcode

# Database configuration dictionary
config = {
    'user': 'root',                    # Replace with your MySQL username
    'password': '!Dfs033108061078',    # Use MySQL password 
    'host': '127.0.0.1',
    'database': 'movies'
}

def show_films(cursor, title):
    """
    Executes a SELECT query with INNER JOINs to display film details
    along with their genre and studio names.
    """
    print(f"\n-- {title} --")
    print("=" * 75)
    
    query = """
        SELECT 
            film.film_name AS Name,
            film.film_director AS Director,
            genre.genre_name AS Genre,
            studio.studio_name AS Studio
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id;
    """
    
    cursor.execute(query)
    records = cursor.fetchall()
    
    for row in records:
        print(f"Film: {row[0]:<25} | Director: {row[1]:<20} | Genre: {row[2]:<12} | Studio: {row[3]}")
    
    print("=" * 75)


def main():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        
        # 1. Initial display of records
        show_films(cursor, "DISPLAYING FILMS")
        
        # 2. INSERT a new film including 'film_runtime' (e.g. 148 mins)
        insert_query = """
            INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, genre_id, studio_id)
            VALUES (
                %s, 
                %s, 
                %s,
                %s, 
                (SELECT genre_id FROM genre WHERE genre_name = 'SciFi' LIMIT 1),
                (SELECT studio_id FROM studio WHERE studio_name = '20th Century Fox' LIMIT 1)
            );
        """
        new_film_data = ("Inception", "2010", 148, "Christopher Nolan")
        cursor.execute(insert_query, new_film_data)
        db.commit()
        
        # Display films after INSERT
        show_films(cursor, "DISPLAYING FILMS AFTER INSERT")
        
        # 3. UPDATE film 'Alien' genre to 'Horror'
        update_query = """
            UPDATE film 
            SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror' LIMIT 1)
            WHERE film_name = 'Alien';
        """
        cursor.execute(update_query)
        db.commit()
        
        # Display films after UPDATE
        show_films(cursor, "DISPLAYING FILMS AFTER UPDATE")
        
        # 4. DELETE film 'Gladiator'
        delete_query = "DELETE FROM film WHERE film_name = 'Gladiator';"
        cursor.execute(delete_query)
        db.commit()
        
        # Display films after DELETE
        show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Invalid username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print(f"Error: {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'db' in locals() and db.is_connected():
            db.close()

if __name__ == "__main__":
    main()