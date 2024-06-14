# Ehsan Akhavan
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import heapq
import random

from constants import Const
from sfc import LayerDownload
from q_learn import QLearn
from random import shuffle
from popularity_learn import PLearn

class Link:
    def __init__(self, tp, s, d):
        self.type = tp
        self.e1 = s
        self.e2 = d
        if self.e1.id[0] == "c" or self.e2.id[0] == "c":
            self.delay = 2000 * np.linalg.norm(self.e1.loc - self.e2.loc)
        else:
            self.delay = 10 * np.linalg.norm(self.e1.loc - self.e2.loc)
    
    def __str__(self):
        return "{},{},{}".format(self.type, self.e1.id, self.e2.id)

    def __repr__(self):
        return self.__str__()


class Node:
    def __init__(self, t, loc, id):
        self.id = id
        self.type = t
        self.loc = np.asarray(loc)
        self.sharing = True
        if self.type[0] == "b":
            self.cpu = 0
            self.ram = 0
            self.disk = 0
        elif self.type[0] == "e":
            self.cpu = Const.EDGE_CPU
            self.ram = Const.EDGE_RAM
            self.disk = Const.EDGE_DSK
        elif self.type[0] == "r":
            self.cpu = Const.REG_CPU
            self.ram = Const.REG_RAM
            self.disk = Const.REG_DSK
        else:
            self.cpu = np.infty
            self.ram = np.infty
            self.disk = np.infty
        self.layers = dict()
    
    def reset(self):
        self.layers = dict()


class NetGenerator:
    def __init__(self):
        self.g = nx.DiGraph()
        # bts_loc  = self.gen_rand_loc(Const.BTS_NUM)
        # edge_loc = self.gen_rand_loc(Const.EDGE_NUM)
        # reg_loc  = self.gen_rand_loc(Const.REG_NUM)
        self.bts_loc  = [(1,3),(3,2),(6,2),(2,7),(4,6),(6,4),(9,2),(4,9),(6,9),(9,7)]
        self.edge_loc = [(0,4),(4,1),(7,1),(4,4),(8,5),(5,9),(8,7)]
        self.reg_loc  = [(5,5)]
        self.cloud_loc = (50, 3)
        # generating all nodes
        for n in range(len(self.bts_loc)):
            n_id = "b{}".format(n)
            nd = Node("bts", self.bts_loc[n], n_id)
            self.g.add_node(n_id, nd=nd)
        for n in range(len(self.edge_loc)):
            n_id = "e{}".format(n)
            nd = Node("edge", self.edge_loc[n], n_id)
            self.g.add_node(n_id, nd=nd)
        for n in range(len(self.reg_loc)):
            n_id = "r{}".format(n)
            nd = Node("reg", self.reg_loc[n], n_id)
            self.g.add_node(n_id, nd=nd)
        n_id = "c"
        nd = Node("cloud", self.cloud_loc, n_id)
        self.g.add_node(n_id, nd=nd)
        # connect bts to edge
        for n in range(len(self.bts_loc)):
            e1 = "b{}".format(n)
            e2 = "e{}".format(self.get_closest(e1, self.edge_loc))
            self.connect_link(e1, e2)
        # connect edge to regional
        for n in range(len(self.edge_loc)):
            e1 = "e{}".format(n)
            e2 = "r{}".format(self.get_closest(e1, self.reg_loc))
            self.connect_link(e1, e2)
        # connect regional to cloud
        e1 = "c"
        e2 = "r{}".format(self.get_closest(e1, self.reg_loc))
        self.connect_link(e1, e2)

    def connect_link(self, e1, e2):
        li1 = Link("wired", self.g.nodes[e1]["nd"], self.g.nodes[e2]["nd"])
        li2 = Link("wired", self.g.nodes[e2]["nd"], self.g.nodes[e1]["nd"])
        self.g.add_edge(e1, e2, li=li1)
        self.g.add_edge(e2, e1, li=li2)

    def get_g(self):
        # fig, ax = plt.subplots()
        # x = []
        # y = []
        # for n in self.g.nodes():
        #     x.append(self.g.nodes[n]["nd"].loc[0])
        #     y.append(self.g.nodes[n]["nd"].loc[1])
        # ax.plot(x, y, '.b')
        # for n in self.g.nodes():
        #     ax.annotate(n, self.g.nodes[n]["nd"].loc)
        # for e in self.g.edges(data=True):
        #     line_t = 'r-'
        #     if self.g[e[0]][e[1]]["li"].type == "mmWave":
        #         line_t = 'b-'
        #     ax.plot([self.g.nodes[e[0]]["nd"].loc[0], self.g.nodes[e[1]]["nd"].loc[0]],
        #             [self.g.nodes[e[0]]["nd"].loc[1], self.g.nodes[e[1]]["nd"].loc[1]], line_t)
        # plt.show()
        return MyNetwork(self.g)

    def get_closest(self, n1, ns):
        ds = np.infty
        closest = None
        l1 = self.g.nodes[n1]["nd"].loc
        for n in range(len(ns)):
            l2 = ns[n]
            d = np.linalg.norm(l2 - l1)
            if closest is None or d < ds:
                ds = d
                closest = n
        return closest

    def gen_rand_loc(num):
        return [(random.randint(0, 10),random.randint(0, 10)) for _ in range(num)]
    
    # def generate_partition(total, parts):
    #     while True:
    #         partition = [random.randint(1, 3) for _ in range(parts)]
    #         if sum(partition) == total:
    #             return partition

    # def generate_groups(self):
    #     partition = self.generate_partition(10, 7)
    #     numbers = list(range(1, 11))
    #     random.shuffle(numbers)
        
    #     groups = []
    #     index = 0
    #     for size in partition:
    #         group = tuple(numbers[index:index + size])
    #         groups.append(group)
    #         index += size
        
    #     return groups