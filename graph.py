import json
import operator
from collections import OrderedDict

import numpy


class Graph:

    def __init__(self):
        self.matrix = None
        self.json_data = None
        self.mapping = OrderedDict()
        self.teleport_matrix = None

    def load_from_json(self, input_file='data.json'):
        data = []
        data_teleport = []

        with open(input_file) as data_file:
            self.json_data = json.load(data_file, object_pairs_hook=OrderedDict)
        i = 0
        for key in self.json_data:
            data.append([])
            data_teleport.append([])
            self.mapping[key] = i
            i += 1

        for key in self.json_data:
            for key2 in self.mapping:
                if key2 in self.json_data[key]['pointsTo']:
                    data[self.mapping[key]].append(1/len(self.json_data[key]['pointsTo']))
                else:
                    data[self.mapping[key]].append(0)
                data_teleport[self.mapping[key]].append(1)

        self.matrix = numpy.matrix(data)
        self.teleport_matrix = numpy.matrix(data_teleport)/len(data_teleport)

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


if __name__ == '__main__':
    g = Graph()
    g.load_from_json('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa.json')
    g.page_rank()
