import sys
import index
import json
import re, string
import copy
from nltk.corpus import stopwords
import nltk
import numpy as np
import matplotlib.pyplot as plt
import random
#for graphs
plotly = False
try:
    import plotly
    from plotly.graph_objs import Scatter, Scatter3d, Layout
except ImportError:
    print ("INFO: Plotly is not installed, plots will not be generated.")


regex = re.compile('[%s]' % re.escape(string.punctuation))
cachedStopWords = stopwords.words('english')

class kMeans():
    def __init__(self, seeds, tweets):
        self.seeds = seeds
        self.tweets = tweets
        self.max_iterations = 1000
        self.k = len(seeds)

        self.clusters = {} # cluster to tweetID
        self.rev_clusters = {} # reverse index, tweetID to cluster
        self.jaccardMatrix = {} # stores pairwise jaccard distance in a matrix

        self.initializeClusters()
        self.initializeMatrix()
        
        self.gx = []
        self.gy = []
        

    def jaccardDistance(self, setA, setB):
        # Calcualtes the Jaccard Distance of two sets
        try:
            return 1 - float(len(setA.intersection(setB))) / float(len(setA.union(setB)))
        except TypeError:
            print ('Invalid type. Type set expected.')

    def bagOfWords(self, string):
        # Returns a bag of words from a given string
        # Space delimited, removes punctuation, lowercase
        # Cleans text from url, stop words, tweet @, and 'rt'
        words = string.lower().strip().split(' ')
        for word in words:
            word = word.rstrip().lstrip()
            if not re.match(r'^https?:\/\/.*[\r\n]*', word) \
            and not re.match('^@.*', word) \
            and not re.match('\s', word) \
            and word not in cachedStopWords \
            and word != 'rt' \
            and word != '':
                yield regex.sub('', word)

    def initializeMatrix(self):
        # Dynamic Programming: creates matrix storing pairwise jaccard distances
        for ID1 in self.tweets:
            self.jaccardMatrix[ID1] = {}
            bag1 = set(self.bagOfWords(self.tweets[ID1]['text']))
            for ID2 in self.tweets:
                if ID2 not in self.jaccardMatrix:
                    self.jaccardMatrix[ID2] = {}
                bag2 = set(self.bagOfWords(self.tweets[ID2]['text']))
                distance = self.jaccardDistance(bag1, bag2)
                self.jaccardMatrix[ID1][ID2] = distance
                self.jaccardMatrix[ID2][ID1] = distance

    def initializeClusters(self):
        # Initialize tweets to no cluster
        for ID in self.tweets:
            self.rev_clusters[ID] = -1

        # Initialize clusters with seeds
        for k in range(self.k):
            self.clusters[k] = set([self.seeds[k]])
            self.rev_clusters[self.seeds[k]] = k

    def calcNewClusters(self):
        # Initialize new cluster
        new_clusters = {}
        new_rev_cluster = {}
        for k in range(self.k):
            new_clusters[k] = set()

        for ID in self.tweets:
            min_dist = float("inf")
            min_cluster = self.rev_clusters[ID]

            # Calculate min average distance to each cluster
            for k in self.clusters:
                dist = 0
                count = 0
                for ID2 in self.clusters[k]:
                    dist += self.jaccardMatrix[ID][ID2]
                    count += 1
                if count > 0:
                    avg_dist = dist/float(count)
                    if min_dist > avg_dist:
                        min_dist = avg_dist
                        min_cluster = k
            new_clusters[min_cluster].add(ID)
            new_rev_cluster[ID] = min_cluster
        return new_clusters, new_rev_cluster

    def converge(self):
        # Initialize previous cluster to compare changes with new clustering
        new_clusters, new_rev_clusters = self.calcNewClusters()
        self.clusters = copy.deepcopy(new_clusters)
        self.rev_clusters = copy.deepcopy(new_rev_clusters)

        # Converges until old and new iterations are the same
        iterations = 1
        while iterations < self.max_iterations:
            new_clusters, new_rev_clusters = self.calcNewClusters()
            iterations += 1
            if self.rev_clusters != new_rev_clusters:
                self.clusters = copy.deepcopy(new_clusters)
                self.rev_clusters = copy.deepcopy(new_rev_clusters)
            else:
                #print iterations
                return
            
    
    def printClusterText(self):
        # Prints text of clusters
        for k in self.clusters:
            for ID in self.clusters[k]:
                print (self.tweets[ID]['text'])
            print ('\n')
 
    def printClusters(self):
        # Prints cluster ID and tweet IDs for that cluster
        for k in self.clusters:
            print (str(k) + ':' + ','.join(map(str,self.clusters[k])))

    def printMatrix(self):
        # Prints jaccard distance matrix
        for ID in self.tweets:
            for ID2 in self.tweets:
                print (ID, ID2, self.jaccardMatrix[ID][ID2])
                
    def plotClusters(self):
    	# Plots Cluster on graph
        print ('\n')
        x = 10
        y = 10
        n = -1
        start = self.seeds[0]
        colors = ['b','g','r','c','m','y','k']
        for k,ID1 in zip(self.clusters,self.seeds):
                n = n + 1
                x = x + self.jaccardMatrix[start][ID1]
                y = y + self.jaccardMatrix[start][ID1]
                self.gx.append(x)
                self.gy.append(y)
                #plt.scatter(x, y, c='b', marker='x', alpha=1)
                for ID2 in self.clusters[k]:
                    a = self.gx[n] - self.jaccardMatrix[ID1][ID2]
                    b = self.gx[n] + self.jaccardMatrix[ID1][ID2]
                    x = random.uniform(a,b)
                        
                    a = self.gy[n] - self.jaccardMatrix[ID1][ID2]
                    b = self.gy[n] + self.jaccardMatrix[ID1][ID2]
                    y = random.uniform(a,b)

                    plt.scatter(x, y, c=colors[n%len(colors)], marker='o', alpha=0.5)
                
        plt.show()
    				
                
    	
def main():
    file1 = "tweets.json" 
    file2 = "seeds.txt"
    tweets = {}
    with open(file1, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            tweets[tweet['id']] = tweet
    
    f = open(file2)
    seeds = [int(line.rstrip(',\n')) for line in f.readlines()]
    f.close()

    kmeans = kMeans(seeds, tweets)
    kmeans.converge()
    kmeans.printClusterText()
    kmeans.printClusters()
    #kmeans.printMatrix()
    kmeans.plotClusters()
    

if __name__ == '__main__':
    main()
