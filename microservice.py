# RCCO, (C) Mahdi Dolati. License: AGPLv3
import numpy as np

from constants import Const


class LayerDownload:
    def __init__(self):
        self.download_data = dict()
        self.added_layers = set()
        self.canceled = False

    def add_data(self, t, l, r):
        if t not in self.download_data:
            self.download_data[t] = list()
        l.add_dl(t, r)
        self.download_data[t].append((r, l))

    def cancel_download(self):
        if not self.canceled:
            for t in self.download_data:
                for r, l in self.download_data[t]:
                    l.rm_dl(t, r)
            self.download_data = dict()
            self.canceled = True


class Vnf:
    def __init__(self, v_id=0, sharable_list=[], layer_cnt=[], layers=[], sharable_pr=[]):
        self.vnf_id = v_id
        self.cpu = np.random.uniform(*Const.VNF_CPU)
        self.ram = np.random.uniform(*Const.VNF_RAM)
        self.layers = dict()


class MicroService:
    def __init__(self, t, vnf):
        self.max_delay = np.random.randint(*Const.MS_DELAY)
        # print(self.max_delay)
        self.traffic_rate = np.random.randint(*Const.LAMBDA_RANGE)
        self.arrival_time = t
        self.vnf = vnf
        self.entry_point = None
        self.used_servers = set()
        self.T1 = range(self.arrival_time, self.tau1)
        self.T2 = range(self.tau1, self.tau2 + 1)
        self.layers = vnf.layers
    
    def __str__(self):
        a = [v.vnf_id for v in self.vnfs]
        return "entry_point: {} --> {}\n\tmax_delay: {}, t1-t2: {}-{}".format(self.entry_point, a, self.max_delay, self.tau1, self.tau2)

    def __repr__(self):
        return self.__str__()


class MSGenerator:
    # Micro Service Generator
    def __init__(self, my_net, orgs, sharable_pr=1.0):
        self.my_net = my_net
        self.layers = dict()
        layer_cnt = 0
        vnf_cnt = 0
        self.orgs = orgs
        self.org_vnfs = dict()
        self.vnf_num = Const.VNF_NUM
        for org in orgs:
            sharable_num = int(np.ceil(orgs[org] * Const.LAYER_NUM))
            sharable_list = list()
            for _ in range(sharable_num):
                sharable_list.append(layer_cnt)
                self.layers[layer_cnt] = np.random.randint(*Const.LAYER_SIZE)  # in megabytes
                layer_cnt += 1
            self.org_vnfs[org] = list()
            org_vnf_num = int(np.ceil(orgs[org] * Const.VNF_NUM))
            for i in range(org_vnf_num):
                a_vnf = Vnf(vnf_cnt, sharable_list, layer_cnt, self.layers, sharable_pr)
                vnf_cnt += 1
                self.org_vnfs[org].append(a_vnf)
                self.vnf = a_vnf
                for l_id in a_vnf.layers:
                    if l_id not in self.layers:
                        self.layers[l_id] = a_vnf.layers[l_id]
                        layer_cnt = layer_cnt + 1

    def get_chain(self, t):
        org_list = [oo for oo in self.orgs]
        org_pr = [self.orgs[oo] for oo in org_list]
        org = np.random.choice(org_list, p=org_pr)
        n = np.random.randint(*Const.SFC_LEN)
        vnfs = np.random.choice(self.org_vnfs[org], size=min(n, len(self.org_vnfs[org])), replace=False)
        new_sfc = MicroService(t, vnfs)
        return new_sfc

    def print(self):
        print("Layers: {}".format(self.layers))
        for vnf in self.vnfs_list:
            print("Vnf: {} -> {}".format(vnf.vnf_id, vnf.layers))
