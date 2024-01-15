CREATE TABLE IF NOT EXISTS products (name TEXT UNIQUE, description TEXT, price NUMBER, picture_url TEXT, unlisted BOOLEAN);
CREATE TABLE IF NOT EXISTS credit_cards (username TEXT, card_number TEXT);
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT);

INSERT OR REPLACE INTO users (username, password) VALUES
    ('instructor', 'swordf1sh!');

INSERT OR REPLACE INTO products VALUES
    ('One hundred pennies', 'Perfect for customers who want to carry as much as possible at all times!', 1.00, '/static/penny.jpg', False),
    ('One sock', 'Fashionable! You can even buy two of them if you want to by fancy.', 5.10, '/static/sock.jpg', False),
    ('A laptop', 'TEST ITEM DO NOT POST', 0.01, '/static/laptop.jpg', True);