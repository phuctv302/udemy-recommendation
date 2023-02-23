import sys, os, json
import pandas as pd

# run test
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from process.collabFilter import CollabFilter
from utils.array import ArrayUtils

cf = CollabFilter(num_neighbors=10)
recommend_courses = cf.recommendTop(257, 5)

results = []
courses = pd.read_csv('../data/courses.csv')
courses = json.loads(courses.to_json(orient='records'))
for rc in recommend_courses:
    rc_obj = ArrayUtils.findObjById(rc['id'], courses)
    results.append(rc_obj)
    
print(results)
