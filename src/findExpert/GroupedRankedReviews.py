#!/usr/bin/python
import cjson
import json
from operator import itemgetter
class GroupedRankedReviews:
    def __init__(self, fnRstRankedReviewers, fnRstReviews, fnRstGroupedRankedReviews):
        self.rankedReviewers = {}
        self.groupedReviews = {}
        self.reviews = {}
        self.getRankedReviewers(fnRstRankedReviewers)
        self.getGroupReviews(fnRstReviews)
        self.sortGroupedReviews(fnRstGroupedRankedReviews)
    def getRankedReviewers(self, fnRstRankedReviewers):
        rs = []
        f = open(fnRstRankedReviewers, 'r')
        for line in f:
            if len(line) < 10:
                continue
            rs.append(cjson.decode(line))
        for r in rs:
            self.rankedReviewers[r['user_id']] = r['score']
    def getGroupReviews(self, fnRstReviews):
        f = open(fnRstReviews, 'r')
        for line in f:
            if len(line) < 10:
                continue
            r = cjson.decode(line)
            score = self.rankedReviewers[r['user_id']]
            r['user_score'] = score
            self.reviews[r['review_id']] = r
            if r['business_id'] in self.groupedReviews:
                self.groupedReviews[r['business_id']].append([r['review_id'], score])
            else:
                self.groupedReviews[r['business_id']] = [[r['review_id'], score]]  

    def sortGroupedReviews(self, fnRstGroupedRankedReviews):
        for k,v in self.groupedReviews.iteritems():
            sv = sorted(v, key=itemgetter(1), reverse=True)
            self.groupedReviews[k] = sv
        f = open(fnRstGroupedRankedReviews, 'w')
        for k,v in self.groupedReviews.iteritems():
            for r in v:
                json.dump(self.reviews[r[0]], f)
                f.write('\n')
        f.close()

if __name__ == '__main__':
    grr = GroupedRankedReviews('../dataset/restaurant_ranked_reviewers.json', '../dataset/restaurant_reviews.json', '../dataset/restaurant_grouped_ranked_reviews.json')
    print 'done!'
    

