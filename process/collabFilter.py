import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics.pairwise import cosine_similarity

from scipy.sparse import csr_matrix
from scipy import sparse
import os

# LOAD DATA
users = pd.read_csv('../data/users.csv')
courses = pd.read_csv('../data/courses.csv')
user_reviews = pd.read_csv('../data/users.reviews.csv')

class CollabFilter():
	def __init__(self, num_neighbors):
		self.Y_data = user_reviews[['user_id', 'course_id', 'rating']]
		self.num_neighbors = num_neighbors
		self.Ybar_data = self.Y_data.values.copy()

		self.num_users = len(self.Y_data['user_id'].unique())
		self.num_courses = len(self.Y_data['course_id'].unique())

	def normalizeMatrix(self):
		self.matrix_util = np.zeros((self.Y_data['user_id'].max(), ))
		user_ids = self.Y_data['user_id']
		for u_id in user_ids.unique():
			id_indexes = np.where(user_ids == u_id)[0].astype(np.int32)
			ratings = self.Ybar_data[id_indexes, 2]
			# calc avg
			m = np.mean(ratings)
			if np.isnan(m):
				m = 0
			#normalize
			self.Ybar_data[id_indexes, 2] = ratings - m
	
		# Create the sparse matrix
		Ybar = sparse.coo_matrix((self.Ybar_data[:, 2], (self.Ybar_data[:, 1].astype(np.int32), self.Ybar_data[:, 0].astype(np.int32))))
		Ybar_csr = csr_matrix(Ybar)
		del Ybar
		return Ybar_csr

	# calc similarity between user and item
	def similarity(self):
		eps = (1e-6)
		self.user_sim = cosine_similarity(self.Ybar_csr.T, self.Ybar_csr.T, dense_output=False)
		return cosine_similarity(self.Ybar_csr.T, self.Ybar_csr.T, dense_output=False)

	def pred(self, user_id, course_id):
		# find all users who have rated this course
		rated_user_indexes = np.where(self.Y_data.values[:, 1] == course_id)[0].astype(np.int32)
		rated_user_ids = self.Y_data.values[rated_user_indexes, 0].astype(np.int32)
		sim = self.user_sim[(user_id, rated_user_ids)].toarray()[0]
		nearest_indexes = np.argsort(sim)[-self.num_neighbors:]
		nearest_s = sim[nearest_indexes]
		r = self.Ybar_csr[(course_id, rated_user_ids[nearest_indexes])]
		return (r * nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8)

	def recommendTop(self, user_id, top_x):
		ids = np.where(self.Ybar_data[:, 0] == user_id)[0]
		courses_rated_by_u = self.Ybar_data[ids, 1].tolist()
		course = {'id': None, 'similar': None}
		list_courses = []
		
		def takeSimilar(elem):
			return elem['similar']

		self.Ybar_csr = self.normalizeMatrix()
		self.user_sim = self.similarity()
		for course_id in self.Y_data['course_id'].unique():
			if course_id not in courses_rated_by_u:
				rating = self.pred(user_id, course_id)
				course['id'] = course_id
				course['similar'] = rating
				list_courses.append(course.copy())
	
		sorted_courses = sorted(list_courses, key=takeSimilar, reverse=True)
		# sorted_courses.pop(top_x)
		return sorted_courses[:top_x]