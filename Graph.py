import math
import collections
from enum import Enum

class GraphType(Enum):
    undirected = 'undir'
    directed = 'dir'

#Graph class represented as an adjacency list,
#self.rep is a dictionary containing nodes as keys,
#set containing adjacent nodes as corresponding values
class Graph:

    #creates empty undirected graph by default
    def __init__(self, graph_type = None, existing_graph = None):
        if existing_graph == None:
            self.rep = {}
            if graph_type == None:
                graph_type = GraphType.undirected
            assert type(graph_type) == GraphType
            self.graph_type = graph_type
        else:
            assert type(existing_graph) == dict
            assert graph_type != None
            self.rep = existing_graph
            self.graph_type = graph_type


    def __str__(self):
        return str(self.rep)

    #element can be a node, node list, 
    #edge tuple, list of edge tuples
    #adds element to self depending on its type
    def __add__(self, element):
        if type(element) is tuple:
            self.add_edge(element)
        elif type(element) is list and len(element) > 0:
            if type(element[0]) is tuple:
                self.add_edges(element)
            else:
                self.add_nodes(element)
        else:
            self.add_node(element) 
    
    #element can be a node, node list, 
    #edge tuple, list of edge tuples
    #deletes element from self depending on its type
    #element MUST be in self
    def __sub__(self, element):
        if type(element) is tuple:
            self.delete_edge(element)
        elif type(element) is list and len(element) > 0:
            if type(element[0]) is tuple:
                self.delete_edges(element)
            else:
                self.delete_nodes(element)
        else:
            self.delete_node(element) 


    #node is a node object
    def add_node(self, node):
        self.rep[node] = set()
        
    #nodes is a list or set of nodes
    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    #edge is a tuple of nodes
    def add_edge(self, edge):
        node1, node2 = edge
        self.rep[node1].add(node2)
        if self.graph_type == GraphType.undirected:
            self.rep[node2].add(node1)

    #edges is a list of tuples of nodes
    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge)

    #node is a node object
    def degree(self, node):
        return len(self.rep[node])

    #order is num of nodes
    def order(self):
        return len(self.rep)

    #same as order
    def __len__(self):
        return self.order()

    #size is num of edges
    def size(self):
        total_edges = 0
        for node in self.rep.keys():
            total_edges += self.degree(node)
        return total_edges // 2

    #edge is a tuple of nodes
    def delete_edge(self, edge):
        node1, node2 = edge
        self.rep[node1].remove(node2)
        if self.graph_type == GraphType.undirected:
            self.rep[node2].remove(node1)
    
    #edges is a list of tuples of nodes
    def delete_edges(self, edges):
        for edge in edges:
            self.delete_edge(edge)

    #node is a node object
    def delete_node(self, node):
        for adjacent_node in self.rep[node]:
            self.rep[adjacent_node].remove(node)
        self.rep.pop(node)

    #nodes is a list or set of nodes
    def delete_nodes(self, nodes):
        for node in nodes:
            self.delete_node(node)

    #returns a relative dictionary contaning nodes paired with
    #objects containing relative distance to the start_node, (math.inf if not valid)
    #and their parent nodes respectively (None if not valid)
    def bfs(self, start_node):
        result = {x : {'distance' : math.inf, 'parent' : None} for x in self.rep.keys()}
        result[start_node].distance = 0
        q = collections.deque()
        q.append(start_node)
        while q:
            parent_node = q.popleft()
            for child_node in self.rep[parent_node]:
                if result[child_node].distance == math.inf:
                    result[child_node].distance = result[parent_node].distance + 1
                    result[child_node].parent = parent_node
                    q.append(child_node)
        return result

    #returns a list containing shortest path
    #from v1 to v2, and none if it doesn't exist
    def get_shortest_path(self, v1, v2):
        bfs_v1 = self.bfs(v1)
        if not(bfs_v1[v2][0] == math.inf):
            result = [v2]
            parent = bfs_v1[v2][1]
            while parent != None:
                result.insert(0, parent)
                parent = bfs_v1[parent][1]
        else:
            result = None
        return result

    #return True if the self is connected, False otherwise    
    def is_connected(self):
        some_item = self.rep.popitem()
        v1 = some_item[0]
        self.rep.setdefault(some_item[0], some_item[1])
        bfs_v1 = self.bfs(v1)
        for child in bfs_v1.values():
            if child[0] == math.inf:
                return False
        return True

    #returns the number of connected components in self
    def count_conn_comps(self):
        nodes = set(self.rep)
        conn_comps = 0
        while nodes:
            v1 = nodes.pop()
            bfs_v1 = self.bfs(v1)
            for node, props in bfs_v1.items():
                if props[0] != math.inf:
                    nodes.discard(node)
            conn_comps += 1
        return conn_comps

    #returns a dictionary representation of the complement of the graph
    def get_complement(self):
        nodes = set(self.rep)
        g_comp = {}
        for node, edges in self.rep.items():
            new_edges = nodes - set(edges)
            new_edges.remove(node)
            g_comp.setdefault(node, new_edges)
        return Graph(self.graph_type, g_comp)

    #returns a dictionary representation of the transpose of the graph
    def get_transpose(self):
        g_transpose = {vertex:set() for vertex in self.rep.keys()}
        for from_vertex, edges in self.rep.items():
            for to_vertex in edges:
                g_transpose[to_vertex].add(from_vertex)
        return Graph(self.graph_type, g_transpose)
        
