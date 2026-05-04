import sqlite3
from werkzeug.security import generate_password_hash
from test_data import users_data, origins_data, categories_data, stores_data, products_data

# This script should be run once to set up the database schema and initial data

# Database will be created in the same directory as this script
connection = sqlite3.connect('database.db')

# Open and execute schema.sql to create all tables
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# ── Insert users ────────────────────────────────────────────────
for user in users_data:
    cur.execute(
        "INSERT INTO users (username, password, full_name, email, phone, role, uk_postcode) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            user['username'],
            generate_password_hash(user['password']),
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
    # Look up the owner's ID by their username
    cur.execute("SELECT id FROM users WHERE username = ?", (store['owner_username'],))
    owner = cur.fetchone()

    cur.execute(
        "INSERT INTO stores (owner_id, name, description, address, uk_postcode, delivers_nationwide, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            owner[0],
            store['name'],
            store['description'],
            store['address'],
            store['uk_postcode'],
            store['delivers_nationwide'],
            store['is_verified']
        )
    )

# ── Insert products ──────────────────────────────────────────────
for product in products_data:
    # Look up the store ID by name
    cur.execute("SELECT id FROM stores WHERE name = ?", (product['store_name'],))
    store = cur.fetchone()

    # Look up the category ID by slug
    cur.execute("SELECT id FROM categories WHERE slug = ?", (product['category_slug'],))
    category = cur.fetchone()

    # Look up the origin ID by country name
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

# Commit all changes and close
connection.commit()
connection.close()

print("Database initialised successfully.")

import os
print("DB LOCATION:", os.path.abspath("database.db"))