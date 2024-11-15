import sqlite3

DB_NAME = "ecommerce.db"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table (role: 'admin' or 'user')
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )""")
    """cursor.execute(
        INSERT INTO users(username, password, role) VALUES(
            'admin', 
            'admin', 
            'admin'
        )
    )"""
    # Items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price REAL,
        stock INTEGER,
        image_path TEXT
    )""")

    # Cart table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        user_id INTEGER,
        item_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(item_id) REFERENCES items(id)
    )""")

    # Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_id INTEGER,
        quantity INTEGER,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(item_id) REFERENCES items(id)
    )""")
    conn.commit()
    conn.close()

def add_user(username, password, role='user'):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   (username, password, role))
    conn.commit()
    conn.close()

def validate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, role,username FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def add_item(name, description, price, stock, image_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, description, price, stock, image_path) VALUES (?, ?, ?, ?, ?)",
                   (name, description, price, stock, image_path))
    conn.commit()
    conn.close()

def get_items(filter_text=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if filter_text:
        cursor.execute("SELECT * FROM items WHERE name LIKE ?", ('%' + filter_text + '%',))
    else:
        cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return items

def add_to_cart(user_id, item_id, quantity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (user_id, item_id, quantity) VALUES (?, ?, ?)",
                   (user_id, item_id, quantity))
    conn.commit()
    conn.close()

def delete_item(item_id):
    """Delete an item by its ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def update_item(item_id, name, description, price, stock, image_path):
    """Update an existing item by its ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE items 
        SET name = ?, description = ?, price = ?, stock = ?, image_path = ?
        WHERE id = ?
    """, (name, description, price, stock, image_path, item_id))
    conn.commit()
    conn.close()

def get_item_by_id(item_id):
    """Retrieve an item by its ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item
def register_user(username, password):
    """Register a new user in the database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'user')",
                       (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
def get_cart_items(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT items.id, items.name, items.price, cart.quantity 
    FROM cart
    JOIN items ON cart.item_id = items.id
    WHERE cart.user_id = ?
    """, (user_id,))
    cart_items = cursor.fetchall()
    conn.close()
    return cart_items

def checkout(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cart_items = get_cart_items(user_id)
    for item_id, name, price, quantity in cart_items:
        cursor.execute("INSERT INTO orders (user_id, item_id, quantity) VALUES (?, ?, ?)",
                       (user_id, item_id, quantity))
        cursor.execute("DELETE FROM cart WHERE user_id = ? AND item_id = ?", (user_id, item_id))
    conn.commit()
    conn.close()
