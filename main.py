from flask import Flask, g, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

# create flask app
app = Flask(__name__)
app.secret_key = 'verysecretkey'

# db setup
DATABASE = 'data.db'

# initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        
# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def ensure_users_table_exists():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Fields (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT UNIQUE NOT NULL,
            Address TEXT NOT NULL,
            Industry TEXT NOT NULL,
            Owner TEXT NOT NULL,
            ZipCode TEXT NOT NULL,
            County TEXT NOT NULL,
            LandOwner TEXT NOT NULL,
            FOREIGN KEY (Owner) REFERENCES Users(Username)
        )
    """)

    # cur.execute("""
    #     CREATE TABLE IF NOT EXISTS Crops (
    #         ID INTEGER PRIMARY KEY AUTOINCREMENT,
    #         CropType TEXT NOT NULL,
    #         Industry TEXT NOT NULL,
    #         FieldID INTEGER NOT NULL,
    #         FOREIGN KEY (FieldID) REFERENCES Fields(ID)
    #     )
    # """)

    cur.execute("INSERT OR IGNORE INTO Users (Username, Password) VALUES (?, ?)", ("lukefarritor", "password"))
    
    cur.execute("INSERT OR IGNORE INTO Fields (Name, Address, Industry, Owner, ZipCode, County, LandOwner) VALUES (?, ?, ?, ?, ?, ?, ?)", ("Example Field", "123 Main St\n Lincoln, NE 68236", "Agriculture", "lukefarritor", "68526", "Lancaster", "Luke Farritor"))
    
    # cur.execute("INSERT INTO Crops (CropType, Industry, FieldID) VALUES (?, ?, ?)", ("Corn", "Agriculture", 1))

    db.commit()

    
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    ensure_users_table_exists()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verify user credentials
        cur = get_db().cursor()
        command = "SELECT * FROM Users WHERE Username=? AND Password=?"
        res = cur.execute(command, (username, password))

        if res.fetchone() is not None:
            user = User(username)
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


# db helper functions
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

def init_db():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL
        )
    """)
    
    # Insert sample user

    db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# api endpoint for sustainability data
@app.route('/api/<city>')
def api(city):
    cur = get_db().cursor()
    command = "SELECT Data FROM Data WHERE Name='" + city + "'"
    print(command)
    res = cur.execute(command)
    data = str(res.fetchone()[0])
    print(data)
    return data.replace("\n", "<br>")
    # return "am ogjfiew ojfieo wjfiowe  us" + str(time.time()) + " " + city

# return static html at index route
@app.route('/')
@login_required
def index():
    # return app.send_static_file("index.html")
    return render_template("map.html")

@app.route('/fields')
@login_required
def fields():
    cur = get_db().cursor()
    command = "SELECT * FROM Fields WHERE Owner=?"
    res = cur.execute(command, (current_user.id,))
    print(current_user.id)

    fields = res.fetchall()
    print(fields)
    return render_template('fields.html', fields=fields)

if __name__ == "__main__":
    # with app.app_context():
    #     init_db()
    app.run(debug=True)