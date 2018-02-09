from string import ascii_lowercase as lc
import math
import collections
from graph_data import *

def toNumber(letter):
    return lc.index(letter)

def c2matrix(g_dict):
    matrix = [[0] * len(g_dict) for i in range(len(g_dict))]
    for vertex_main, vertex_edges in g_dict.items():
        for vertex_sub in vertex_edges:
            matrix[toNumber(vertex_main)][toNumber(vertex_sub)] = 1
    return matrix

def c2dictionary(g_matrix):
    base = 'a'
    g_dict = {}
    for index, row in enumerate(g_matrix):
        edges = [chr(index + ord(base)) for index, element in enumerate(row) if element is 1 ]
        g_dict.setdefault(chr(index + ord(base)), edges)
    return g_dict

#runs BFS on undirected graph g_dict starting at vertex s
#the function returns a dictionary where the keys are the names of the vertices and the values
#are lists of length two where the first value of the list is the distance from the key to s, and
#the second value is the parent of key in the BFS tree. 
def BFS(g_dict, vertex):
    result = {x : [math.inf, None] for x in lc[:len(g_dict)]}
    result[vertex][0] = 0
    q = collections.deque()
    q.append(vertex)
    while q:
        v_parent = q.popleft()
        for v_child in g_dict[v_parent]:
            if result[v_child][0] == math.inf:
                result[v_child][0] = result[v_parent][0] + 1
                result[v_child][1] = v_parent
                q.append(v_child)
    return result

#g_dict is a dictionary representation of an undirected graph
#returns the shortest path from the vertex 'start' to the vertex 'end' as a string
#for example, if the shortest path from 'a' to 'd' goes through 'f' and and 'c', the
#function will return [a,f,c,d]'.
def getShortestPath(g_dict, v1, v2):
    BFS_v1 = BFS(g_dict, v1)
    if not(BFS_v1[v2][0] == math.inf):
        result = [v2]
        parent = BFS_v1[v2][1]
        while parent != None:
            result.insert(0, parent)
            parent = BFS_v1[parent][1]
    else:
        result = None
    return result

#g_dict is a dictionary representation of an undirected graph
#return True if the graph is connected, False otherwise    
def isConnected(g_dict):
    some_item = g_dict.popitem()
    v1 = some_item[0]
    g_dict.setdefault(some_item[0], some_item[1])
    BFS_v1 = BFS(g_dict, v1)
    for child in BFS_v1.values():
        if child[0] == math.inf:
            return False
    return True

#g_dict is a dictionary representation of an undirected graph
#returns the number of connected components in g
def countCC(g_dict):
    nodes = set(g_dict)
    conn_comp = 0
    while nodes:
        v1 = nodes.pop()
        BFS_v1 = BFS(g_dict, v1)
        for vertex, props in BFS_v1.items():
            if props[0] != math.inf:
                nodes.discard(vertex)
        conn_comp += 1
    return conn_comp

#g_dict is a dictionary representation of an undirected graph
#returns a dictionary representation of the complement of the graph
def complement(g_dict):
    nodes = set(g_dict)
    g_comp = {}
    for vertex, edges in g_dict.items():
        new_edges = list(nodes - set(edges))
        new_edges.remove(vertex)
        g_comp.setdefault(vertex, new_edges)
    return g_comp

#g_dict is a dictionary representation of a directed graph
#returns a dictionary representation of the transpose of the graph
def transpose(g_dict):
    g_trans = {vertex:[] for vertex in g_dict.keys()}
    for from_vertex, edges in g_dict.items():
        for to_vertex in edges:
            g_trans[to_vertex].append(from_vertex)
    return g_trans

def completeGraph(order):
    return {x : [y for y in lc[:order] if y != x] for x in lc[:order]}
