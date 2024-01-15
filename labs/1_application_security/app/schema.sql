CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, picture_url TEXT, password TEXT, password_was_reset DEFAULT 0);
CREATE TABLE IF NOT EXISTS posts (user_id INTEGER, message TEXT, timestamp timestamp);
CREATE TABLE IF NOT EXISTS reset_codes (user_id INTEGER, reset_code TEXT);

INSERT OR REPLACE INTO users (username, picture_url, password) VALUES
    ('alex', '/static/profiles/alex.png', 'swordf1sh!');
INSERT OR REPLACE INTO posts VALUES (1, 'Just setting up my TweetBook!', DateTime('now'));