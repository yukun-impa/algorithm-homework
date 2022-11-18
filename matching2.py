import networkx as nx
import matplotlib.pyplot as plt
class MaximumMatching2:
    def __init__(self, set1_num, set2_num):
        self.set1_num = set1_num
        self.set2_num = set2_num
        self.g = [[] for i in range(0, self.set1_num + 1)]
        self.parent_a = [-1 for i in range(0, self.set1_num + 1)]
        self.parent_b = [-1 for i in range(0, self.set2_num + 1)]
        self.vis = [0 for i in range(0, self.set1_num + 1)]
        self.dfn = 0
        self.res = 0

    
    def add_edge(self, a, b):
        self.g[a].append(b)

    def dfs(self, v):
        self.vis[v] = self.dfn

        for u in self.g[v]:
            if self.parent_b[u] == -1:
                self.parent_b[u] = v
                self.parent_a[v] = u
                return True
            
        for u in self.g[v]:
            if self.vis[self.parent_b[u]] != self.dfn and self.dfs(self.parent_b[u]):
                self.parent_a[v] = u
                self.parent_b[u] = v
                return True

        return False
    
    def find_matching(self):
        res = 0
        while True:
            self.dfn += 1
            count = 0
            for i in range(1, self.set1_num + 1):
                if self.parent_a[i] == -1 and self.dfs(i):
                    count += 1
            if count == 0:
                break
            res += count
        return res


    #Please ignore the following codes. They are just used to draw the pictures#
    ############################################################################
    ############################################################################
    def print_result(self):
        print(self.find_matching())
        G = nx.DiGraph()
        
        for i in range(1, self.set1_num + 1):
            G.add_node(i)

        for j in range(1, self.set2_num + 1):
            G.add_node(self.num2char(j))


        for i in range(1, self.set1_num + 1):
            for j in self.g[i]:
                if j != self.parent_a[i]:
                    G.add_edge(i, self.num2char(j), color = 'black')
        
        for i in range(1, self.set1_num + 1):
            if self.parent_a[i] != -1:
                G.add_edge(self.num2char(self.parent_a[i]), i, color = 'red')

        m = self.set1_num
        n = self.set2_num
        pos = {}
        pos.update((m + 1 - i, (0.5, i - m/2)) for i in range(1, m + 1))
        pos.update((self.num2char(n + 1 - i), (1, i - n/2)) for i in range(1, n + 1))

        colors = nx.get_edge_attributes(G, 'color').values()
        
        
        nx.draw(G, pos=pos, edge_color=colors, with_labels=True)
   
    def num2char(self, i):
        return str(i)
