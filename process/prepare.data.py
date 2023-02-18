import pandas as pd
import numpy as np
import sys, os, json

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
	for i, review in review_df.iterrows():
		for i, user in user_df.iterrows():
			if (user['_old'] == review['user']):
				review['user_id'] = user['id']
				break
	
	review_df.to_csv('../data/users.reviews.csv')
	print('[x] Done')
	
# mergeReviews()
# fakeUsersData()
normalizeReview()