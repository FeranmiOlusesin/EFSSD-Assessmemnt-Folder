# Test data for the African grocery app

users_data = [
    {
        'username': 'admin',
        'password': 'password',
        'full_name': 'Admin User',
        'email': 'admin@afromart.com',
        'phone': '07700000000',
        'role': 'admin',
        'uk_postcode': 'E1 6RF'
    },
    {
        'username': 'mama_tolu',
        'password': 'password',
        'full_name': 'Toluwani Adeyemi',
        'email': 'tolu@afromart.com',
        'phone': '07711111111',
        'role': 'store_owner',
        'uk_postcode': 'N17 8QT'
    },
    {
        'username': 'kofi_gh',
        'password': 'password',
        'full_name': 'Kofi Mensah',
        'email': 'kofi@afromart.com',
        'phone': '07722222222',
        'role': 'customer',
        'uk_postcode': 'SW2 1RZ'
    }
]

origins_data = [
    {'country': 'Nigeria',   'region': 'West Africa',    'flag_emoji': '🇳🇬'},
    {'country': 'Ghana',     'region': 'West Africa',    'flag_emoji': '🇬🇭'},
    {'country': 'Ethiopia',  'region': 'East Africa',    'flag_emoji': '🇪🇹'},
    {'country': 'Cameroon',  'region': 'Central Africa', 'flag_emoji': '🇨🇲'},
    {'country': 'Senegal',   'region': 'West Africa',    'flag_emoji': '🇸🇳'},
    {'country': 'Kenya',     'region': 'East Africa',    'flag_emoji': '🇰🇪'},
    {'country': 'Uganda',    'region': 'East Africa',    'flag_emoji': '🇺🇬'},
    {'country': 'Zimbabwe',  'region': 'Southern Africa','flag_emoji': '🇿🇼'},
]

categories_data = [
    {'name': 'Grains & Tubers',       'slug': 'grains-tubers',    'icon': '🌾'},
    {'name': 'Spices & Seasonings',   'slug': 'spices-seasonings','icon': '🌶️'},
    {'name': 'Frozen Meat & Fish',    'slug': 'frozen-meat-fish', 'icon': '🐟'},
    {'name': 'Beverages & Drinks',    'slug': 'beverages',        'icon': '🥤'},
    {'name': 'Snacks & Confectionery','slug': 'snacks',           'icon': '🍘'},
    {'name': 'Cooking Oils & Pastes', 'slug': 'oils-pastes',      'icon': '🫙'},
    {'name': 'Canned & Dried Goods',  'slug': 'canned-dried',     'icon': '🥫'},
    {'name': 'Fresh Produce',         'slug': 'fresh-produce',    'icon': '🥬'},
]

stores_data = [
    {
        'owner_username': 'mama_tolu',
        'name': "Mama Tolu's African Kitchen",
        'description': 'Authentic West African groceries delivered across London.',
        'address': '14 High Road, Tottenham, London',
        'uk_postcode': 'N17 8QT',
        'delivers_nationwide': 0,
        'is_verified': 1
    }
]

products_data = [
    # Grains & Tubers
    {
        'store_name': "Mama Tolu's African Kitchen",
        'category_slug': 'grains-tubers',
        'origin_country': 'Nigeria',
        'name': 'Semovita (2kg)',
        'description': 'Fine semolina flour used to make swallow, perfect with egusi or ogbono soup.',
        'price_gbp': 4.99,
        'unit': '2kg bag',
        'image': 'semovita.jpg',
        'in_stock': 1
    },
    {
        'store_name': "Mama Tolu's African Kitchen",
        'category_slug': 'grains-tubers',
        'origin_country': 'Ghana',
        'name': 'Banku Mix (1kg)',
        'description': 'Traditional Ghanaian fermented corn and cassava dough mix.',
        'price_gbp': 3.49,
        'unit': '1kg bag',
        'image': 'banku_mix.jpg',
        'in_stock': 1
    },
    {
        'store_name': "Mama Tolu's African Kitchen",
        'category_slug': 'grains-tubers',
        'origin_country': 'Nigeria',
        'name': 'Eba (Garri) - Yellow (1.5kg)',
        'description': 'Coarse yellow cassava granules for making eba.',
        'price_gbp': 3.99,
        'unit': '1.5kg bag',
        'image': 'yellow_garri.jpg',
        'in_stock': 1
    },
    # Spices & Seasonings
    {
        'store_name': "Mama Tolu's African Kitchen",
        'category_slug': 'spices-seasonings',
        'origin_country': 'Nigeria',
        'name': 'Ogiri (Locust Bean Paste)',
        'description': 'Fermented locust bean condiment, essential for authentic West African soups.',
        'price_gbp': 2.50,
        'unit': '100g jar',
        'image': 'ogiri.jpg',
        'in_stock': 1
    },
    {
        'store_name': "Mama Tolu's African Kitchen",
        'category_slug': 'spices-seasonings',
        'origin_country': 'Cameroon',
        'name': 'Country Onions (Selim Pepper)',
        'description': 'Smoky, aromatic spice pods used in soups and pepper soup base.',
        'price_gbp': 3.20,
        'unit': '50g pack',
        'image': 'country_onions.jpg',
        'in_stock': 1
    },
    # Frozen Meat & Fish
    {
        'store_name': "Mama Tolu's African Kitchen",
        'category_slug': 'frozen-meat-fish',
        'origin_country': 'Nigeria',
        'name': 'Smoked Catfish (Eja Aboriye)',
        'description': 'Whole smoked catfish, adds deep flavour to egusi and vegetable soups.',
        'price_gbp': 6.50,
        'unit': 'per piece (~400g)',
        'image': 'smoked_catfish.jpg',
        'in_stock': 1
    },
    {
        'store_name': "Mama Tolu's African Kitchen",
        'category_slug': 'frozen-meat-fish',
        'origin_country': 'Ghana',
        'name': 'Frozen Tilapia (Whole)',
        'description': 'Fresh frozen whole tilapia, popular across West and East Africa.',
        'price_gbp': 5.99,
        'unit': 'per fish (~600g)',
        'image': 'tilapia.jpg',
        'in_stock': 0
    },
    # Beverages
    {
        'store_name': "Mama Tolu's African Kitchen",
        'category_slug': 'beverages',
        'origin_country': 'Nigeria',
        'name': 'Malta Guinness (Can)',
        'description': 'Non-alcoholic malt drink, a beloved West African classic.',
        'price_gbp': 1.50,
        'unit': '330ml can',
        'image': 'malta_guinness.jpg',
        'in_stock': 1
    },
    # Cooking Oils & Pastes
    {
        'store_name': "Mama Tolu's African Kitchen",
        'category_slug': 'oils-pastes',
        'origin_country': 'Nigeria',
        'name': 'Red Palm Oil (1 litre)',
        'description': 'Pure unrefined red palm oil for soups, stews and jollof rice.',
        'price_gbp': 5.49,
        'unit': '1 litre bottle',
        'image': 'palm_oil.jpg',
        'in_stock': 1
    },
    {
        'store_name': "Mama Tolu's African Kitchen",
        'category_slug': 'oils-pastes',
        'origin_country': 'Ghana',
        'name': 'Egusi (Ground Melon Seeds)',
        'description': 'Pre-ground egusi seeds for making egusi soup. Saves preparation time.',
        'price_gbp': 4.25,
        'unit': '500g pack',
        'image': 'egusi.jpg',
        'in_stock': 1
    },
]