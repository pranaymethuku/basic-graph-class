import math
import collections
from enum import Enum

class GraphType(Enum):
	undirected = 'undir'
	directed = 'dir'


class Graph:
	"""
		Graph class represented as an adjacency list,
		self.rep is a dictionary containing nodes as keys,
		set containing adjacent nodes as corresponding values

		Creates an empty undirected graph if no parameters given

		Requires
		--------
		If existing_graph parameter is non-Null, 
		graph_type parameter must be non-Null.

		If existing graph type is a dictionary (adjacency list),
		value type must be a Set of nodes.

		If existing graph type is a list of lists (adjacency matrix),
		it is converted into an adjacency list representation.           
	"""

	def __init__(self, graph_type=None, existing_graph=None):

		if type(existing_graph) == dict:
			assert graph_type != None
			self.rep = existing_graph
			self.graph_type = graph_type
		elif type(existing_graph) == list:
			assert graph_type != None
			self.graph_type = graph_type
			self.rep = {}
			for index, row in enumerate(existing_graph):
				edges = set(
					[index for index, element in enumerate(row) if element is 1])
				self.rep.setdefault(index, edges)
		elif existing_graph == None:
			self.rep = {}
			if graph_type == None:
				graph_type = GraphType.undirected
			assert type(graph_type) == GraphType
			self.graph_type = graph_type

	def __str__(self):
		return str(self.rep)

	def __add__(self, element):
		"""
			element can be a node, node list, 
			edge tuple, list of edge tuples
			deletes element from self depending on its type
		"""
		if type(element) is tuple:
			self.add_edge(element)
		elif type(element) is list and len(element) > 0:
			if type(element[0]) is tuple:
				self.add_edges(element)
			else:
				self.add_nodes(element)
		else:
			self.add_node(element)

	def __sub__(self, element):
		"""
			element can be a node, node list, 
			edge tuple, list of edge tuples
			deletes element from self depending on its type
			element MUST be in self
		"""
		if type(element) is tuple:
			self.delete_edge(element)
		elif type(element) is list and len(element) > 0:
			if type(element[0]) is tuple:
				self.delete_edges(element)
			else:
				self.delete_nodes(element)
		else:
			self.delete_node(element)

	def add_node(self, node):
		"""
			node is a node object
		"""
		self.rep[node] = set()

	def add_nodes(self, nodes):
		"""
			nodes is a list or set of nodes
		"""
		for node in nodes:
			self.add_node(node)

	def add_edge(self, edge):
		"""
			edge is a tuple of nodes
		"""
		node1, node2 = edge
		self.rep[node1].add(node2)
		if self.graph_type == GraphType.undirected:
			self.rep[node2].add(node1)

	def add_edges(self, edges):
		"""
			edges is a list of tuples of nodes
		"""
		for edge in edges:
			self.add_edge(edge)

	def degree(self, node):
		"""
			node is a node object
		"""
		return len(self.rep[node])

	def get_neighbors(self, node):
		"""
			node is a node object
			returns set of neighbors of node
		"""
		return self.rep[node]

	def order(self):
		"""
			order is num of nodes
		"""
		return len(self.rep)

	def __len__(self):
		"""
			returns num of nodes
		"""
		return self.order()

	def num_of_edges(self):
		total_edges = 0
		for node in self.rep.keys():
			total_edges += self.degree(node)
		return total_edges // 2

	def delete_edge(self, edge):
		"""
			edge is a tuple of nodes
		"""
		node1, node2 = edge
		self.rep[node1].remove(node2)
		if self.graph_type == GraphType.undirected:
			self.rep[node2].remove(node1)

	def delete_edges(self, edges):
		"""
			edges is a list of tuples of nodes
		"""
		for edge in edges:
			self.delete_edge(edge)

	def delete_node(self, node):
		"""
			node is a node object
		"""
		for adjacent_node in self.rep[node]:
			self.rep[adjacent_node].remove(node)
		self.rep.pop(node)

	def delete_nodes(self, nodes):
		"""
			nodes is a list of node objects
		"""
		for node in nodes:
			self.delete_node(node)

	# Utility Definitions follow

	def bfs(self, start_node):
		"""
			Returns a relative dictionary contaning nodes paired with
			objects containing relative distance to the start_node, (math.inf if not valid)
			and their parent nodes respectively (None if not valid)
		"""
		result = {x: {'distance': math.inf, 'parent': None}
				  for x in self.rep.keys()}
		result[start_node].distance = 0
		q = collections.deque()
		q.append(start_node)
		while q:
			parent_node = q.popleft()
			for child_node in self.get_neighbors(parent_node):
				if result[child_node].distance == math.inf:
					result[child_node].distance = result[parent_node].distance + 1
					result[child_node].parent = parent_node
					q.append(child_node)
		return result

	def get_shortest_path(self, v1, v2):
		"""
			Returns a list containing shortest path
			from v1 to v2, and none if it doesn't exist
		"""
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

	def explore(self, parent_node, visited=None):
		"""
			Sub-procedure of DFS, sets value of visited nodes to true
			Updates visited if already present, else creates it

			Returns visited after exploring graph
		"""
		if type(visited) is not dict:
			visited = {x: False for x in self.rep.keys()}
		elif len(visited) != len(self):
			visited.update({x: False for x in self.rep.keys()})
		visited[parent_node] = True
		for child_node in self.get_neighbors(parent_node):
			if not visited[child_node]:
				self.explore(child_node, visited)
		return visited

	def dfs(self):
		"""
			Returns a relative dictionary contaning nodes paired with
			true, indicating all nodes being visited
		"""
		# Need to review decision of returning object
		visited = {x: False for x in self.rep.keys()}
		for node in self.rep.keys():
			if not visited(node):
				self.explore(node, visited)
		return visited

	def is_connected(self):
		"""
			return True if the self is connected, False otherwise    
		"""
		some_item = self.rep.popitem()
		v1 = some_item[0]
		self.rep.setdefault(some_item[0], some_item[1])
		bfs_v1 = self.bfs(v1)
		for child in bfs_v1.values():
			if child[0] == math.inf:
				return False
		return True

	def count_conn_comps(self):
		"""
			returns the number of connected components in self 
		"""
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

	def get_complement(self):
		"""
			returns a dictionary representation of the complement of the graph
		"""
		nodes = set(self.rep)
		g_comp = {}
		for node, edges in self.rep.items():
			new_edges = nodes - set(edges)
			new_edges.remove(node)
			g_comp.setdefault(node, new_edges)
		return Graph(self.graph_type, g_comp)

	def get_transpose(self):
		"""
			returns a dictionary representation of the transpose of the graph
		"""
		g_transpose = {vertex: set() for vertex in self.rep.keys()}
		for from_vertex, edges in self.rep.items():
			for to_vertex in edges:
				g_transpose[to_vertex].add(from_vertex)
		return Graph(self.graph_type, g_transpose)
