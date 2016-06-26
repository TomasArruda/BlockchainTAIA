import math
import json
import operator
from collections import OrderedDict

import numpy


class Graph:

    POINTS_TO_KEY = "pointsTo"

    def __init__(self):
        self.adjacency_matrix = None
        self.matrix = None
        self.json_data = None
        self.mapping = OrderedDict()
        self.teleport_matrix = None
        self.adjacency_list = {}

    def load_from_json(self, input_file='data.json'):
        data = []
        data_adjacency = []
        data_teleport = []

        with open(input_file) as data_file:
            self.json_data = json.load(data_file, object_pairs_hook=OrderedDict)
        i = 0
        for key in self.json_data:
            data.append([])
            data_teleport.append([])
            data_adjacency.append([])
            self.mapping[key] = i
            self.adjacency_list[key] = []
            i += 1

        for key in self.json_data:
            for key2 in self.mapping:
                if key2 in self.json_data[key][self.POINTS_TO_KEY]:
                    data[self.mapping[key]].append(1)
                    data_adjacency[self.mapping[key]].append(1)
                    self.adjacency_list[key].append(key2)
                else:
                    data[self.mapping[key]].append(0)
                    data_adjacency[self.mapping[key]].append(0)
                data_teleport[self.mapping[key]].append(1)

        self.matrix = numpy.matrix(data)/1.
        for key, value in self.mapping.items():
            if len(self.adjacency_list[key]) > 0:
                self.matrix[value, :] = self.matrix[value, :]/len(self.adjacency_list[key])
        self.teleport_matrix = numpy.matrix(data_teleport)/len(data_teleport)
        self.adjacency_matrix = numpy.matrix(data_adjacency)

    def page_rank(self, u=0.85, output_file='pr_file.txt'):
        random_walk = self.matrix + 0
        transition_matrix = random_walk*u + self.teleport_matrix*(1-u)
        transition_matrix = transition_matrix**20
        i = 0
        ans = {}
        for key in self.mapping:
            ans[key] = transition_matrix.item(i)
            i += 1

        sorted_x = sorted(ans.items(), key=operator.itemgetter(1), reverse=True)
        with open(output_file, 'w') as pr_file:
            for k, v in sorted_x:
                pr_file.write(k + '\t' + str(v) + '\n')

    def get_neighbors_of(self, node, from_original=False):
        if from_original:
            return self.json_data[node][self.POINTS_TO_KEY]
        return self.adjacency_list[node]

    def more_metrics(self):
        common_n = {}
        adamic_a = {}
        pref_atta = {}
        iter_count = 0
        iter_total = len(self.mapping)**2
        for key in self.mapping:
            neighbors_a = self.get_neighbors_of(key)
            for key2 in self.mapping:
                iter_count += 1
                if iter_count % 1000 == 0:
                    print(str(iter_count/iter_total) + "% done.")
                if key2 == key:
                    continue

                neighbors_b = self.get_neighbors_of(key2)
                common_neighbors = set.intersection(set(neighbors_a), set(neighbors_b))

                index = key + '\t' + key2
                pref_atta[index] = len(neighbors_a) * len(neighbors_b)
                common_n[index] = len(common_neighbors)
                adamic_a[index] = 0
                for node in common_neighbors:
                    if len(self.get_neighbors_of(node)) > 1:
                        adamic_a[index] += 1/(math.log(len(self.get_neighbors_of(node))))

        sorted_x = sorted(common_n.items(), key=operator.itemgetter(1), reverse=True)
        with open('common_n.txt', 'w') as output_file:
            for k, v in sorted_x:
                output_file.write(k + '\t' + str(v) + '\n')

        sorted_x = sorted(pref_atta.items(), key=operator.itemgetter(1), reverse=True)
        with open('pref_atta.txt', 'w') as output_file:
            for k, v in sorted_x:
                output_file.write(k + '\t' + str(v) + '\n')

        sorted_x = sorted(adamic_a.items(), key=operator.itemgetter(1), reverse=True)
        with open('adamic_a.txt', 'w') as output_file:
            for k, v in sorted_x:
                output_file.write(k + '\t' + str(v) + '\n')


if __name__ == '__main__':
    g = Graph()
    g.load_from_json('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa.json')
    g.page_rank()
    g.more_metrics()

