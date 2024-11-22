from flask import Flask, request, g
import sqlite3

app = Flask(__name__)
DATABASE = 'sample.db'

#
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# 
@app.route('/init')
def init_db():
    db = get_db()
    cursor = db.cursor()
    # ユーザーテーブルの作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')
    # 
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    db.commit()
    return "Database initialized!"

#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
      
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing query: {query}")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            return f"Welcome, {user[1]}!"
        else:
            return "Invalid username or password."

    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''
    

if __name__ == '__main__':
    app.run(debug=True)
