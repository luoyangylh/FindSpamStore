__author__ = 'longhuayou'

import re
import operator
from collections import defaultdict

class Data:
    stop_words = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am',
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
    def __init__(self, f_review, f_business, restaurant_reviews):
        self.f_review = f_review
        self.f_business = f_business
        self.restaurant_reviews = restaurant_reviews

    def select_restaurant(self):
        restaurant_reviews = open(self.restaurant_reviews, 'w')
        review = open(self.f_review, 'r')
        business = open(self.f_business, 'r')
        business_id = []
        count = 0
        #select business id whose category includes restaurants
        for line in business:
            if re.search(r'restaurants', line.lower()):
                l = re.sub(r'[":]',' ',line)
                i = re.search(r'business_id[\s]*[\S]* ', l)
                id = i.group(0).split()
                business_id.append(id[1])
        #select restaurant reviews according to business id
        for line in review:
            l = re.sub(r'[":]',' ',line)
            i = re.search(r'business_id[\s]*[\S]* ', l)
            id = i.group(0).split()
            if id[1] in business_id:
                print >> restaurant_reviews, line
                count += 1
            print count
        print 'There are %d business ids.' % len(business_id)
        print 'There are %d reviews.' % count

    def select_features(self, top):
        features = defaultdict(list)
        top_f = []
        reviews = []
        f = open(self.restaurant_reviews, 'r')
        for line in f:
            if line == '\n':
                continue
            l = re.sub(r'[^a-z0-9 ]',' ',line.lower())
            t = re.search('text[\s\S]*type[\s]*review', l)
            text = t.group(0).split()
            #text is the list of all the words in a review
            #print text[1:-2]
            terms = text[1:-2]
            for t in terms:
                if t in self.stop_words or len(t) < 2:
                    terms.remove(t)
                else:
                    if t in features:
                        features[t] += 1
                    else:
                        features[t] = 1
            reviews.append(terms)
        #sorted features from most frequent to least frequent
        sorted_f = sorted(features.iteritems(), key=operator.itemgetter(1), reverse=True)
        #top n features in list
        for i in range(top):
            top_f.append(sorted_f[i][0])
        return top_f, reviews

    def calculate_features(self, top_f, review):
        feature_vec = []
        for r in review:
            total = 0
            v = []
            for f in top_f:
                num = r.count(f)
                v.append(num)
                total += num
            if total == 0:
                continue
            for i in range(len(top_f)):
                freq = float(v[i]) / float(total)
                v[i] = freq
            feature_vec.append(v)
        print feature_vec


if __name__ == '__main__':
    d = Data('yelp_academic_dataset_review.json', 'yelp_academic_dataset_business.json', 'restaurant_reviews.json')
    #d.select_restaurant()
    top_f, reviews = d.select_features(100)
    d.calculate_features(top_f, reviews)
