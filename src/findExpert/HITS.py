import math
import heapq
class HITS:
    def __init__(self, graph):
        self.graph = graph
        
    def updateAuth(self):
        norm = 0
        for n in self.graph.nodes_iter():
            n.auth = 0
            for hub in n.linkedBy:
                n.auth = n.auth + hub.hub
            norm = norm + n.auth**2
        
        #normalize
        norm = math.sqrt(norm)
        for n in self.graph.nodes_iter():
            n.auth = n.auth / norm
            
    def updateHub(self):
        norm = 0
        for n in self.graph.nodes_iter():
            n.hub = 0
            for auth in n.linkTo:
                n.hub = n.hub + auth.auth
            norm = norm + n.hub**2
            
        #normalize 
        norm = math.sqrt(norm)
        for n in self.graph.nodes_iter():
            n.hub = n.hub / norm
    
    def calAuthHub(self, n_iter):
        while(n_iter > 0):
            self.updateAuth()
            self.updateHub()
            n_iter = n_iter - 1
    
    def getNodes(self):
        return self.graph.nodes()
    
    def topAuthUser(self, num):
        heapiedUser = []
        for n in self.graph.nodes_iter():
            heapq.heappush(heapiedUser, (-n.auth, n))#-n.auth to form a max heap
        if (len(heapiedUser) < num):
            n_user = len(heapiedUser)
        else:
            n_user = num
        
        topNodes = [heapq.heappop(heapiedUser) for i in range(n_user)]
        return [t[1] for t in topNodes]
        

    def topHubUser(self, num):
        heapiedUser = []
        for n in self.graph.nodes_iter():
            heapq.heappush(heapiedUser, (-n.hub, n))#-n.hub to form a max heap
        if (len(heapiedUser) < num):
            n_user = len(heapiedUser)
        else:
            n_user = num

        topNodes = [heapq.heappop(heapiedUser) for i in range(n_user)]
        return [t[1] for t in topNodes]
