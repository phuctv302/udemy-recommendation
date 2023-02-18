import ast

class StringUtils:
    def __init__(self):
        pass

    @staticmethod
    def toObject(str):
        return ast.literal_eval(str)