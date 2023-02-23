import numpy as np

class ArrayUtils:
	def __init__(self):
		pass

	@staticmethod
	def updateAttrAllObjs(arr, attr_key, attr_value):
		return ArrayUtils.mutateAllObjs(arr, lambda obj: obj.update({attr_key: attr_value}))
  
	@staticmethod
	def mutateAllObjs(arr, fn):
		return [fn(obj) for obj in arr]

	@staticmethod
	def listToNumpyArr(arr):
		if isinstance(arr, np.ndarray):
			return arr
		return np.array(arr)

	@staticmethod
	def findObjBy(key, value, arr):
		for obj in arr:
			if obj[key] == value:
				return obj

	@staticmethod
	def findObjById(value, arr):
		return ArrayUtils.findObjBy('id', value, arr)
