from math import log
import numpy as np
import networkx as nx
import copy
import matplotlib.pyplot as plt

#G = nx.read_gml(r'E:\complex network\数据集\astro-ph.gml',label='id')
#pos = nx.shell_layout(G)
#nx.draw(G, pos = pos, with_labels=True, node_size = 900, width = 0.2, edge_color = 'g')
#plt.show()
G = nx.read_gml(r'E:\complex network\数据集\netscience.gml',label='id')
degree = dict(nx.degree(G))
k123 = sum(degree.values())/len(G)
Ek = -log(1/k123)
pos = nx.shell_layout(G)
#nx.draw(G, pos = pos, with_labels=True, node_size = 900, width = 0.2, edge_color = 'g')
#plt.show()
K1 = [val for (node, val) in G.degree()]
K2 = [node for (node, val) in G.degree()]
V = G.nodes()
E =G.edges()
K= dict(zip(K2,K1))
S = []
S1 =[]
num =G.number_of_nodes()
H_123 = []
S2 = []
x=[]
S123 = []

def e(G):
    zhibiao = []
    N = G.number_of_nodes()
    for i in G:
        for j in G:
            if i==j:
                dij = 0
            else:
                if nx.has_path(G, source=i, target=j) == True:
                    d = nx.shortest_path_length(G, source=i, target=j)
                    dij = 1 / d
                    zhibiao.append(dij)
                else:
                    dij = 0
    ss0 = sum(zhibiao)
    ss1 = (1/(N*(N-1))) * ss0
    return ss1

def CC(G,v,u):
    kz2 = []
    kz1 = []
    if v in G:
        if u in G:
            if v!= u:
                x = list(G.neighbors(v))
                y = list(G.neighbors(u))
                res = [a for a in x if a in y]
                for a in res:
                    kz =  nx.clustering(G, a)
                    kz2.append(kz)
                for b in kz2:
                    kz3 = 1+b
                    kz1.append(kz3)
                CC= sum(kz1)
            else:
                CC = 0
    return CC


def p(u, v):
    he1 = []
    l = list(G.neighbors(v))
    for i in l:
        he1.append(K.get(i))
    he = sum(he1)
    p = K.get(u) / he
    return p


def H(u, v):
    H = -p(u, v) * log(p(u, v))
    return H


def get_key1(dct, value):
    return list(filter(lambda k: dct[k] == value, dct))


def newL(A, B):
    C = []
    for i in A:
        C.append(i)
    for j in B:
        if j not in C:
            C.append(j)
    return C

while len(S) < 0.01*num:
    list_ef = []
    list_v = []
    for v in V:
        H2 = []
        u = list(G.neighbors(v))
        for j in u:
            H1 = H(v, j)
            H2.append(H1)
        ef = sum(H2)
        if nx.clustering(G, v) == 1:
            efA = ef - nx.clustering(G, v) / K.get(v)
        else:
            efA = ef - nx.clustering(G, v)
        while len(H_123) == 0:
            list_ef.append(efA)
            list_v.append(v)
            break
        while len(H_123) >= 1:
            for item in H_123:
                if nx.has_path(G, source=v, target=item) == True:
                    l = nx.shortest_path_length(G, source=v, target=item)
                    if l <= 4:
                        efA = efA - CC(G, v,item) * efA / (Ek * 2 ** (l-1))
                        list_ef.append(copy.deepcopy(efA))
                        list_v.append(v)
                    else:
                        list_ef.append(copy.deepcopy(efA))
                        list_v.append(v)
                else:
                    list_ef.append(copy.deepcopy(efA))
                    list_v.append(v)
            break
    xy = dict(zip(list_v, list_ef))
    #print(sorted(xy.items(), key=lambda x: x[1], reverse=True))
    #print(list_ef)
    v1 = np.max(list_ef)
    v2 = get_key1(xy, v1)
    S123.append(copy.deepcopy(v1))
    for i in v2:
        x = []
        x.append(i)
        S.append(i)
    H_123 = x
    V = [item for item in V if item not in set(v2)]
    for i in v2:
        S2.append(i)
#print(S)
# print(S2)
S1 = list(map(int, S2))
# print(len(S1))
ss0 = e(G)

G.remove_nodes_from(S1)
# print(G.number_of_nodes())
ss1 = e(G)

e = 1 - ss1 / ss0
print(e)
