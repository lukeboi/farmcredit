from flask import Flask, g
import sqlite3

# create flask app
app = Flask(__name__)

# db setup
DATABASE = 'data.db'

# db helper functions
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
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True)