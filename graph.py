import json
import operator
from collections import OrderedDict

import numpy
import csv


class Graph:

	def __init__(self):
		self.matrix = None
		self.json_data = None
		self.mapping = OrderedDict()
		self.teleport_matrix = None
		self.adjacency_matrix = None
		
	def load_from_json(self, input_file='data.json'):
		data = []
		data_teleport = []
		data_adjacecency = []
		
		with open(input_file) as data_file:
			self.json_data = json.load(data_file, object_pairs_hook=OrderedDict)
		i = 0
		for key in self.json_data:
			data.append([])
			data_teleport.append([])
			data_adjacecency.append([])
			self.mapping[key] = i
			i += 1
			
		for key in self.json_data:
			for key2 in self.mapping:
				if key2 in self.json_data[key]['pointsTo']:
					data[self.mapping[key]].append(1/len(self.json_data[key]['pointsTo']))
					data_adjacecency[self.mapping[key]].append(1)
				else:
					data[self.mapping[key]].append(0)
					data_adjacecency[self.mapping[key]].append(0)
				data_teleport[self.mapping[key]].append(1)
				
		self.matrix = numpy.matrix(data)
		self.teleport_matrix = numpy.matrix(data_teleport)/len(data_teleport)
		self.adjacency_matrix = numpy.matrix(data_adjacecency)
		
	def page_rank(self, u=0.85, output_file='pr_file.txt'):
		random_walk = self.matrix + 0
		transition_matrix = random_walk*u + self.teleport_matrix*(1-u)
		transition_matrix = transition_matrix**20
		i = 0
		ans = {}
		for key in self.mapping:
			ans[key] = transition_matrix.item(i)
			i += 1
			
		sorted_x = sorted(ans.items(), key=operator.itemgetter(1))
		with open(output_file, 'w') as pr_file:
			for k, v in sorted_x:
				pr_file.write(k + '\t' + str(v) + '\n')
				
	
	def gephi_csv_generator(self):
		with open("C:\Users\Luiz Vasconcelos\Desktop\\nodesData.csv", "wb") as file:	
			csv_file = csv.writer(file)
			
			csv_file.writerow(['Id'] + ['Label'])
			count = 0
	
			for item in self.json_data:
				csv_file.writerow([count] + [item])
				count = count+1
				
			file.close()
			
		with open("C:\Users\Luiz Vasconcelos\Desktop\\edgesData.csv", "wb") as file:
			csv_file2 = csv.writer(file)
		
			csv_file2.writerow(['Source'] + ['Target'] + ['Type'] + ['Id'] + ['Weight'])
			count2 = 0
			
			print self.adjacency_matrix
			print str(len(self.adjacency_matrix))
			
			for x in range(0,len(self.adjacency_matrix)):
				print x
				for y in range(0,len(self.adjacency_matrix)):
					if self.adjacency_matrix.item(x,y) == 1:
						csv_file2.writerow([self.mapping.keys()[x]] + [self.mapping.keys()[y]] + ['Undirected'] + [count2] + [1.0])
						count2 = count2+1
				
			file.close()
	
	
if __name__ == '__main__':
	g = Graph()
	g.load_from_json('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa.json')
	g.gephi_csv_generator()
	g.page_rank()