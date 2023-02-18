import pandas as pd
import requests
import json
import time

class ReviewAPI:
	def __init__(self, user, password):
		self.user = user
		self.password = password

	def fetch(self):
		data = []
		i = 0
		for course_id in self.getListCourseIds(2000):
			url = f'https://www.udemy.com/api-2.0/courses/{course_id}/reviews?page_size=1000'
			while url:
				print(f'[*] Fetching: {url}')
				print(f' [x] Course remaining: {len(self.getListCourseIds(2000)) - i}')
				i += 1

				res = requests.get(url, auth=(self.user, self.password)).json()
				if res.get('results'):
					[review.update({'course_id': course_id}) for review in res['results']]
					data += res['results']

				url = res.get('next')
    
    
		print(' [x] Finish fetching review api udemy')

		# save data to file
		df = pd.read_json(json.dumps(data))
		df.to_csv('../data/reviews.2.csv')
		print(' [x] Success saving data to file')
  
	def getListCourseIds(self, n):
		data = []
		df = pd.read_csv('../data/courses.csv')
		df = df.iloc[n:(n+999)]
		for index, row in df.iterrows():
			data.append(row['id'])

		return data
				
		
  
user = '6KurIWFyvzm9s0Pduu7Vha7lhQZp65mBZO7QmHGS'
password = 'qF0IG28OtiuL7KU9TAYcCtqzVZqqH2ONj6JxcfgBnIxT4cdDRGdXMHkNm9UxgEcJ5pVeSuSkEDooy6cFvq3o7LTdhefT7aM7IyRkxhorfbr3t5AFx1TgBNMrwuTexRgK'
reviewAPI = ReviewAPI(user, password)
reviewAPI.fetch()