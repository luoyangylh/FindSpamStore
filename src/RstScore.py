#!/usr/bin/python
import json
import cjson
from SVMScore import *
from Gourmet import *
class RstScore:
    def __init__(self, gourmet, svm, gWeight=0.5, svmWeight=0.5):
        self.gourmet = gourmet
        self.svm = svm
        self.gWeight = gWeight
        self.svmWeight = svmWeight
        self.business = {}

    def getRstScoreById(self, business_id):
        return self.gWeight * self.gourmet.getScore(business_id) + self.svmWeight * self.svm.getScore(business_id)
        #return self.gWeight * self.gourmet.getScore(business_id)
    def calRstScore(self):
        fn_yelp_business = '../yelp_dataset/yelp_academic_dataset_business.json'
        fn_business = '../dataset/restaurant.json'
        f = open(fn_yelp_business, 'r')
        for line in f:
            if len(line) < 10:
                continue
            b = cjson.decode(line)
            if 'Restaurants' in b['categories']:
                self.business[b['business_id']] = b
        f.close()

        for k in self.business.iterkeys():
            self.business[k]['our_score'] = self.getRstScoreById(k)

        f = open(fn_business, 'w')
        for v in self.business.itervalues():
            json.dump(v, f)
            f.write('\n')
        f.close()
                
if __name__ == '__main__':
    g = Gourmet()
    svm = SVMScore()
    rst = RstScore(g, svm)
    rst.calRstScore()
    print 'done!'
    
