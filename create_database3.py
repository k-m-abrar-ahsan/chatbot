import sqlite3
import os
from datetime import datetime

# Define the database file name
DB_FILE = 'database3.db'

def create_and_populate_database():
    # Remove the database file if it already exists to ensure a clean slate
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed existing database: {DB_FILE}")

    conn = None
    try:
        # Connect to SQLite database (it will be created if it doesn't exist)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Create Flight table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Flight (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_city TEXT NOT NULL,
                to_city TEXT NOT NULL,
                departure_date TEXT NOT NULL,
                price REAL NOT NULL,
                available_seats INTEGER NOT NULL,
                airline TEXT NOT NULL
            )
        ''')
        print("Flight table created.")

        # Create Hotel table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Hotel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                hotel_name TEXT NOT NULL,
                price REAL NOT NULL,
                available_rooms INTEGER NOT NULL,
                available_date TEXT NOT NULL,
                room_type TEXT NOT NULL
            )
        ''')
        print("Hotel table created.")

        # Insert sample Flight data
        # Using specific dates for consistency with queries
        june_22_2025 = '2025-06-22'
        june_26_2025 = '2025-06-26'
        june_27_2025 = '2025-06-27'

        flights_data = [
            ('Dhaka', 'Paris', june_22_2025, 50.00, 100, 'Air France'),
            ('Dhaka', 'Paris', june_22_2025, 60.00, 50, 'Turkish Airlines'),
            ('Paris', 'New York', june_26_2025, 450.00, 120, 'Delta'),
            ('Paris', 'New York', june_26_2025, 350.00, 70, 'American Airlines'),
            ('New York', 'Los Angeles', '2025-07-01', 300.00, 200, 'United Airlines'),
            ('Dhaka', 'London', '2025-07-10', 700.00, 80, 'British Airways'),
            ('London', 'Dhaka', '2025-07-20', 650.00, 90, 'Biman Bangladesh Airlines')
        ]
        cursor.executemany('''
            INSERT INTO Flight (from_city, to_city, departure_date, price, available_seats, airline)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', flights_data)
        print("Sample Flight data inserted.")

        # Insert sample Hotel data
        hotels_data = [
            ('New York', 'Grand Hyatt', 250.00, 50, june_26_2025, 'Luxury'),
            ('New York', 'The Pod Hotel', 120.00, 80, june_26_2025, 'Budget'),
            ('New York', 'Marriott Marquis', 300.00, 30, june_27_2025, 'Luxury'),
            ('Paris', 'Hotel Louvre', 200.00, 40, june_22_2025, 'Mid-range'),
            ('Paris', 'Ritz Paris', 800.00, 10, june_22_2025, 'Luxury'),
            ('Dhaka', 'Radisson Blu', 150.00, 70, '2025-06-20', 'Luxury'),
            ('London', 'The Langham', 400.00, 25, '2025-07-10', 'Luxury')
        ]
        cursor.executemany('''
            INSERT INTO Hotel (city, hotel_name, price, available_rooms, available_date, room_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', hotels_data)
        print("Sample Hotel data inserted.")

        # Commit changes and close connection
        conn.commit()
        print("Database created and populated successfully!")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_and_populate_database()