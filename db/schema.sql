DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS delivery_zones;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS origins;
DROP TABLE IF EXISTS stores;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT UNIQUE NOT NULL,
    password    TEXT NOT NULL,
    full_name   TEXT NOT NULL,
    email       TEXT UNIQUE NOT NULL,
    phone       TEXT,
    role        TEXT NOT NULL DEFAULT 'customer',  -- 'customer', 'store_owner', 'admin'
    uk_postcode TEXT,
    created     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE origins (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    country     TEXT NOT NULL,
    region      TEXT NOT NULL,  -- e.g. 'West Africa', 'East Africa'
    flag_emoji  TEXT
);

CREATE TABLE categories (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT UNIQUE NOT NULL,
    slug    TEXT UNIQUE NOT NULL,
    icon    TEXT
);

CREATE TABLE stores (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id            INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name                TEXT NOT NULL,
    description         TEXT,
    address             TEXT,
    uk_postcode         TEXT,
    phone               TEXT,
    email               TEXT,
    category            TEXT DEFAULT 'African groceries',
    image               TEXT,          -- storefront / hero URL or static path under /static/
    logo                TEXT,          -- square logo URL or static path
    delivers_nationwide BOOLEAN DEFAULT 0,
    is_verified         BOOLEAN DEFAULT 0,
    created             TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id    INTEGER NOT NULL REFERENCES stores(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    origin_id   INTEGER REFERENCES origins(id),
    name        TEXT NOT NULL,
    description TEXT,
    price_gbp   REAL NOT NULL,
    unit        TEXT,           -- e.g. '1kg', '500ml', 'per piece'
    image       TEXT,           -- URL or filename of product image
    in_stock    BOOLEAN DEFAULT 1,
    created     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventory (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id   INTEGER NOT NULL REFERENCES products(id),
    store_id     INTEGER NOT NULL REFERENCES stores(id),
    quantity     INTEGER NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE delivery_zones (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id           INTEGER NOT NULL REFERENCES stores(id),
    uk_postcode_prefix TEXT NOT NULL,   -- e.g. 'E1', 'SW', 'B'
    fee_gbp            REAL NOT NULL DEFAULT 0.00,
    est_days           INTEGER NOT NULL DEFAULT 2
);

CREATE TABLE orders (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id      INTEGER NOT NULL REFERENCES users(id),
    store_id         INTEGER NOT NULL REFERENCES stores(id),
    status           TEXT NOT NULL DEFAULT 'pending',  -- 'pending','confirmed','preparing','out_for_delivery','delivered','cancelled'
    subtotal_gbp     REAL NOT NULL,
    delivery_fee_gbp REAL NOT NULL DEFAULT 0.00,
    total_gbp        REAL NOT NULL,
    delivery_address TEXT NOT NULL,
    uk_postcode      TEXT NOT NULL,
    placed_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivered_at     TIMESTAMP
);

CREATE TABLE order_items (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id       INTEGER NOT NULL REFERENCES orders(id),
    product_id     INTEGER NOT NULL REFERENCES products(id),
    quantity       INTEGER NOT NULL,
    unit_price_gbp REAL NOT NULL
);

CREATE TABLE reviews (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    reviewer_id INTEGER NOT NULL REFERENCES users(id),
    product_id  INTEGER REFERENCES products(id),
    store_id    INTEGER REFERENCES stores(id),
    rating      INTEGER NOT NULL,   -- 1 to 5
    comment     TEXT,
    created     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Example delete order for app code / SQL consoles (commented — not runnable as-is without values):
-- DELETE FROM reviews WHERE reviewer_id = ?;
-- DELETE FROM orders WHERE customer_id = ?;
-- DELETE FROM stores WHERE owner_id = ?;
-- DELETE FROM users WHERE id = ?;
