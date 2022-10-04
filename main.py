from flask import Flask
import time

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/api/')
def api():
    return "am ogjfiew ojfieo wjfiowe  us" + str(time.time())

if __name__ == "__main__":
    app.run(debug=True)