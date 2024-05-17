from flask import Flask, jsonify, request
import os
import pickle
import numpy as np

app = Flask(__name__)

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
artifacts_dir = os.path.join(current_dir, 'artifacts')

# Load the pickle files
model_path = os.path.join(artifacts_dir, 'model.pkl')
book_names_path = os.path.join(artifacts_dir, 'book_names.pkl')
final_rating_path = os.path.join(artifacts_dir, 'final_rating.pkl')
book_pivot_path = os.path.join(artifacts_dir, 'book_pivot.pkl')

with open(model_path, 'rb') as f:
    model = pickle.load(f)

with open(book_names_path, 'rb') as f:
    book_names = pickle.load(f)

with open(final_rating_path, 'rb') as f:
    final_rating = pickle.load(f)

with open(book_pivot_path, 'rb') as f:
    book_pivot = pickle.load(f)


def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]: 
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)

    return poster_url

def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                books_list.append(j)
    return books_list , poster_url 

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the Book Recommender System API!"
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    selected_book = data['selected_book']
    recommended_books, poster_url = recommend_book(selected_book)
    print("recommended_books")
    print(recommended_books)
    print("poster_url")
    print(poster_url)
    response = {
        'recommended_books': recommended_books,
        'poster_urls': poster_url
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
