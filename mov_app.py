from flask import Flask, request, jsonify, render_template
from joblib import load
import numpy as np
import pandas as pd
from movie import search, find_similar_movies



# Load the necessary data
vectorizer = load('vectorizer.joblib')
tfidf = load('tfidf.joblib')
movies = load('movies.joblib')
ratings = load('ratings.joblib') 




app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/movie", methods=['POST'])
def movie():
    data = request.get_json()
    title = data.get('title')
    print("Searching for:", title)
    
    # Search top 5 similar titles
    results = search(title)
    if results.empty:
        print("No results found.")  # Debug
        return jsonify({'error': 'Movie not found.'})
    
    movie_id = results.iloc[0]["movieId"]
    recs = find_similar_movies(movie_id)
    return jsonify(recs.to_dict(orient='records'))


 



if __name__ == "__main__":
    app.run(debug=True)