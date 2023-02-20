import pandas as pd
import numpy as np
import sys, os, json, ast

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.string import StringUtils
from utils.array import ArrayUtils

def mergeReviews():
	df0 = pd.read_csv('../data/reviews.csv')
	df1 = pd.read_csv('../data/reviews.1.csv')
	df2 = pd.read_csv('../data/reviews.2.csv')
	df3 = pd.read_csv('../data/reviews.3.csv')
	df4 = pd.read_csv('../data/reviews.4.csv')
	df5 = pd.read_csv('../data/reviews.5.csv')
	df6 = pd.read_csv('../data/reviews.6.csv')
	df7 = pd.read_csv('../data/reviews.7.csv')
	df8 = pd.read_csv('../data/reviews.8.csv')

	df = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7, df8], ignore_index=True)
	df.rename({"Unnamed: 0":"a"}, axis="columns", inplace=True)
	df.drop(["a"], axis=1, inplace=True)
	df.to_csv('../data/users.reviews.csv')

	print('[x] Done')

def fakeUsersData():
	review_df = pd.read_csv('../data/users.reviews.csv')
	user_strings = np.unique(review_df['user'].values)
	user_objs = [StringUtils.toObject(str) for str in user_strings]
	
	new_user_objs = []
	i = 1
	for user in user_objs:
		user['_old'] = json.dumps(user)
		user['id'] = i
		i += 1
		new_user_objs.append(user)
	
	users_df = pd.read_json(json.dumps(new_user_objs))
	users_df.to_csv('../data/users.csv')

	print('[x] Done')

def normalizeReview():
	review_df = pd.read_csv('../data/users.reviews.csv')
	user_df = pd.read_csv('../data/users.csv')

	review_df['user'] = review_df['user'].str.replace("'", "\"")

	df = pd.merge(review_df, user_df[['id', '_old']], left_on='user', right_on='_old')\
		.rename(columns={'id_y': 'user_id'})\
	.rename(columns={'id_x': 'id'})
	
	df.drop('_old', axis=1, inplace=True)
	df.drop(['Unnamed: 0'], axis=1, inplace=True)
	
	df.to_csv('../data/users.reviews.csv')
	print('[x] Done')

def dropRandomReviews():
	review_df = pd.read_csv('../data/users.reviews.csv')
	# calculate number of rows to drop
	n_rows_to_drop = int(0.4 * len(review_df))

	# randomly select rows to drop
	rows_to_drop = np.random.choice(review_df.index, size=n_rows_to_drop, replace=False)

	# drop selected rows
	review_df.drop(['Unnamed: 0'], axis=1, inplace=True)
	review_df = review_df.drop(rows_to_drop)
 
	review_df.to_csv('../data/users.reviews.csv')
	print('[x] Done')
	
# mergeReviews()
# fakeUsersData()
# normalizeReview()
# dropRandomReviews()