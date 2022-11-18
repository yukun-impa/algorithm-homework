import networkx as nx
import matplotlib.pyplot as plt
class MaximumFlow:
    def __init__(self, nodes_num):
        self.INF = 999999
        self.nodes_num = nodes_num
        self.edges = [[0 for x in range(nodes_num + 1)] for y in range(nodes_num + 1)] 
        self.parent = {}

        self.G = nx.DiGraph()
        self.original_edges = [[0 for x in range(nodes_num + 1)] for y in range(nodes_num + 1)] 

    def add_edge(self, from_node, to_node, cap):
        self.edges[from_node][to_node] += cap
        self.original_edges[from_node][to_node] += cap

    
    # Bfs is used to find augmenting paths. Update the hashmap "parent" 
    # while bfs to find the path.
    def bfs(self, source, target):
        visited = [False for x in range(0, self.nodes_num + 1)]
        visited[source] = True
        queue = []
        queue.append(source)
        while len(queue) > 0:
            i = queue[0]
            queue.pop(0)
            for j in range(1, self.nodes_num + 1):
                if self.edges[i][j] > 0 and visited[j] == False:
                    visited[j] = True
                    self.parent[j] = i
                    queue.append(j)

        return visited[target],

    def maximumflow(self, source, target):
        maximum_flow = 0
        while self.bfs(source, target):
            new_flow = self.INF
            curr = target

            """
            Once we find a augmenting path. We try to find the minimum residual
            capacity on this path by backtracking
            """
            while curr != source:
                prev = self.parent[curr]
                new_flow = min(new_flow, self.edges[prev][curr])
                curr = prev
            maximum_flow += new_flow

            # If no augmenting paths are found. the function return maximum flow
            if new_flow == 0:
                return maximum_flow

            # We adjust the residual network
            curr = target
            while curr != source:
                prev = self.parent[curr]
                self.edges[prev][curr] -= new_flow
                self.edges[curr][prev] += new_flow 
                curr = prev
    
    def minimumcut(self, source, target):
        visited = [False for x in range(0, self.nodes_num + 1)]
        visited[source] = True
        queue = []
        queue.append(source)
        while len(queue) > 0:
            i = queue[0]
            queue.pop(0)
            for j in range(1, self.nodes_num + 1):
                if self.edges[i][j] > 0 and visited[j] == False:
                    visited[j] = True
                    self.parent[j] = i
                    queue.append(j)
        return visited
    
    def print_result(self, source, target):
        print("The maximum flow is", self.maximumflow(source, target))
        st = self.minimumcut(source, target)
        G = self.G
        for i in range(1, self.nodes_num + 1):
            G.add_node(i)

        edge_label = {}
        for i in range(1, self.nodes_num + 1):
            for j in range(1, self.nodes_num + 1):
                if self.original_edges[i][j] > 0:
                    G.add_edge(i, j)
        
        pos = nx.spring_layout(G)
        self.pos = pos
        plt.figure()

        for i in range(1, self.nodes_num + 1):
            for j in range(1, self.nodes_num + 1):
                if self.original_edges[i][j] > 0:
                    cap = self.original_edges[i][j]
                    flow = self.original_edges[i][j] - self.edges[i][j]
                    edge_label[(i, j)] = str(flow) + "/" + str(cap)
        
        color = []
        for i in range(1, self.nodes_num + 1):
            if st[i]:
                color.append('green')
            else:
                color.append('red')
        
        labels={node: node for node in G.nodes()}
        labels[source] = 's=' + str(source)
        labels[target] = 't=' + str(target)
        nx.draw(
            G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color=color, alpha=0.9,
            labels=labels

        )


        nx.draw_networkx_edge_labels(
            G, pos,
            edge_label,
            font_color='red',
        )