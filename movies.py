#!/usr/bin/env python3

import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer
import random
pd.set_option('display.max_colwidth', None)


# Load dataset
movie_df = pd.read_csv('movies.csv')
movie_df = movie_df.dropna(subset=['genres'])

# Encode genres and keep all original columns
def encode_data(movie_df):
    mlb = MultiLabelBinarizer()
    genre_list = movie_df["genres"].str.split("|")
    genre_encoded = pd.DataFrame(mlb.fit_transform(genre_list), columns=mlb.classes_)
    df = movie_df.copy()
    df = pd.concat([df, genre_encoded], axis=1)
    return df


# KNN recommendation based on genre weights

def knn_recommend(selected_movies, movie_df_encoded, knn, k=10):
    # Ensure movie_df_encoded has the genres encoded
    genre_encoded = movie_df_encoded.drop(columns=["movieId", "title", "genres"])

    # Get the average genre vector of selected movies
    selected_data = movie_df_encoded[movie_df_encoded["movieId"].isin(selected_movies)]
    selected_genres = genre_encoded.loc[selected_data.index]
    avg_genre_vector = selected_genres.mean(axis=0)
    avg_genre_vector /= avg_genre_vector.sum()  # Normalize the average genre vector

    # Convert the query point to a DataFrame to ensure feature names match
    query_point = pd.DataFrame(avg_genre_vector.values.reshape(1, -1), columns=avg_genre_vector.index)

    # Find the nearest neighbors using the fitted knn model
    distances, indices = knn.kneighbors(query_point)

    # Get recommended movie indices and return the corresponding rows from movie_df
    recommendations = movie_df_encoded.iloc[indices[0]]
    return recommendations[["movieId", "title", "genres"]]



# Recommend random movies
def recommend_10_random(movie_df, num=10):
    return movie_df.sample(n=num, random_state=random.randint(1, 100))


# Search for movies, by year or title
def search_movie(search, movie_df):
    if isinstance(search, int):  # Search by year
        year_pattern = rf"\({search}\)"  # Match the exact year in parentheses
        results = movie_df[movie_df["title"].str.contains(year_pattern, na=False, regex=True)]

    elif isinstance(search, str):  # Search by title
        search = search.strip().lower()
        results = movie_df[movie_df["title"].str.lower().str.contains(search, na=False, regex=False)]

    else:
        return "Invalid search type. Please enter a movie title (str) or year (int)."

    return results if not results.empty else "No results found."


# Main movie recommendation system function
def movie_recommendation_system():
    selected_movies = []  # Stores movieId of selected movies
    movie_df_encoded = encode_data(movie_df)  # Create the encoded genre DataFrame

    # Fit the KNN model once with the encoded genre data
    genre_encoded = movie_df_encoded.drop(columns=["movieId", "title", "genres"])
    knn = NearestNeighbors(n_neighbors=10, metric='cosine')
    knn.fit(genre_encoded)

    # First display 10 random movies
    print("\nWelcome to the movie recommendation engine.")
    print("\nHere are 10 random movie suggestions:")
    random_movies = recommend_10_random(movie_df, num=10)
    print(random_movies[["movieId", "title", "genres"]].to_string(index=False))


    while True:
        pd.set_option('display.max_colwidth', None)
        # Run KNN only if there are selected movies
        if selected_movies:
            recommended_movies = knn_recommend(selected_movies, movie_df_encoded, knn)
            print("Here are some recommended movies based on your selection:")
            print(recommended_movies[["movieId", "title", "genres"]].to_string(index=False))


        print("\nChoose an option:")
        print("1. Select a movie by movieId from suggestions")
        print("2. Search for a movie by title or year")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            movie_id = input("Enter the movieId of the movie you'd like to select: ")
            if movie_id.isdigit() and int(movie_id) in movie_df["movieId"].values:
                selected_movies.append(int(movie_id))
                print("Movie added to your selections!")
            else:
                print("Invalid movieId. Please try again.")
                continue  # Restart loop

        elif choice == "2":
            search_term = input("Enter a movie title or year: ")
            search_term = int(search_term) if search_term.isdigit() else search_term
            results = search_movie(search_term, movie_df)
            print(results if isinstance(results, str) else results[["movieId", "title", "genres"]].head(10).to_string(index=False))
            select = input('Enter 1 for main menu, 2 to input movie: ')
            if select == "1":
                continue
            else:
                movie_id = input("Enter the movieId of the movie you'd like to select: ")
                if movie_id.isdigit() and int(movie_id) in movie_df["movieId"].values:
                    selected_movies.append(int(movie_id))
                    print("Movie added to your selections!")
                else:
                    print("Invalid movieId. Please try again.")
                    continue  # Restart loop




        elif choice == "3":
            print("Exiting movie recommendation system. Goodbye!")
            break  # Exit loop

        else:
            print("Invalid input. Please enter 1, 2, or 3.")



# Run the system
movie_recommendation_system()
