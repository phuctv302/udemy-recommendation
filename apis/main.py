from fastapi import FastAPI
import pandas as pd

import sys, os, json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from process.collabFilter import CollabFilter
from utils.array import ArrayUtils

app = FastAPI()

@app.get('/recommendation')
def getRecommendations(user_id: int, num_neighbors: int = 5, num_top: int = 3):
	cf = CollabFilter(num_neighbors)
	data = cf.recommendTop(user_id, num_top)
	for item in data:
		item['id'] = int(item['id'])
	return data

@app.get('/courses')
def getAllCourses(page: int = 1, limit: int = 10):
	courses_df = pd.read_csv('../data/courses.csv')
	courses = json.loads(courses_df.to_json(orient='records'))
	return courses[(page-1)*limit: page*limit]

@app.get('/courses/{course_id}')
def getCourse(course_id: int):
	courses_df = pd.read_csv('../data/courses.csv')
	courses = json.loads(courses_df.to_json(orient='records'))
	return ArrayUtils.findObjById(course_id, courses)

@app.get('/users')
def getAllUsers(page: int = 1, limit: int = 10):
	users_df = pd.read_csv('../data/users.csv')
	users = json.loads(users_df.to_json(orient='records'))
	return users[(page-1)*limit: page*limit]

@app.get('/users/{user_id}')
def getCourse(user_id: int):
	users_df = pd.read_csv('../data/users.csv')
	users = json.loads(users_df.to_json(orient='records'))
	return ArrayUtils.findObjById(user_id, users)