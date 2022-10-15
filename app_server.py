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
    poster_url = download_poster_to_user_pc(movie_name)
    poster_url = "http://image.tmdb.org/t/p/original/5O1GLla5vNuegqNxNhKL1OKE1lO.jpg"
    return render_template("show_movie.html", movie_name=movie_name)

app.run(host='127.0.0.5', port=81, debug=False)