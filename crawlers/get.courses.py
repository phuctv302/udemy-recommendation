import pandas as pd
import requests
import json

class CourseAPI:
	def __init__(self, url, user, password):
		self.url = url
		self.user = user
		self.password = password

	def fetch(self):
		data = []
		while self.url:
			print(f'[*] Fetching: {self.url}')

			res = requests.get(self.url, auth=(self.user, self.password)).json()
			if res.get('results'):
				data += res.get('results')

			self.url = res.get('next')
		print(' [x] Finish fetching course api udemy')

		# save data to file
		df = pd.read_json(json.dumps(data))
		df.to_csv('./data/courses.csv')
		print(' [x] Success saving data to file')
				
		
  
url = 'https://www.udemy.com/api-2.0/courses?page_size=100'
user = '6KurIWFyvzm9s0Pduu7Vha7lhQZp65mBZO7QmHGS'
password = 'qF0IG28OtiuL7KU9TAYcCtqzVZqqH2ONj6JxcfgBnIxT4cdDRGdXMHkNm9UxgEcJ5pVeSuSkEDooy6cFvq3o7LTdhefT7aM7IyRkxhorfbr3t5AFx1TgBNMrwuTexRgK'
courseAPI = CourseAPI(url, user, password)
courseAPI.fetch()