import sqlite3

def database():
        conn = sqlite3.connect('database.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS customer 
                (customerId INTEGER PRIMARY KEY, 
                email TEXT,
                password TEXT,
                firstName TEXT,
                lastName TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                country TEXT, 
                phone TEXT
                )''')

        conn.execute('''CREATE TABLE IF NOT EXISTS seller
                (seller_Id INTEGER PRIMARY KEY, 
                email TEXT,
                password TEXT,
                firstName TEXT,
                lastName TEXT,
                store_name TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                country TEXT, 
                phone TEXT
                )''')

        conn.execute('''CREATE TABLE IF NOT EXISTS products
                (productId INTEGER PRIMARY KEY,
                name TEXT,
                price REAL,
                description TEXT,
                image TEXT,
                stock INTEGER,
                seller_email TEXT
                )''')


        conn.execute('''CREATE TABLE IF NOT EXISTS Orders
                (orderId INTEGER PRIMARY KEY,
                productId INTEGER,
                customerId INTEGER
                )''')

        conn.commit()
        conn.close()

