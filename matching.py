import networkx as nx
import matplotlib.pyplot as plt
from maximumflow import MaximumFlow

class MaximumMatching:
    def __init__(self, set1_num, set2_num):
        self.set1_num = set1_num
        self.set2_num = set2_num
        self.nodes_num = set1_num + set2_num
        self.flow_solver = MaximumFlow(self.nodes_num + 1)
        # We add edges from 0 to every node in set1 with capacity 1
        # and edges from j from set2 to node nodes_num + 1 with capacity 1;
        for i in range(1, set1_num + 1):
            self.flow_solver.add_edge(0, i, 1)
        for i in range(set1_num + 1, self.nodes_num + 1):
            self.flow_solver.add_edge(i, self.nodes_num + 1, 1)

        # Please ignore the following line. It's just used to draw the graph
        self.original_edges = [[0 for x in range(self.nodes_num + 1)] for y in range(self.nodes_num + 1)] 
        
    
    def add_edge(self, a, b):
        self.flow_solver.add_edge(a, self.set1_num + b, 1)

        # Please ignore the following line. It's just used to draw the graph
        self.original_edges[a][self.set1_num + b] = 1

    def max_maching(self):
        # We find the maximum matching by find the flow from node "0" to node "nodes_num + 1"
        return self.flow_solver.maximumflow(0, self.nodes_num + 1)
    



    #Please ignore the following codes. They are just used to draw the pictures#
    ############################################################################
    ############################################################################
    def print_result(self):
        print(self.max_maching())
        G = nx.DiGraph()

        for i in range(1, self.set1_num + 1):
            G.add_node(i)

        for j in range(self.nodes_num, self.set1_num, -1):
            G.add_node(self.num2char(j))


        edge_label = {}

        visited_1 = [False for i in range(0, self.set1_num + 1)]
        visited_2 = [False for i in range(0, self.nodes_num + 1)]

        for i in range(1, self.set1_num + 1):
            for j in range(self.set1_num + 1, self.nodes_num + 1):
                if self.original_edges[i][j] > 0:
                    if self.flow_solver.edges[i][j] == 0:
                        visited_1[i] = True
                        visited_2[j] = True
                        G.add_edge(i, self.num2char(j), color = 'r')
                        edge_label[i, self.num2char(j)] = '1/1'
                        G.add_edge('source', i, color = 'r')
                        edge_label[('source', i)] = '1/1'
                        G.add_edge(self.num2char(j), 'target', color = 'r')
                        edge_label[self.num2char(j), 'target'] = '1/1'
                    else:
                        G.add_edge(i, self.num2char(j), color = 'black')
                        edge_label[i, self.num2char(j)] = '0/1'



        for i in range(1, self.set1_num + 1):
            if visited_1[i] == False:
                G.add_edge('source', i, color = 'black')
                edge_label[('source', i)] = '0/1'

        for j in range(self.set1_num + 1, self.nodes_num + 1):
            if visited_2[j] == False:
                G.add_edge(self.num2char(j), 'target', color = 'black')
                edge_label[self.num2char(j), 'target'] = '0/1'

        m = self.set1_num
        n = self.set2_num
        pos = {}
        pos['source'] = (0, n / 4)
        pos['target'] = (2, m / 4)
        pos.update((m + 1 - i, (0.5, i - m/2)) for i in range(1, m + 1))
        pos.update((self.num2char(2 * m +  n + 1 - i), (1.5, i - m - n/2)) for i in range(m + 1, m + n + 1))

        colors = nx.get_edge_attributes(G, 'color').values()
        
        set1 = range(1, self.set1_num + 1)
        
        nx.draw(G, pos=pos, edge_color=colors, with_labels=True)
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_label,
            font_color='red',
        )

   
    def num2char(self, i):
        return str(i - self.set1_num)

