import sqlite3

def connect(path="app.db"):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row  
    conn.execute("CREATE TABLE IF NOT EXISTS account (id INTEGER PRIMARY KEY, name TEXT NOT NULL, sum INTEGER NOT NULL)")
    conn.execute("CREATE TABLE IF NOT EXISTS module  (id INTEGER PRIMARY KEY, name TEXT NOT NULL, sum INTEGER NOT NULL)")
    conn.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, ammount INTEGER NOT NULL, module_id INTEGER NOT NULL REFERENCES module(id), account_id INTEGER NOT NULL REFERENCES account(id), comment TEXT, date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
    conn.execute("CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, name TEXT NOT NULL, value TEXT NOT NULL)")
    conn.execute("INSERT OR IGNORE INTO settings (id, name, value) VALUES (1, 'window_selected', '1')")
    
    return conn

def submit_transaction(conn, ammount, module_id, account_id, comment, date):
    conn.execute("INSERT INTO transactions (ammount, module_id, account_id, comment, date) VALUES (?, ?, ?, ?, ?)", (ammount, module_id, account_id, comment, date))
    conn.commit()