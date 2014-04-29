__author__ = 'longhuayou'


import json

class SVMScore:
    def __init__(self):
        self.business_star = "../dataset/svm_star.json"
    def getScore(self, business_id):
        file = open(self.business_star, 'r')
        for text in file:
            t = json.loads(text)
            score = t[business_id]
        return score
