#!/usr/bin/python
import json
import cjson

class Gourmet:
    def __init__(self):
        self.fn_restaurant_grouped_ranked_reviews = '../dataset/restaurant_grouped_ranked_reviews.json'
        self.groupedRankedReviews = {}
        self.top = 10
        f = open(self.fn_restaurant_grouped_ranked_reviews, 'r')
        for line in f:
            if len(line) < 10:
                continue
            r = cjson.decode(line)
            if r['business_id'] in self.groupedRankedReviews:
                self.groupedRankedReviews[r['business_id']].append(r['stars'])
            else:
                self.groupedRankedReviews[r['business_id']] = [r['stars']]
        f.close()

    def getScore(self, business_id):
        scores = self.groupedRankedReviews[business_id]
        cnt = min(self.top, len(scores))
        s = 0
        for i in range(cnt):
            s += scores[i]
        return s * 1.0 / cnt
        
