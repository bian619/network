from math import log
import numpy as np
import networkx as nx
import copy
import matplotlib.pyplot as plt



G = nx.read_gml(r'C:\Users\吉祥如意\Desktop\全国数据\建网\zhongguo.gml',label='id')
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

def CN(G,v,u):
    if v in G:
        if u in G:
            if v!= u:
                x = list(G.neighbors(v))
                y = list(G.neighbors(u))
                res = [a for a in x if a in y]
            else:
                res = []
    return len(res)


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
def AUC(dict1,dict2):
    n1 = 0
    n2 = 0
    for i in dict1.values():
        for j in dict2.values():
            if i == j:
                n1+=1
            elif i > j:
                n2+=1
    n= len(dict1)*len(dict2)
    auc = (0.5*n1+n2)/n
    return auc


while len(S) <30:
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
                        efA = efA - CN(G, v,item) * efA / (Ek *(2 ** (l-1)))
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
    v1 = np.max(list_ef)
    #print(v1)
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
print(S)
#print(S2)
S1 = list(map(int,S2))
#print(len(S1))
ss0 = e(G)

G.remove_nodes_from(S1)
#print(G.number_of_nodes())
ss1 = e(G)

e = 1-ss1/ss0
#print(e)

'''liantong = []
for c in nx.connected_components(G):
    liantong.append(c)
print(len(liantong))
print(liantong)'''


'''color_map = []
for node in G:
    if node in S1:
        color_map.append('red')
    else:
        color_map.append('green')'''

'''pos = nx.random_layout(G)
nx.draw(G, pos=pos, with_labels=True, node_size=900, width=0.2, edge_color='g', node_color=color_map)
plt.show()'''
