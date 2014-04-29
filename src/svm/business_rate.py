__author__ = 'longhuayou'

import re
import math
import operator
import json
from collections import defaultdict
from sklearn import svm

class Data:

    def __init__(self, f_review, f_business, restaurant_reviews, svm_star):
        self.f_review = f_review
        self.f_business = f_business
        self.restaurant_reviews = restaurant_reviews
        self.svm_star = svm_star
        self.stop_words = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am',
                  'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been',
                  'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either',
                  'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have',
                  'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into',
                  'is', 'it', 'its', 'just', 'least', 'let', 'likely', 'may', 'me',
                  'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off',
                  'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say',
                  'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their',
                  'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas',
                  'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while',
                  'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']


    def select_restaurant(self):
        restaurant_reviews = open(self.restaurant_reviews, 'w')
        review = open(self.f_review, 'r')
        business = open(self.f_business, 'r')
        business_id = []
        business_star = []
        count = 0
        #select business id whose category includes restaurants
        for line in business:
            j = json.loads(line)
            if 'Restaurants' in j['categories']:
                business_star.append(j['stars'])
                business_id.append(j['business_id'])

        #select restaurant reviews according to business id
        for r in review:
            js = json.loads(r)
            if js['business_id'] in business_id:
                print >> restaurant_reviews, r,
                count += 1
            print count
        print 'There are %d business ids.' % len(business_id)
        print 'There are %d reviews.' % count
        return business_id, business_star


    def select_features(self, business_id, top):
        features = defaultdict(list)
        top_f = []
        reviews = defaultdict(list)
        f = open(self.restaurant_reviews, 'r')
        for line in f:
            j = json.loads(line)
            if j['business_id'] in business_id[:1000]:
                #draw review text
                text = re.sub(r'[^a-z0-9 ]',' ', j['text'].lower())
                term = text.split()

                for t in term:
                    if t not in self.stop_words and len(t) > 2:
                        reviews[j['business_id']].append(t)
                        if t in features:
                            features[t] += 1
                        else:
                            features[t] = 1
        #sorted features from most frequent to least frequent
        sorted_f = sorted(features.iteritems(), key=operator.itemgetter(1), reverse=True)
        #top n features in list
        for i in range(top):
            top_f.append(sorted_f[i][0])
        return top_f, reviews


    def calculate_features(self, top_f, review, business_id):
        feature_vec = []
        for id in business_id:
            r = review[id]
            total = 0
            v = []
            for f in top_f:
                num = r.count(f)
                v.append(num)
                total += num
            if total == 0:
                for i in range(len(v)):
                    v[i] = 0
            else:
                for i in range(len(top_f)):
                    freq = float(v[i]) / float(total)
                    v[i] = freq
                #print freq
            feature_vec.append(v)
        return feature_vec


    def svm_model(self, feature_vec, id, stars, num):
        svm_file = open(self.svm_star, 'w')
        business_id = id
        train_num_start = num[0]
        train_num_end = num[1]
        test_num_start = num[2]
        test_num_end = num[3]

        clf = svm.LinearSVC(C = 1, multi_class = 'crammer_singer')
        #clf = svm.LinearSVC()
        #clf = svm.SVC(kernel='linear', C=1.0)
        clf.fit(feature_vec[train_num_start:train_num_end], stars[train_num_start:train_num_end])
        auto_star = clf.predict(feature_vec[test_num_start:test_num_end])

        #output stars to file
        business_stars = dict(zip(business_id, auto_star))
        json.dump(business_stars, svm_file)
        #print business_stars

        #test
        original = stars[test_num_start:test_num_end]
        #print original, len(original)
        #print auto_star, len(auto_star)

        same = 0.0
        sum = 0.0
        for i in range(len(auto_star)):
            sum += math.pow(original[i]-auto_star[i], 2)
            if original[i] == auto_star[i]:
                same += 1.0
        similar_rate = same / len(auto_star)
        rmse = math.sqrt(sum / len(auto_star))
        print "The RMSE is ", rmse
        #print clf.score(feature_vec[test_num_start:test_num_end], stars[test_num_start:test_num_end])
        #print weight


if __name__ == '__main__':
    feature_num = 200

    d = Data('yelp_academic_dataset_review.json', 'yelp_academic_dataset_business.json', 'restaurant_reviews.json', 'svm_star.json')
    business_id, business_star = d.select_restaurant()
    #print business_star
    top_f, reviews = d.select_features(business_id, feature_num)
    #print top_f

    print top_f
    feature_vec = d.calculate_features(top_f, reviews, business_id)

    train_num_start = 0
    train_num_end = 1000
    test_num_start = 0
    test_num_end = len(business_id)
    num = [train_num_start, train_num_end, test_num_start, test_num_end]

    d.svm_model(feature_vec, business_id, business_star, num)


