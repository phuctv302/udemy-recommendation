from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

users = pd.read_csv('../data/users.csv')
courses = pd.read_csv('../data/courses.csv')
user_reviews = pd.read_csv('../data/users.reviews.csv')

df = pd.merge(user_reviews, courses, left_on='course_id', right_on='id').rename(columns={'id_x': 'id'})
df.drop(['id_y'], axis=1, inplace=True)
df = pd.merge(df, users, left_on='user_id', right_on='id').rename(columns={'id_x': 'id'})
df.drop(['id_y'], axis=1, inplace=True)

df.dropna(inplace=True)

ratings_matrix = df.pivot_table(index='user_id', columns='course_id', values='rating', aggfunc='mean')

user_similarity = cosine_similarity(ratings_matrix)

# get the top 10 similar users to a user
user_id = 336
similar_users = user_similarity[user_id].argsort()[:-11:-1]

# get the courses that these users have rated highly
similar_users_ratings = ratings_matrix.iloc[similar_users].mean()

# recommend the top 10 courses
recommended_courses = similar_users_ratings.sort_values(ascending=False)[:10]

print(recommended_courses)