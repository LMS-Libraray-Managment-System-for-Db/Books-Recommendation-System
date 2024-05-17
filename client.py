import streamlit as st
import requests

# Streamlit UI for selecting a book
selected_book = st.text_input("Enter the name of the book:")

# Button to trigger API request
if st.button('Get Recommendations'):
    # API endpoint URL
    url = 'http://127.0.0.1:5000/recommend'

    # JSON data to send in the request
    data = {'selected_book': selected_book}

    # Send POST request to the API
    response = requests.post(url, json=data)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Get response data as JSON
        recommendations = response.json()

        # Display recommendations
        st.write("Recommended Books:")
        for i, book in enumerate(recommendations['recommended_books']):
            st.text(book)
            st.image(recommendations['poster_urls'][i])
    else:
        # Display error message if request fails
        st.error("Failed to get recommendations. Please try again.")
