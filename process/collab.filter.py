import pandas
from pandas import read_csv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse


def getDataframeRatingsBase(file):
	r_cols = ['user_id', 'course_id', 'rating']
	ratings = pandas.read_csv(file, usecols=r_cols, encoding='utf8')[r_cols]
	ratings.info()
	Y_data = ratings.values
	return Y_data

class CF(object):
	"""
	class Collaborative Filtering, hệ thống đề xuất dựa trên sự tương đồng
	giữa các users với nhau, giữa các items với nhau
	"""
	def __init__(self, data_matrix, k, dist_func=cosine_similarity, uuCF=1):
		"""
		Khởi tạo CF với các tham số đầu vào:
			data_matrix: ma trận Utility, gồm 3 cột, mỗi cột gồm 3 số liệu: user_id, item_id, rating.
			k: số lượng láng giềng lựa chọn để dự đoán rating.
			uuCF: Nếu sử dụng uuCF thì uuCF = 1 , ngược lại uuCF = 0. Tham số nhận giá trị mặc định là 1.
			dist_f: Hàm khoảng cách, ở đây sử dụng hàm cosine_similarity của klearn.
			limit: Số lượng items gợi ý cho mỗi user. Mặc định bằng 10.
		"""
		self.uuCF = uuCF  # user-user (1) or item-item (0) CF
		self.Y_data = data_matrix if uuCF else data_matrix[:, [1, 0, 2]]
		self.k = k
		self.dist_func = dist_func
		self.Ybar_data = None
		# số lượng user và item, +1 vì mảng bắt đầu từ 0
		self.n_users = len(self.Y_data[:, 0])
		self.n_items = len(self.Y_data[:, 1])
		print(self.n_users)
		
	def normalize_matrix(self):
		"""
		Tính similarity giữa các items bằng cách tính trung bình cộng ratings giữa các items.
		Sau đó thực hiện chuẩn hóa bằng cách trừ các ratings đã biết của item cho trung bình cộng
		ratings tương ứng của item đó, đồng thời thay các ratings chưa biết bằng 0.
		"""
		users = self.Y_data[:, 0]
		self.Ybar_data = self.Y_data.copy()
		self.mu = np.zeros((self.n_users,)) # matrix Utility
		for n in range(self.n_users):
			ids = np.where(users == n)[0].astype(np.int32)
			item_ids = self.Y_data[ids, 1]
			ratings = self.Y_data[ids, 2]
			# take mean - avg of all elements in an array
			m = np.mean(ratings)
			if np.isnan(m):
				m = 0  # để tránh mảng trống và nan value
			self.mu[n] = m
			
			# chuẩn hóa
			self.Ybar_data[ids, 2] = ratings - self.mu[n]
		self.Ybar = sparse.coo_matrix((self.Ybar_data[:, 2],
									(self.Ybar_data[:, 1], self.Ybar_data[:, 0])), (self.n_items, self.n_users))
		self.Ybar = self.Ybar.tocsr()
		
	# Tính toán độ tương đồng giữa các user và item
	def similarity(self):
		eps = 1e-6
		self.S = self.dist_func(self.Ybar.T, self.Ybar.T)
		
	def __pred(self, u, i, normalized=1):
		"""
		Dự đoán ra ratings của các users với mỗi items.
		"""
		# tìm tất cả user đã rate item i
		ids = np.where(self.Y_data[:, 1] == i)[0].astype(np.int32)
		users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)
		sim = self.S[u, users_rated_i]
		a = np.argsort(sim)[-self.k:]
		nearest_s = sim[a]
		r = self.Ybar[i, users_rated_i[a]]
		if normalized:
			# cộng với 1e-8, để tránh chia cho 0
			return (r * nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8)

		return (r * nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8) + self.mu[u]

	def pred(self, u, i, normalized=1):
		"""
		Xét xem phương pháp cần áp dùng là uuCF hay iiCF
		"""
		if self.uuCF: return self.__pred(u, i, normalized)
		return self.__pred(i, u, normalized)

	def recommend_top(self, u, top_x):
		"""
		Determine top 10 items should be recommended for user u.
		. Suppose we are considering items which
		have not been rated by u yet.
		"""
		ids = np.where(self.Y_data[:, 0] == u)[0]
		items_rated_by_u = self.Y_data[ids, 1].tolist()
		item = {'id': None, 'similar': None}
		list_items = []

		def take_similar(elem):
			return elem['similar']

		for i in range(self.n_items):
			if i not in items_rated_by_u:
				rating = self.__pred(u, i)
				item['id'] = i
				item['similar'] = rating
				list_items.append(item.copy())

		sorted_items = sorted(list_items, key=take_similar, reverse=True)
		sorted_items.pop(top_x)
		return sorted_items

	def runTest(self):
		print(self.recommend_top(3, 3))

data_matrix = getDataframeRatingsBase('../data/users.reviews.csv')
cf = CF(data_matrix, 336)
cf.normalize_matrix()
cf.similarity()
cf.runTest()
