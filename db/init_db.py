import os
import sqlite3
from werkzeug.security import generate_password_hash
from test_data import users_data, origins_data, categories_data, stores_data, products_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')

connection = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH, encoding='utf-8') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# ── Insert users ────────────────────────────────────────────────
for user in users_data:
    cur.execute(
        "INSERT INTO users (username, password, full_name, email, phone, role, uk_postcode) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            user['username'],
            generate_password_hash(user['password'], method='pbkdf2:sha256'),
            user['full_name'],
            user['email'],
            user['phone'],
            user['role'],
            user['uk_postcode']
        )
    )

# ── Insert origins ───────────────────────────────────────────────
for origin in origins_data:
    cur.execute(
        "INSERT INTO origins (country, region, flag_emoji) VALUES (?, ?, ?)",
        (origin['country'], origin['region'], origin['flag_emoji'])
    )

# ── Insert categories ────────────────────────────────────────────
for category in categories_data:
    cur.execute(
        "INSERT INTO categories (name, slug, icon) VALUES (?, ?, ?)",
        (category['name'], category['slug'], category['icon'])
    )

# ── Insert stores ────────────────────────────────────────────────
for store in stores_data:
    cur.execute("SELECT id FROM users WHERE username = ?", (store['owner_username'],))
    owner = cur.fetchone()
    if not owner:
        raise RuntimeError(f"No owner user: {store['owner_username']}")

    cur.execute(
        """
        INSERT INTO stores (
            owner_id, name, description, address, uk_postcode, phone, email, category,
            image, logo, delivers_nationwide, is_verified
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            owner[0],
            store['name'],
            store['description'],
            store['address'],
            store['uk_postcode'],
            store.get('phone', ''),
            store.get('email', ''),
            store.get('category', 'African groceries'),
            store.get('image', ''),
            store.get('logo', ''),
            store.get('delivers_nationwide', 0),
            store.get('is_verified', 1),
        )
    )

# ── Insert products ──────────────────────────────────────────────
for product in products_data:
    cur.execute("SELECT id FROM stores WHERE name = ?", (product['store_name'],))
    store = cur.fetchone()

    cur.execute("SELECT id FROM categories WHERE slug = ?", (product['category_slug'],))
    category = cur.fetchone()

    cur.execute("SELECT id FROM origins WHERE country = ?", (product['origin_country'],))
    origin = cur.fetchone()

    cur.execute(
        "INSERT INTO products (store_id, category_id, origin_id, name, description, price_gbp, unit, image, in_stock) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            store[0],
            category[0],
            origin[0] if origin else None,
            product['name'],
            product['description'],
            product['price_gbp'],
            product['unit'],
            product['image'],
            product['in_stock']
        )
    )

connection.commit()
connection.close()

print("Database initialised successfully.")
print("DB LOCATION:", DB_PATH)
