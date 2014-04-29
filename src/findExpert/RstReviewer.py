#!/usr/bin/python
import cjson
import json
import networkx as nx
import math
import heapq
from ReviewerNode import *
from HITS import *
class RstReviewer:
    def __init__(self, fnRstReviews, fnYelpUser, fnRstReviewers):
        self.item_weight = {'auth':1.0, 'hub':1.0, 'votes':1.0, 'review_count':1.0, 'fans':1.0, 'compliments':1.0, 'elite':1.0}
        self.maxScore = 10.0
        
        self.reviewers = {}
        self.rankedReviewers = []
        self.__getReviewersFromRstReviews(fnRstReviews)
        self.__createRstReviewer(fnYelpUser, fnRstReviewers)
        self.__getLargestWeaklyConnectedReviewerGraph(fnRstReviewers)
        self.__calAuthHub()
        self.__normalizeReviewerScore()
        self.__rankingReviewers()
    def __getReviewersFromRstReviews(self, fn):
        rs = []
        f = open(fn, 'r')
        for line in f:
            if len(line) < 10:
                continue
            rs.append(cjson.decode(line))
        for r in rs:
            self.reviewers[r['user_id']] = {}
        f.close()

    def __recordReviewerScore(self, user):
        uId = user['user_id']
        self.reviewers[uId]['user_id'] = uId
        self.reviewers[uId]['auth'] = 0
        self.reviewers[uId]['hub'] = 0
        self.reviewers[uId]['votes'] = sum(user['votes'].itervalues())
        self.reviewers[uId]['review_count'] = user['review_count']
        self.reviewers[uId]['fans'] = user['fans']
        self.reviewers[uId]['compliments'] = sum(user['compliments'].itervalues())
        self.reviewers[uId]['elite'] = len(user['elite'])

    def __createRstReviewer(self, fnYelpUser, fnRstReviewers):
        f_o = open(fnYelpUser, 'r')
        f_n = open(fnRstReviewers, 'w')
        for line in f_o:
            user = cjson.decode(line)
            if user['user_id'] in self.reviewers:
                f_n.write(line)
                self.__recordReviewerScore(user)
        f_o.close()
        f_n.close()

    def __getLargestWeaklyConnectedReviewerGraph(self, fnRstReviewers):
        f = open(fnRstReviewers, 'r')
        G = nx.DiGraph()
        reviewers = []
        for line in f:
            if len(line) < 10:
                continue
            reviewers.append(cjson.decode(line))
        for r in reviewers:
            rId = r['user_id']
            n1 = ReviewerNode(rId)
            friendsId = r['friends']
            for fId in friendsId:
                if (not rId == fId) and (fId in self.reviewers):
                    n2 = ReviewerNode(fId)
                    G.add_edge(n1, n2)
        wG = nx.weakly_connected_component_subgraphs(G)[0]
        for node in wG.nodes_iter():
            node.linkTo = wG.successors(node)
            node.linkedBy = wG.predecessors(node)
        self.wG = wG
                   
    def __calAuthHub(self):
        hits = HITS(self.wG)
        hits.calAuthHub(1000)
        nodes = hits.getNodes()
        for n in nodes:
            if n.user_id in self.reviewers:
                self.reviewers[n.user_id]['auth'] = n.auth
                self.reviewers[n.user_id]['hub'] = n.hub
                
    def __normalizeReviewerScore(self):
        items = self.item_weight.keys()
        maxscore = {i:-1 for i in items}
        for r in self.reviewers.itervalues():
            for i in items:
                if maxscore[i] < r[i]:
                    maxscore[i] = r[i]
        for r in self.reviewers.itervalues():
            for i in items:
                if not maxscore[i] == 0:
                    r[i] = r[i] * 1.0 / maxscore[i]
    def __rankingReviewers(self):
        sumscore = sum(self.item_weight.itervalues())
        for r in self.reviewers.itervalues():
            r['score'] = 0
            for i, w in self.item_weight.iteritems():
                r['score'] += r[i] * w
            r['score'] *= self.maxScore/sumscore

        heapiedUser = []
        for k,r in self.reviewers.iteritems():
            heapq.heappush(heapiedUser, (-r['score'], {k:r}))#-r.score to form a max heap
        numUser = len(heapiedUser)
        topNodes = [heapq.heappop(heapiedUser) for i in range(numUser)]
        self.rankedReviewers = [t[1] for t in topNodes]

    def dumpRankedReviewers(self, fn):
        f = open(fn, 'w')
        for r in self.rankedReviewers:
            json.dump(r.values()[0], f)
            f.write('\n')
        f.close()
if __name__ == '__main__':
    fnRstReviews = '../dataset/restaurant_reviews.json'
    fnYelpUser = '../yelp_dataset/yelp_academic_dataset_user.json'
    fnRstReviewers = '../dataset/restaurant_reviewers.json'
    fnDumpRankedReviewers = '../dataset/restaurant_ranked_reviewers.json'
    rr = RstReviewer(fnRstReviews, fnYelpUser, fnRstReviewers)
    rr.dumpRankedReviewers(fnDumpRankedReviewers)
    for i in range(10):
        print rr.rankedReviewers[i]
    
    print 'done!'


            
