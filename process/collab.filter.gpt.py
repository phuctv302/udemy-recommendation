from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# create user-item matrix
user_reviews = pd.read_csv('../data/users.reviews.csv')
user_item_matrix = user_reviews.pivot_table(index='user_id', columns='course_id', values='rating')

# calculate cosine similarity matrix
user_similarity_matrix = cosine_similarity(user_item_matrix)

# get similar users for a given user
user_id = 1
similar_user_ids = user_similarity_matrix[user_id].argsort()[::-1][1:]

# generate recommendations based on similar users' ratings
recommendations = []
for course_id in user_item_matrix.columns:
    if pd.isnull(user_item_matrix.loc[user_id, course_id]):
        rating_sum = 0
        weight_sum = 0
        for similar_user_id in similar_user_ids:
            if not pd.isnull(user_item_matrix.loc[similar_user_id, course_id]):
                similarity_score = user_similarity_matrix[user_id, similar_user_id]
                rating_sum += similarity_score * user_item_matrix.loc[similar_user_id, course_id]
                weight_sum += similarity_score
        if weight_sum > 0:
            recommendation_score = rating_sum / weight_sum
            recommendations.append((course_id, recommendation_score))

# sort recommendations by score and return top N
recommendations.sort(key=lambda x: x[1], reverse=True)
top_n_recommendations = recommendations[:10]

print(top_n_recommendations)