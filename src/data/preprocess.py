"""
Hier wird:
- feautre engineering automatisch durchgeführt, die Dateien werden nicht gespeichert sondern nur als Dataframe instanziert
und fürs Training von ML Modellen verwendet
"""
# alle imports
import pandas as pd
import numpy as np
from Notebooks.data_exp_prep.unsplit import unsplit  # selbstgeschreibene funktion aus /data_exp_prep/unsplit.py
from sklearn.preprocessing import LabelEncoder
import os

def run_preprocessing():

    n = 100
    print('-' * n)
    print('Reading Data')
    # Get the directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path
    data_dir = os.path.join(current_dir, '..', '..', 'Data')

    links_path = os.path.join(data_dir, 'raw', 'links.csv')
    movies_path = os.path.join(data_dir, 'raw', 'movies.csv')
    ratings_path = os.path.join(data_dir, 'raw','ratings')  # for your unsplit function
    tags_path = os.path.join(data_dir, 'raw', 'tags.csv')

    links = pd.read_csv(links_path)
    movies = pd.read_csv(movies_path)
    tags = pd.read_csv(tags_path)
    ratings = unsplit(ratings_path)

    #dictonary in which the keys are the dfs, and the values are the columns that are going to be dropped at the end of data prep
    cols_to_drop = {
        'movies': ['genres', 'genres_list', 'genres_str', 'title', 'title_only'],
        'ratings': ['timestamp', 'Unnamed: 0', 'userId'],
        'tags': ['tag', 'timestamp', 'userId']
    }


    print('-'*n)
    # Movies prep
    print('Preparing movies dataframe')
    movies_copy = movies.copy()

    # separate the genres from each other
    movies_copy['genres_list'] = movies_copy['genres'].apply(lambda x: x.split('|'))

    # join them back with '|' so we can use str.get_dummies
    movies_copy['genres_str'] = movies_copy['genres_list'].apply(lambda x: '|'.join(x))

    # Each variable is converted in as many 0/1 variables as there are different values.
    # https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html
    genre_dummies = movies_copy['genres_str'].str.get_dummies(sep='|')

    # join the genres to the data frame
    movies_copy = movies_copy.join(genre_dummies)
    del genre_dummies

    # seperate the year from the title
    movies_copy[['title_only','year']] = movies_copy['title'].str.extract(r'^(.*)\s\((\d{4})\)$')

    # save the null values as a series
    mask = movies_copy['year'].isna()

    # fill the null values with a random year between 1950 and 2025
    movies_copy.loc[mask, 'year'] = np.random.randint(1950, 2026, size=mask.sum())
    movies_copy['year'] = movies_copy['year'].astype(np.uint16)
    movies_copy['year'] = movies_copy['year'] / movies_copy['year'].max()
    # drop the columns
    movies_copy.drop(columns = cols_to_drop['movies'], inplace = True, axis = 1)

    movies = movies_copy
    del movies_copy
    print(movies.head(5))

    print('-'*n)

    # Ratings prep
    print('Preparing the Ratings')

    ratings.drop(cols_to_drop['ratings'], inplace = True, axis = 1)
    ratings = ratings.groupby(['movieId']).mean()
    ratings['rating'].fillna(ratings['rating'].median(), inplace=True)
    print(ratings.isna().sum())
    ratings['rating'] = ratings['rating'] / ratings['rating'].max()
    print(ratings.head(5))
    print('-'*n)

    # tags prep
    print('Preparing tags')
    # Encode target labels with value between 0 and n_classes-1.
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html
    le = LabelEncoder()

    tags_copy = tags.copy()

    # Cast a pandas object to a string or whatever but in this case string
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.astype.html
    tags_copy['tag'] = tags_copy['tag'].astype(str)

    # encode the string values of tags into numerical data using label encoder
    tags_copy['tag_encoded'] = le.fit_transform(tags_copy['tag'])
    tag_min = tags_copy['tag_encoded'].min()
    tag_max = tags_copy['tag_encoded'].max()
    tags_copy['tag_encoded'] = tags_copy['tag_encoded'].apply(lambda x: np.random.randint(tag_min, tag_max) if pd.isnull(x) else x)

    # drop the cols
    tags_copy.drop(cols_to_drop['tags'], inplace = True, axis = 1)

    tags = tags_copy
    del tags_copy
    print(tags.head(5))
    print('-'*n)
    """
    Optimierung von Datentypen
    """
    # Wie viel Speicher brauchen die einzelnen Dataframes
    print(tags.memory_usage(deep=True).sum() / (1024 * 1024), "MB")
    print(ratings.memory_usage(deep=True).sum() / (1024 * 1024), "MB")
    print(movies.memory_usage(deep=True).sum() / (1024 * 1024), "MB")
    print(links.memory_usage(deep=True).sum() / (1024 * 1024), "MB")
    print('-'*n)

    # Datentyp optimierung
    print('Optimierung von Datentypen')
    tags['movieId'] = tags['movieId'].astype(np.uint32)
    #tags['userId'] = tags['userId'].astype(np.uint32)

    #ratings['movieId'] = ratings['movieId'].astype(np.uint32)
    #ratings['userId'] = ratings['userId'].astype('uint32')
    ratings['rating'] = ratings['rating'].astype(np.float16)

    movies['year'] = movies['year'].astype(np.float16)
    print('-'*n)

    # Wie viel Speicher brauchen die einzelnen Dataframes
    print(tags.memory_usage(deep=True).sum() / (1024 * 1024), "MB")
    print(ratings.memory_usage(deep=True).sum() / (1024 * 1024), "MB")
    print(movies.memory_usage(deep=True).sum() / (1024 * 1024), "MB")
    print(links.memory_usage(deep=True).sum() / (1024 * 1024), "MB")
    print('-'*n)

    """
    Merge all Dataframes into one df
    """
    print('Merging movies and ratings')

    # Merge step by step
    df_merged_1 = movies.merge(ratings, on='movieId', how='outer')
    del movies, ratings
    print('-' * n)
    print('Merging links and tags')
    df = df_merged_1.merge(tags, on='movieId', how='outer')
    del df_merged_1, tags
    print(df.head(3))
    print('-'*n)

    df['rating'].fillna(df['rating'].median(), inplace=True)
    df['tag_encoded'] = df['tag_encoded'].apply(lambda x: np.random.randint(tag_min, tag_max) if pd.isnull(x) else x)
    print(df.isna().sum())
    print('Process Finished')


