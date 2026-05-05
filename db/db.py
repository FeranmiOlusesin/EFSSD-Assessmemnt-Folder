import sqlite3
import os

def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, 'db', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# ════════════════════════════════════════════════════════
# USERS
# ════════════════════════════════════════════════════════

def get_user_by_username(username):
    """Fetch a single user by their username."""
    connection = get_db_connection()
    user = connection.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    connection.close()
    return user


def get_user_by_id(user_id):
    """Fetch a single user by their ID."""
    connection = get_db_connection()
    user = connection.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    connection.close()
    return user


def create_user(username, hashed_password, full_name, email, phone, uk_postcode, role='customer'):
    """Insert a new user into the database."""
    connection = get_db_connection()
    try:
        connection.execute(
            "INSERT INTO users (username, password, full_name, email, phone, role, uk_postcode) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (username, hashed_password, full_name, email, phone, role, uk_postcode)
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        # Username or email already exists
        return False
    finally:
        connection.close()


def delete_user(user_id):
    """Delete a user and all associated data."""
    conn = get_db_connection()
    conn.execute('DELETE FROM reviews WHERE reviewer_id = ?', (user_id,))
    conn.execute('DELETE FROM orders WHERE customer_id = ?', (user_id,))
    conn.execute('DELETE FROM stores WHERE owner_id = ?', (user_id,))
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()


# ════════════════════════════════════════════════════════
# STORES
# ════════════════════════════════════════════════════════

def get_all_stores():
    """Fetch all verified stores."""
    connection = get_db_connection()
    stores = connection.execute(
        "SELECT stores.*, users.full_name AS owner_name FROM stores JOIN users ON stores.owner_id = users.id WHERE stores.is_verified = 1"
    ).fetchall()
    connection.close()
    return stores


def get_store_by_id(store_id):
    """Fetch a single store by its ID."""
    connection = get_db_connection()
    store = connection.execute(
        "SELECT stores.*, users.full_name AS owner_name FROM stores JOIN users ON stores.owner_id = users.id WHERE stores.id = ?",
        (store_id,)
    ).fetchone()
    connection.close()
    return store


def get_stores_by_owner(owner_id):
    """Fetch all stores belonging to a specific owner."""
    connection = get_db_connection()
    stores = connection.execute(
        "SELECT * FROM stores WHERE owner_id = ?", (owner_id,)
    ).fetchall()
    connection.close()
    return stores


def create_store(owner_id, name, description, address, uk_postcode, delivers_nationwide=0):
    """Insert a new store into the database."""
    connection = get_db_connection()
    connection.execute(
        "INSERT INTO stores (owner_id, name, description, address, uk_postcode, delivers_nationwide) VALUES (?, ?, ?, ?, ?, ?)",
        (owner_id, name, description, address, uk_postcode, delivers_nationwide)
    )
    connection.commit()
    connection.close()


# ════════════════════════════════════════════════════════
# PRODUCTS
# ════════════════════════════════════════════════════════

def get_all_products():
    """Fetch all in-stock products with their category and origin info."""
    connection = get_db_connection()
    products = connection.execute(
        """
        SELECT products.*,
               categories.name  AS category_name,
               categories.icon  AS category_icon,
               origins.country  AS origin_country,
               origins.region   AS origin_region,
               origins.flag_emoji,
               stores.name      AS store_name
        FROM products
        JOIN categories ON products.category_id = categories.id
        JOIN stores     ON products.store_id = stores.id
        LEFT JOIN origins ON products.origin_id = origins.id
        WHERE products.in_stock = 1
        ORDER BY products.created DESC
        """
    ).fetchall()
    connection.close()
    return products


def get_product_by_id(product_id):
    """Fetch a single product with full details."""
    connection = get_db_connection()
    product = connection.execute(
        """
        SELECT products.*,
               categories.name  AS category_name,
               categories.icon  AS category_icon,
               origins.country  AS origin_country,
               origins.region   AS origin_region,
               origins.flag_emoji,
               stores.name      AS store_name
        FROM products
        JOIN categories ON products.category_id = categories.id
        JOIN stores     ON products.store_id = stores.id
        LEFT JOIN origins ON products.origin_id = origins.id
        WHERE products.id = ?
        """,
        (product_id,)
    ).fetchone()
    connection.close()
    return product


def get_products_by_store(store_id):
    """Fetch all products listed by a specific store."""
    connection = get_db_connection()
    products = connection.execute(
        """
        SELECT products.*,
               categories.name AS category_name,
               origins.country AS origin_country,
               origins.flag_emoji
        FROM products
        JOIN categories ON products.category_id = categories.id
        LEFT JOIN origins ON products.origin_id = origins.id
        WHERE products.store_id = ?
        ORDER BY products.created DESC
        """,
        (store_id,)
    ).fetchall()
    connection.close()
    return products


def get_products_by_category(category_slug):
    """Fetch all in-stock products in a given category."""
    connection = get_db_connection()
    products = connection.execute(
        """
        SELECT products.*,
               categories.name AS category_name,
               categories.icon AS category_icon,
               origins.country AS origin_country,
               origins.flag_emoji,
               stores.name     AS store_name
        FROM products
        JOIN categories ON products.category_id = categories.id
        JOIN stores     ON products.store_id = stores.id
        LEFT JOIN origins ON products.origin_id = origins.id
        WHERE categories.slug = ? AND products.in_stock = 1
        ORDER BY products.price_gbp ASC
        """,
        (category_slug,)
    ).fetchall()
    connection.close()
    return products


def get_products_by_origin(country):
    """Fetch all in-stock products from a specific African country."""
    connection = get_db_connection()
    products = connection.execute(
        """
        SELECT products.*,
               categories.name AS category_name,
               origins.country AS origin_country,
               origins.region  AS origin_region,
               origins.flag_emoji,
               stores.name     AS store_name
        FROM products
        JOIN categories ON products.category_id = categories.id
        JOIN stores     ON products.store_id = stores.id
        JOIN origins    ON products.origin_id = origins.id
        WHERE origins.country = ? AND products.in_stock = 1
        ORDER BY products.name ASC
        """,
        (country,)
    ).fetchall()
    connection.close()
    return products


def search_products(query):
    """Search products by name or description using a keyword."""
    connection = get_db_connection()
    like_query = f"%{query}%"
    products = connection.execute(
        """
        SELECT products.*,
               categories.name AS category_name,
               origins.country AS origin_country,
               origins.flag_emoji,
               stores.name     AS store_name
        FROM products
        JOIN categories ON products.category_id = categories.id
        JOIN stores     ON products.store_id = stores.id
        LEFT JOIN origins ON products.origin_id = origins.id
        WHERE (products.name LIKE ? OR products.description LIKE ?)
          AND products.in_stock = 1
        ORDER BY products.name ASC
        """,
        (like_query, like_query)
    ).fetchall()
    connection.close()
    return products


def create_product(store_id, category_id, origin_id, name, description, price_gbp, unit, image, in_stock=1):
    """Insert a new product into the database."""
    connection = get_db_connection()
    connection.execute(
        "INSERT INTO products (store_id, category_id, origin_id, name, description, price_gbp, unit, image, in_stock) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (store_id, category_id, origin_id, name, description, price_gbp, unit, image, in_stock)
    )
    connection.commit()
    connection.close()


def update_product_stock(product_id, in_stock):
    """Toggle a product's in_stock status (1 = in stock, 0 = out of stock)."""
    connection = get_db_connection()
    connection.execute(
        "UPDATE products SET in_stock = ? WHERE id = ?",
        (in_stock, product_id)
    )
    connection.commit()
    connection.close()


# ════════════════════════════════════════════════════════
# CATEGORIES & ORIGINS
# ════════════════════════════════════════════════════════

def get_all_categories():
    """Fetch all product categories."""
    connection = get_db_connection()
    categories = connection.execute(
        "SELECT * FROM categories ORDER BY name ASC"
    ).fetchall()
    connection.close()
    return categories


def get_all_origins():
    """Fetch all countries of origin."""
    connection = get_db_connection()
    origins = connection.execute(
        "SELECT * FROM origins ORDER BY country ASC"
    ).fetchall()
    connection.close()
    return origins


# ════════════════════════════════════════════════════════
# ORDERS
# ════════════════════════════════════════════════════════

def create_order(customer_id, store_id, subtotal_gbp, delivery_fee_gbp, total_gbp, delivery_address, uk_postcode):
    """Insert a new order and return its ID."""
    connection = get_db_connection()
    cursor = connection.execute(
        """
        INSERT INTO orders (customer_id, store_id, subtotal_gbp, delivery_fee_gbp, total_gbp, delivery_address, uk_postcode)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (customer_id, store_id, subtotal_gbp, delivery_fee_gbp, total_gbp, delivery_address, uk_postcode)
    )
    order_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return order_id


def add_order_item(order_id, product_id, quantity, unit_price_gbp):
    """Insert a single item into an order."""
    connection = get_db_connection()
    connection.execute(
        "INSERT INTO order_items (order_id, product_id, quantity, unit_price_gbp) VALUES (?, ?, ?, ?)",
        (order_id, product_id, quantity, unit_price_gbp)
    )
    connection.commit()
    connection.close()


def get_orders_by_customer(customer_id):
    """Fetch all orders placed by a customer, newest first."""
    connection = get_db_connection()
    orders = connection.execute(
        """
        SELECT orders.*, stores.name AS store_name
        FROM orders
        JOIN stores ON orders.store_id = stores.id
        WHERE orders.customer_id = ?
        ORDER BY orders.placed_at DESC
        """,
        (customer_id,)
    ).fetchall()
    connection.close()
    return orders


def get_order_by_id(order_id):
    """Fetch a single order with its full details."""
    connection = get_db_connection()
    order = connection.execute(
        """
        SELECT orders.*, stores.name AS store_name,
               users.full_name AS customer_name
        FROM orders
        JOIN stores ON orders.store_id = stores.id
        JOIN users  ON orders.customer_id = users.id
        WHERE orders.id = ?
        """,
        (order_id,)
    ).fetchone()
    connection.close()
    return order


def get_order_items(order_id):
    """Fetch all items within a specific order."""
    connection = get_db_connection()
    items = connection.execute(
        """
        SELECT order_items.*,
               products.name  AS product_name,
               products.image AS product_image,
               (order_items.quantity * order_items.unit_price_gbp) AS line_total
        FROM order_items
        JOIN products ON order_items.product_id = products.id
        WHERE order_items.order_id = ?
        """,
        (order_id,)
    ).fetchall()
    connection.close()
    return items


def update_order_status(order_id, status):
    """Update the status of an order."""
    connection = get_db_connection()
    connection.execute(
        "UPDATE orders SET status = ? WHERE id = ?",
        (status, order_id)
    )
    connection.commit()
    connection.close()


def get_orders_by_store(store_id):
    """Fetch all orders received by a store, newest first."""
    connection = get_db_connection()
    orders = connection.execute(
        """
        SELECT orders.*, users.full_name AS customer_name
        FROM orders
        JOIN users ON orders.customer_id = users.id
        WHERE orders.store_id = ?
        ORDER BY orders.placed_at DESC
        """,
        (store_id,)
    ).fetchall()
    connection.close()
    return orders


# ════════════════════════════════════════════════════════
# REVIEWS
# ════════════════════════════════════════════════════════

def get_reviews_for_product(product_id):
    """Fetch all reviews for a specific product."""
    connection = get_db_connection()
    reviews = connection.execute(
        """
        SELECT reviews.*, users.username AS reviewer_username
        FROM reviews
        JOIN users ON reviews.reviewer_id = users.id
        WHERE reviews.product_id = ?
        ORDER BY reviews.created DESC
        """,
        (product_id,)
    ).fetchall()
    connection.close()
    return reviews


def get_reviews_for_store(store_id):
    """Fetch all reviews for a specific store."""
    connection = get_db_connection()
    reviews = connection.execute(
        """
        SELECT reviews.*, users.username AS reviewer_username
        FROM reviews
        JOIN users ON reviews.reviewer_id = users.id
        WHERE reviews.store_id = ?
        ORDER BY reviews.created DESC
        """,
        (store_id,)
    ).fetchall()
    connection.close()
    return reviews


def create_review(reviewer_id, rating, comment, product_id=None, store_id=None):
    """Insert a new review for a product or a store."""
    connection = get_db_connection()
    connection.execute(
        "INSERT INTO reviews (reviewer_id, product_id, store_id, rating, comment) VALUES (?, ?, ?, ?, ?)",
        (reviewer_id, product_id, store_id, rating, comment)
    )
    connection.commit()
    connection.close()


def get_average_rating_for_product(product_id):
    """Calculate the average star rating for a product."""
    connection = get_db_connection()
    result = connection.execute(
        "SELECT ROUND(AVG(rating), 1) AS avg_rating, COUNT(*) AS total FROM reviews WHERE product_id = ?",
        (product_id,)
    ).fetchone()
    connection.close()
    return result


# ════════════════════════════════════════════════════════
# DELIVERY ZONES
# ════════════════════════════════════════════════════════

def get_delivery_zones_for_store(store_id):
    """Fetch all delivery zones configured for a store."""
    connection = get_db_connection()
    zones = connection.execute(
        "SELECT * FROM delivery_zones WHERE store_id = ?", (store_id,)
    ).fetchall()
    connection.close()
    return zones


def check_delivery_available(store_id, uk_postcode_prefix):
    """Check if a store delivers to a given postcode prefix (e.g. 'E1', 'SW2')."""
    connection = get_db_connection()
    zone = connection.execute(
        "SELECT * FROM delivery_zones WHERE store_id = ? AND uk_postcode_prefix = ?",
        (store_id, uk_postcode_prefix)
    ).fetchone()
    connection.close()
    return zone  # Returns the zone row if found, or None if not available

