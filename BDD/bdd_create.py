import sqlite3

def create_db():
    conn = sqlite3.connect('model_logs.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS training_logs (
                  id INTEGER PRIMARY KEY,
                  datetime TEXT,
                  model_type TEXT,
                  mse REAL,
                  r2 REAL
              )
              ''')
    c.execute('''
              CREATE TABLE IF NOT EXISTS prediction_logs (
                  id INTEGER PRIMARY KEY,
                  datetime TEXT,
                  prediction REAL,
                  input_data TEXT,
                  user TEXT
              )
              ''')
    conn.commit()
    conn.close()

create_db()
