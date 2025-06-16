import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect("database3.db")
cursor = conn.cursor()

# Create the Flight, Hotel, and Sales_log tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Flight (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_city TEXT,
    to_city TEXT,
    departure_date TEXT,
    available_seats INTEGER,
    price REAL,
    booking_link TEXT,
    airline TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Hotel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_name TEXT,
    hotel_address TEXT,
    hotel_rating REAL,
    city TEXT,
    available_rooms INTEGER,
    price REAL,
    hotel_link TEXT,
    available_type TEXT,
    available_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Sales_log ( 
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    product_name TEXT,
    sold INTEGER,
    unit_price REAL,
    total_sold_price REAL,
    date TEXT
)
""")

# Add extra flights
flights = [
('Los Angeles', 'New York', '2025-01-01', 3, 399.00, 'https://example.com/booking1','Biman Bangladesh'),
    ('Los Angeles', 'New York', '2025-01-01', 2, 425.50, 'https://example.com/booking2','Air Canada'),
    ('Dhaka', 'Chittagong', '2025-06-10', 4, 120.00, 'https://example.com/booking3','Qatar Airways'),
    ('Dhaka', 'Banasree', '2025-06-23', 6, 749.99, 'https://example.com/booking4','Philippine Airlines'),
    ('Dhaka', 'Wari', '2025-05-22', 2, 200.99, 'https://example.com/booking4','Pamir Airways'),
    ('Dhaka', 'Banasree', '2025-06-21', 4, 303.99, 'https://example.com/booking4','Saudi Airlines'),
    ('Dhaka', 'Wari', '2025-06-22', 3, 215.00, 'https://example.com/booking6','malaysia Airlines'),
    ('Dhaka', 'Paris', '2025-06-21', 33, 215.00, 'https://example.com/booking6','Air France'),
    ('Dhaka','Paris', '2025-06-26', 33, 400.00, 'https://example.com/booking6', 'Emirates'),
    ('Dhaka','Paris', '2025-06-22', 33, 450.00, 'https://example.com/booking6', 'Etihad'),
    ('Paris','New York', '2025-06-26', 33, 100.00, 'https://example.com/booking6',"Spirit"),


]

hotels = [
    ('The Grand Palace', '123 Main St, Cox\'s Bazar', 4.5, 'Cox\'s Bazar', 10, 150.00, 'https://example.com/hotel1', 'Deluxe', '2025-07-01'),
    ('Sea Breeze Resort', 'Beach Road, Cox\'s Bazar', 4.0, 'Cox\'s Bazar', 5, 180.00, 'https://example.com/hotel2', 'Standard', '2025-07-01'),
    ('The Grand Palace', '123 Main St, Cox\'s Bazar', 4.5, 'Cox\'s Bazar', 10, 150.00, 'https://example.com/hotel1', 'Deluxe', '2025-07-01'),
    ('Sea Breeze Resort', 'Beach Road, Cox\'s Bazar', 4.0, 'Cox\'s Bazar', 5, 180.00, 'https://example.com/hotel2', 'Standard', '2025-07-01'),
    ('Skyline Inn', '56 High St, Sylhet', 3.8, 'Sylhet', 8, 90.00, 'https://example.com/hotel3', 'Suite', '2025-06-15'),
    ('Hilltop Retreat', 'Hill Road, Bandarban', 4.7, 'Bandarban', 3, 200.00, 'https://example.com/hotel4', 'Deluxe', '2025-06-20'),
    ('Urban Stay', 'Banani, Dhaka', 4.2, 'Dhaka', 6, 130.00, 'https://example.com/hotel5', 'Standard', '2025-06-30'),
    ('City Comfort Hotel', 'Gulshan, Dhaka', 4.0, 'Dhaka', 4, 120.00, 'https://example.com/hotel6', 'Standard', '2025-06-22'),
    ('Parisian Suites', '45 Rue de Rivoli, Paris', 4.9, 'Paris', 2, 300.00, 'https://example.com/hotel7', 'Luxury', '2025-06-21'),
    ('Budget Inn', '18 Avenue des Champs-Élysées, Paris', 3.2, 'Paris', 5, 85.00, 'https://example.com/hotel8', 'Basic', '2025-06-21'),
    ('Parisian Suites', '45 Rue de Rivoli, Paris', 4.9, 'Paris', 2, 300.00, 'https://example.com/hotel7', 'Luxury', '2025-06-21'),
    ('Budget Inn', '18 Avenue des Champs-Élysées, New York', 3.2, 'New York', 5, 85.00, 'https://example.com/hotel8', 'Basic', '2025-06-26'),
    ('Bangla Hotel', '22 Avenue des Champs-Élysées, New York', 3.2, 'New York', 5, 100.00, 'https://example.com/hotel8', 'Basic', '2025-06-26'),
    
]

# Sales data (removed log_id as it is auto-incremented)
sales_data = [
    (6, 'Food - Frozen Foods', 28, 6.99, 195.72, '2024-06-01'),
    (6, 'Food - Frozen Foods', 28, 6.99, 195.72, '2024-06-01'),
    (3,6,'Food - Frozen Foods',	28,	6.99,	195.72,    '2024-06-01'),
              (4,6,'Food - Frozen Foods',	28,	6.99,	195.72,    '2024-06-01'),
              (5,6,'Food - Frozen Foods',	28,	6.99,	195.72,    '2024-06-01'),
              (6,6,'Food - Frozen Foods',	28,	6.99,	195.72,    '2024-06-01'),
              (7,6,'Food - Frozen Foods',	28,	6.99,	195.72,    '2024-06-01'),
              (8,6,'Food - Frozen Foods',	28,	6.99,	195.72,    '2024-06-01'),
              (9,6,'Food - Frozen Foods',	28,	6.99,	195.72,   '2024-06-01'),
              (10, 4, 'Food - Cooking Oils', 2, 4.99, 9.98, '2024-06-02'),
                (11, 6, 'Food - Supplements', 6, 24.99, 149.94,  '2024-06-02'),
                (12, 6, 'Food - Frozen Foods', 2, 1.99, 3.98,  '2024-06-02'),
                (13, 9, 'Food - Produce', 28, 3.49, 97.72,  '2024-06-02'),
                (14, 1, 'Audio', 4, 39.99, 159.96,  '2024-06-02'),
                (15, 8, 'Home', 11, 39.99, 439.89,  '2024-06-05'),
                (16, 3, 'Food - Dairy', 16, 4.99, 79.84, '2024-06-05'),
                (17, 8, 'Food - Bakery', 3, 2.49, 7.47, '2024-06-05'),
                (18, 2, 'Gaming', 27, 299.99, 8099.73, '2024-06-05'),
                (19, 7, 'Food - Bakery', 15, 4.59, 68.85, '2024-06-05'),
                (20, 10, 'Kitchen', 28, 39.99, 1119.72, '2024-06-07'),
                (21, 10, 'Food - Condiments', 10, 3.29, 32.9, '2024-06-07'),
                (22, 2, 'Food - Beverages', 16, 1.99, 31.84, '2024-06-07'),
                (23, 10, 'Food - Grains', 3, 2.49, 7.47, '2024-06-07'),
                (24, 4, 'Gaming', 25, 39.99, 999.75, '2024-06-07'),
                (25, 4, 'Gaming', 11, 69.99, 769.89, '2024-06-07'),
                (26, 5, 'Accessories', 22, 22.99, 505.78, '2024-06-07'),
                (27, 8, 'Food - Meal Kits', 16, 7.99, 127.84,'2024-06-07'),              
                (29, 6, 'Food - Beverages', 28, 5.99, 167.72, '2024-06-10'),
                (30, 3, 'Food - Snacks', 8, 5.99, 47.92, '2024-06-10'),
                (31, 9, 'Pets', 28, 16.99, 475.72, '2024-06-10'),
                (32, 5, 'Home', 21, 19.99, 419.79, '2024-06-10'),
                (33, 1, 'Accessories', 14, 19.99, 279.86,'2024-06-10'),
                (34, 2, 'Pets', 4, 24.99, 99.96,'2024-06-10'),
                (35, 7, 'Food - Produce', 29, 3.99, 115.71, '2024-06-10'),
                (36, 6, 'Food - Soups', 9, 2.99, 26.91, '2024-06-10'),
                (37, 9, 'Food - Seafood', 24, 9.99, 239.76, '2024-06-10'),
                (38, 2, 'Food - Snacks', 16, 2.29, 36.64, '2024-06-10'),
                (39, 2, 'Home', 1, 15.99, 15.99, '2024-06-10'),
                (40, 1, 'Fitness', 3, 39.99, 119.97, '2024-06-10'),
                (41, 8, 'Clothing - Footwear', 15, 79.99, 1199.85,'2024-06-10'),
                (42, 8, 'Clothing - Footwear', 15, 79.99, 1199.85,'2025-06-10'),
]

# Begin transaction for bulk inserts'''
try:
    conn.execute("BEGIN TRANSACTION;")

    cursor.executemany("""
        INSERT INTO Flight (from_city, to_city, departure_date, available_seats, price, booking_link, airline)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, flights)

    cursor.executemany("""
        INSERT INTO Hotel (hotel_name, hotel_address, hotel_rating, city, available_rooms, price, hotel_link, available_type, available_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, hotels)

    cursor.executemany("""
        INSERT INTO Sales_log (product_id, product_name, sold, unit_price, total_sold_price, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, sales_data)


    conn.commit()  # Commit all inserts in one transaction

except Exception as e:
    conn.rollback()  # Rollback in case of error
    print("Error:", e)




finally:
    conn.close()  # Close the connection

print("✅ Flights, Hotels, and Sales data added successfully.")
