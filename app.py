from email.mime import image
from itertools import product
from datetime import datetime
from flask import Flask, render_template, url_for, request, flash, redirect, session
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from werkzeug.security import generate_password_hash, check_password_hash
from db.db import *
import os

# Import get_db_connection if not already imported
try:
    from db.db import get_db_connection
except ImportError:
    # Stub for get_db_connection if not defined in db.db
    import sqlite3
    def get_db_connection():
        import sqlite3
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, 'db', 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

def _looks_like_passlib_hash(stored_pw):
    s = stored_pw.strip() if isinstance(stored_pw, str) else ''
    return s.startswith(('pbkdf2:', 'scrypt:', 'argon2'))


def validate_login(username, password):
    """Verify password against Werkzeug hash; upgrade legacy plaintext passwords once."""
    if not username:
        return None
    uname = username.strip()
    user = get_user_by_username(uname)
    if not user:
        return None
    stored = user['password']
    if isinstance(stored, bytes):
        stored = stored.decode('utf-8', errors='replace')
    if stored is None or not str(stored).strip():
        return None

    stored = stored.strip()
    pw_plain = '' if password is None else password

    try:
        if check_password_hash(stored, pw_plain):
            return user
    except (ValueError, TypeError):
        pass

    # Legacy rows where plaintext was stored — verify then save a real hash once
    if not _looks_like_passlib_hash(stored):
        try:
            from hmac import compare_digest
            if compare_digest(stored, pw_plain):
                new_hash = generate_password_hash(pw_plain, method='pbkdf2:sha256')
                update_user_password(user['id'], new_hash)
                return get_user_by_id(user['id'])
        except (TypeError, AttributeError):
            pass

    return None

# Stub for get_cart_items if not already defined in db.db
def get_cart_items(user_id):
    """
    Returns a list of cart items for the given user_id.
    Replace this stub with your actual implementation or import.
    """
    # Example stub: Replace with actual DB query
    return []

# Stub for add_product_to_cart if not already defined in db.db
def add_product_to_cart(user_id, product_id, quantity):
    """
    Adds a product to the user's cart.
    Replace this stub with your actual implementation or import.
    """
    # Example stub: Replace with actual DB operation
    pass

# Stub for update_cart_item if not already defined in db.db
def update_cart_item(user_id, product_id, quantity):
    """
    Updates the quantity of a product in the user's cart.
    Replace this stub with your actual implementation or import.
    """
    # Example stub: Replace with actual DB operation
    pass

# Stub for remove_cart_item if not already defined in db.db
def remove_cart_item(user_id, product_id):
    """
    Removes a product from the user's cart.
    Replace this stub with your actual implementation or import.
    """
    # Example stub: Replace with actual DB operation
    pass

# Stub for clear_cart if not already defined in db.db
def clear_cart(user_id):
    """
    Clears all items from the user's cart.
    Replace this stub with your actual implementation or import.
    """
    # Example stub: Replace with actual DB operation
    pass

# Stub for get_orders_by_user if not already defined in db.db
def get_orders_by_user(user_id):
    """
    Returns a list of orders for the given user_id.
    Replace this stub with your actual implementation or import.
    """
    # Example stub: Replace with actual DB query
    return []

def get_featured_products(limit=6):
    """
    Returns a list of featured products, limited by the specified number.
    Replace this stub with your actual implementation or import.
    """
    # Example stub: Replace with actual DB query
    return get_all_products()[:limit]

def get_popular_stores(limit=6):
    """
    Returns a list of popular stores, limited by the specified number.
    Replace this stub with your actual implementation or import.
    """
    # Example stub: Replace with actual DB query
    return get_all_stores()[:limit]

_APP_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=os.path.join(_APP_DIR, 'Static'), static_url_path='/static')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
UPLOADS_PATH = "."
app.secret_key = 'your_secret_key'
csrf = CSRFProtect(app)
migrate_stores_schema()


@app.template_global()
def resolve_store_image(path):
    """Map DB value to usable URL — external link or Flask static path; default storefront placeholder."""
    if path and str(path).strip():
        p = str(path).strip()
        if p.startswith(('http://', 'https://')):
            return p
        return url_for('static', filename=p.lstrip('/'))
    return url_for('static', filename='stores/placeholder-shop.svg')


@app.template_global()
def resolve_store_logo(path):
    if not path or not str(path).strip():
        return None
    p = str(path).strip()
    if p.startswith(('http://', 'https://')):
        return p
    return url_for('static', filename=p.lstrip('/'))


def user_can_manage_store(store, user):
    if not store or not user:
        return False
    if user['role'] == 'admin':
        return True
    return user['role'] == 'store_owner' and store['owner_id'] == user['id']


@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf())

@app.template_filter()
def get_username(user_id):
    user = get_user_by_id(user_id)
    return user['username'] if user else 'Unknown'

siteName = "AfroGrocer"
@app.context_processor
def inject_site_name():
    return dict(siteName=siteName)


@app.context_processor
def inject_current_year():
    return dict(current_year=datetime.now().year)

@app.context_processor
def inject_user_role():
    is_admin = False

    if session.get('user_id'):
        user = get_user_by_id(session['user_id'])
        if user and user['role'] == 'admin':
            is_admin = True

    return dict(is_admin=is_admin)

# Home Page
@app.route('/')
def index():
    username = session.get('username', 'Guest')
    featured_products = get_featured_products(limit=6)
    popular_stores = get_popular_stores(limit=6)
    return render_template(
        'index.html',
        title="Welcome",
        username=username,
        featured_products=featured_products,
        popular_stores=popular_stores
    )

# About Page
@app.route('/about')
def about():
    return render_template('about.html', title="About AfroGrocer")

# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Process contact form here (send email, save to db, etc.)
        flash(category='success', message="Thank you for contacting us! We'll get back to you soon.")
        return redirect(url_for('contact'))
    return render_template('contact.html', title="Contact")

# Product List
@app.route('/products')
def product_list():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    # Check if current user is admin
    is_admin = False
    if session.get('user_id'):
        user = get_user_by_id(session['user_id'])
        if user and user['role'] == 'admin':
            is_admin = True
    
    return render_template('product_list.html', products=products, is_admin=is_admin)

# Product Detail
@app.route('/product/<int:id>')
def product_detail(id):
    product = get_product_by_id(id)
    if not product:
        flash(category='warning', message='Product not found!')
        return redirect(url_for('product_list'))
    return render_template('product_detail.html', title=product['name'], product=product)

# Store List
@app.route('/stores')
def store_list():
    uid = session.get('user_id')
    user = get_user_by_id(uid) if uid else None
    is_admin = bool(user and user['role'] == 'admin')
    stores = get_all_stores(verified_only=True)
    return render_template('store_list.html', title="Stores", stores=stores, is_admin=is_admin)


@app.route('/stores/create', methods=('GET', 'POST'))
def store_add():
    uid = session.get('user_id')
    user = get_user_by_id(uid) if uid else None
    if not user or user['role'] != 'admin':
        flash(category='danger', message='Only an administrator can add new stores.')
        return redirect(url_for('store_list'))

    owners = get_users_who_can_own_stores()
    if request.method == 'POST':
        if not owners:
            flash(category='danger', message='No eligible owner accounts.')
            return redirect(url_for('store_add'))
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        address = request.form.get('address', '').strip()
        uk_postcode = request.form.get('uk_postcode', '').strip()
        category = request.form.get('category', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        image = request.form.get('image', '').strip()
        logo = request.form.get('logo', '').strip()
        delivers = 1 if request.form.get('delivers') else 0
        is_verified = 1 if request.form.get('is_verified') else 0
        try:
            owner_id = int(request.form['owner_id'])
        except (KeyError, ValueError):
            flash(category='danger', message='Pick a valid store owner.')
            return redirect(url_for('store_add'))
        sid = create_store(
            owner_id,
            name,
            description,
            address,
            uk_postcode,
            delivers_nationwide=delivers,
            is_verified=is_verified,
            phone=phone,
            email=email,
            category=category or 'African groceries',
            image=image,
            logo=logo,
        )
        flash(category='success', message=f'Store "{name}" has been created.')
        return redirect(url_for('store_detail', id=sid))

    return render_template(
        'store_form.html',
        title='Add store',
        store=None,
        owners=owners,
        is_edit=False,
        submit_label='Create store',
        user_role='admin',
    )


@app.route('/store/<int:sid>/edit', methods=('GET', 'POST'))
def store_edit(sid):
    store = get_store_by_id(sid)
    if not store:
        flash(category='warning', message='Store not found.')
        return redirect(url_for('store_list'))

    uid = session.get('user_id')
    user = get_user_by_id(uid) if uid else None
    if not user_can_manage_store(store, user):
        flash(category='danger', message='You do not have permission to edit this store.')
        return redirect(url_for('store_list'))

    owners = get_users_who_can_own_stores() if user['role'] == 'admin' else []

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        address = request.form.get('address', '').strip()
        uk_postcode = request.form.get('uk_postcode', '').strip()
        category = request.form.get('category', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        image = request.form.get('image', '').strip()
        logo = request.form.get('logo', '').strip()
        delivers = 1 if request.form.get('delivers') else 0

        fields = {
            'name': name,
            'description': description,
            'address': address,
            'uk_postcode': uk_postcode,
            'category': category or 'African groceries',
            'phone': phone,
            'email': email,
            'image': image,
            'logo': logo,
            'delivers_nationwide': delivers,
        }
        if user['role'] == 'admin':
            try:
                fields['owner_id'] = int(request.form['owner_id'])
            except (KeyError, ValueError):
                flash(category='danger', message='Invalid owner selection.')
                return redirect(url_for('store_edit', sid=sid))
            fields['is_verified'] = 1 if request.form.get('is_verified') else 0

        update_store(sid, **fields)
        flash(category='success', message='Store details updated.')
        return redirect(url_for('store_detail', id=sid))

    return render_template(
        'store_form.html',
        title='Edit store',
        store=store,
        owners=owners,
        is_edit=True,
        submit_label='Save changes',
        user_role=user['role'],
    )


# Store Detail
@app.route('/store/<int:id>')
def store_detail(id):
    store = get_store_by_id(id)
    if not store:
        flash(category='warning', message='Store not found!')
        return redirect(url_for('store_list'))
    uid = session.get('user_id')
    user = get_user_by_id(uid) if uid else None
    can_manage_store = user_can_manage_store(store, user)
    products = get_products_by_store(id)
    return render_template(
        'store_detail.html',
        title=store['name'],
        store=store,
        products=products,
        can_manage_store=can_manage_store,
    )

# Cart Page
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_items = get_cart_items(session.get('user_id'))
    cart_total = sum(item['price_gbp'] * item['quantity'] for item in cart_items) if cart_items else 0
    return render_template('cart.html', title="Your Cart", cart_items=cart_items, cart_total=cart_total)

# Add to Cart
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    add_product_to_cart(session.get('user_id'), product_id, quantity)
    flash(category='success', message='Product added to cart!')
    return redirect(url_for('cart'))

# Update Cart
@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    update_cart_item(session.get('user_id'), product_id, quantity)
    flash(category='success', message='Cart updated!')
    return redirect(url_for('cart'))

# Remove from Cart
@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    remove_cart_item(session.get('user_id'), product_id)
    flash(category='info', message='Item removed from cart.')
    return redirect(url_for('cart'))

# Checkout Page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = get_cart_items(session.get('user_id'))
    cart_total = sum(item['price_gbp'] * item['quantity'] for item in cart_items) if cart_items else 0
    if request.method == 'POST':
        # Process order here (save order, send confirmation, etc.)
        flash(category='success', message='Order placed successfully!')
        clear_cart(session.get('user_id'))
        return redirect(url_for('index'))
    return render_template('checkout.html', title="Checkout", cart_items=cart_items, cart_total=cart_total)

# Order History
@app.route('/orders')
def order_history():
    orders = get_orders_by_user(session.get('user_id'))
    return render_template('order_history.html', title="Order History", orders=orders)

# User Profile
@app.route('/profile')
def profile():
    user = get_user_by_id(session.get('user_id'))
    return render_template('profile.html', title="Profile", user=user)

# Register Page
@app.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        repassword = request.form.get('repassword', '')
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        uk_postcode = request.form.get('uk_postcode', '').strip()
        role = 'customer'
        error = None
        if not username:
            error = 'Username is required!'
        elif not full_name.strip():
            error = 'Full name is required!'
        elif not email:
            error = 'Email is required!'
        elif not uk_postcode:
            error = 'UK postcode is required!'
        elif not password or not repassword:
            error = 'Password is required!'
        elif password != repassword:
            error = 'Passwords do not match!'
        elif get_user_by_username(username):
            error = 'Username already exists! Please choose a different one.'
        if error is None:
            # Explicit algorithm so hashing is never ambiguous across Werkzeug versions
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            if not create_user(username, password_hash, full_name, email, phone, uk_postcode, role):
                error = 'Could not register — that username or email may already exist.'
            else:
                flash(category='success', message=f"Registration successful! Welcome {username}!")
                return redirect(url_for('login'))
        if error is not None:
            flash(category='danger', message=f"Registration failed: {error}")
    return render_template('register.html', title="Register")

# Login Page
@app.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        error = None
        user = None
        if not username:
            error = 'Username is required!'
        elif not password:
            error = 'Password is required!'
        else:
            user = validate_login(username, password)
            if user is None:
                error = 'Invalid username or password!'
        if error is None and user is not None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(category='success', message=f"Login successful! Welcome back {username}!")
            return redirect(url_for('index'))
        elif error is not None:
            flash(category='danger', message=f"Login failed: {error}")
    return render_template('login.html', title="Log In")

# Logout
@app.route('/logout/')
def logout():
    session.clear()
    flash(category='info', message='You have been logged out.')
    return redirect(url_for('index'))



@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        price_gbp = request.form['price_gbp']
        image = request.form['image']
        store_id = session.get('user_id')  # Adjust if you have a different way to get store/user

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO products (name, description, category, price_gbp, image, store_id) VALUES (?, ?, ?, ?, ?, ?)',
            (name, description, category, price_gbp, image, store_id)
        )
        conn.commit()
        conn.close()
        flash('Product created successfully!', 'success')
        return redirect(url_for('product_list'))
    return render_template('create_product.html', title="Add New Product")

# Edit A Product Page
@app.route('/update/<int:id>/', methods=('GET', 'POST'))
def update_product(id):

    # Get product data
   product = get_product_by_id(id)
   categories = get_all_categories()

   if request.method == 'POST':
       # Get updated data from the form
       name = request.form['name']
       description = request.form['description']
       category = request.form['category_id']
       price_gbp = request.form['price_gbp']
       unit = request.form['unit']
       image = request.form['image']
       in_stock = request.form.get('in_stock', 0)

       # Update product in the database
       conn = get_db_connection()
       conn.execute(
           'UPDATE products SET name = ?, description = ?, category_id = ?, price_gbp = ?, unit = ?, image = ?, in_stock = ? WHERE id = ?',
           (name, description, category, price_gbp, unit, image, in_stock, id)
       )
       conn.commit()
       conn.close()
       flash('Product updated successfully!', 'success')
       return redirect(url_for('product_detail', id=id))

   return render_template('update_product.html', title="Update Product", product=product, categories=categories)

if __name__ == '__main__':
    print("Starting Flask application...")
    print("Open Your Application in Your Browser: http://localhost:81")
    app.run(host='0.0.0.0', port=81, debug=True)

# Hand-code your admin credentials
# admin_username = 'admin'
# admin_password = generate_password_hash('password')  # Make sure to hash the password!
# admin_full_name = 'Admin User'
# admin_email = 'admin@example.com'
# admin_phone = '07000000000'
# admin_role = 'admin'
# admin_postcode = 'E1 6RF'

# Create the admin user
# create_user(admin_username, admin_password, admin_full_name, admin_email, admin_phone, admin_postcode, role=admin_role)
