from flask import Flask, render_template, request
from integration import download_poster_to_user_pc

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=["GET", "POST"])
def search():
    movie_name = request.form['movie_name']
    movie_name = movie_name.lower()
    print(f"movie_name = {movie_name}")
    download_poster_to_user_pc(movie_name)
    return render_template("hello.html", movie_name=movie_name)

app.run(host='127.0.0.5', port=81, debug=False)