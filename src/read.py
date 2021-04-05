# FORMAT FILE EKSTERNAL YANG DIBACA

# jumlah simpul
# nama simpul beserta koordinatnya
# matriks tetangga

'''
CONTOH
12 (jumlah simpul)
1 -6.884893 107.611445 (nama simpul - koordinat x - koordinat y)
2 -6.885191 107.613017
3 -6.885257 107.613733
4 -6.887256 107.611540
5 -6.887386 107.613611
6 -6.887910 107.608289
7 -6.893882 107.608450
8 -6.893230 107.610447
9 -6.893605 107.611944
10 -6.893780 107.613036
11 -6.894759 107.611723
12 -6.894883 107.608839
1 2 4 (matriks tetangga)
2 1 3 4
3 2 5
4 1 2 5 6
5 3 4 10
6 4 7
7 6 8 12
8 7 9
9 8 10 11
10 5 9
11 9 12
12 7 11

catatan :
1) bobot graf menyatakan jarak antar simpul (m atau km)
2) nilai heuristik yang dipakai adalah jarak garis lurus dari 1 titik ke tujuan

'''
import math
import networkx as nx
import os
#import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
#plt.switch_backend('agg')
# kelas graf
class Graf:
    def __init__(self, Nsimp):
        
        # menyimpan jumlah simpul
        self.Nsimp = Nsimp

        # menyimpan nama simpul sbg dictionary
        self.dict = {}

        # graf disimpan dalam bentuk dictionary
        self.graph = {}

        # menyimpan data koordinat setiap simpul
        self.koor = {}

        # menambahkan simpul dalam graf
        # inisialisasi array sebanyak Nsimp
        for i in range(Nsimp):
            self.graph[i] = []
    
    def getNSimpul(self):
        return self.Nsimp

    def getDict(self):
        return self.dict

    def getGraf(self):
        return self.graph
    
    def getKoor(self):
        return self.koor

    def add_edge(self, v1, v2, bobot):
        # diasumsikan simpul sudah terdapat dalam graf
        temp = [v2, bobot]
        if(temp not in self.graph[v1]):
            self.graph[v1].append(temp)

        temp1 = [v1, bobot]
        if(temp1 not in self.graph[v2]):
            self.graph[v2].append(temp1)

    def getKey(self, value, dictio):
        for key, val in dictio.items():
            if val == value:
                return key

        return "key doesn't exist"

    def euclideanDistance(self, index1, index2):
        # get x1 y1
        x1 = self.koor[index1][0]
        y1 = self.koor[index1][1]

        # get x2 y2
        x2 = self.koor[index2][0]
        y2 = self.koor[index2][1]

        e = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        return round(e,4)

    def generateGraphfromFile(self, koor, dataAdj, dictionary):
        self.koor = koor
        self.dict = dictionary

        for i in range(len(dataAdj)):
            for j in range(1,len(dataAdj[i])):
                index1 = dataAdj[i][0]
                index2 = dataAdj[i][j]
                # cari jarak antar 2 koordinat
                e = self.euclideanDistance(index1,index2)
                # menambahkan sisi antar 2 simpul
                self.add_edge(index1,index2,e)
    
# membaca file txt dan membuat graf berdasarkan file tsb dan mengembalikan objek graf
def readFile(x):
    datakoor = []
    dataAdj = []
    with open(x,'r') as f:
        # membaca baris pertama yang berisi n simpul
        n = int(f.readline())

        i=0
        track = 0
        for line in f:
            # membaca n baris selanjutnya
            # datakoor = [[namasimp1, x1, y1], 
            #             [namasimp2, x2, y2], 
            #             [dst]]
            if i in range(n):
                temp = line.split()
                temp1 = []
                temp1.append(temp[0])
                temp1.append(float(temp[1]))
                temp1.append(float(temp[2]))
                datakoor.append(temp1)

            # membaca n baris selanjutnya
            # dataAdj = [[namasimpul1, tetangganya, tetangganya, ...], 
            #            [namasimpul2, tetangganya, tetangganya, ...]
            #            [dst ... ]]
            if (n<=i<2*n):
                #dataAdj.append([float(x) for x in line.split()])
                tempAdj = []
                tempAdj.append(track) # uda work
                
                # cari tetangga
                tempRaw = line.split()
                for i in range(len(tempRaw)):
                    if(tempRaw[i]=="1"):
                        tempAdj.append(i)

                track = track + 1
                dataAdj.append(tempAdj)

            i = i+1

    # sudah work
    #print(n)
    #print(datakoor)
    #print(dataAdj)

    ### MENYIMPAN NAMA SIMPUL DENGAN DICTIONARY
    # membuat array angka yang merepresentasikan nama setiap simpul [0..n-1]
    key = [0 for i in range(n)]
    for i in range(n):
        key[i] = i

    # array menyimpan nama simpul dan koordinat
    koor = []
    namasimp = []
    for i in range(len(datakoor)):
        namasimp.append(datakoor[i][0])
        temp = (datakoor[i][1],datakoor[i][2])
        koor.append(temp)
    #print(namasimp)
    #print(koor)

    # membuat dictionary untuk nama simpul
    map = {}
    for nomor, nama in zip(key,namasimp):
        map[nomor] = nama
    #print(map)

    # membuat dictionary untuk koor simpul
    mapkoor = {}
    for nomor, xy in zip(key,koor):
        mapkoor[nomor] = xy
    #print(mapkoor)

    # buat grafnya
    g = Graf(n)
    g.generateGraphfromFile(mapkoor,dataAdj,map)
    return g

'''
def arrayOfCost(graph):
    costMat = []
    for i in range (12):
        costArr = []
        for j in range (len(g.getGraf())):
            costArr.append(graph.euclideanDistance(i,j))
        costMat.append(costArr)
    return costMat
'''

# visualisasi graf dengan networkx
def visualize(g):
    Gr = nx.Graph()

    # menambahkan simpul
    for i in range(g.getNSimpul()):
        Gr.add_node(g.getDict()[i], pos=g.getKoor()[i])

    # menambahkan sisi
    for i in range(g.getNSimpul()):
        temp = g.getGraf()[i]
        for j in range(len(temp)):
            src = g.getDict()[i]
            dest = g.getDict()[temp[j][0]]
            weighted = temp[j][1]
            Gr.add_edge(src, dest, weight=weighted )

    pos = nx.get_node_attributes(Gr,'pos')
    labels = nx.get_edge_attributes(Gr,'weight')
    nx.draw(Gr, pos,with_labels=True, font_weight='bold')
    nx.draw_networkx_edge_labels(Gr,pos,edge_labels=labels)
    plt.show()
    #plt.savefig('static/foo.png')
    #plt.clf()

def visualizePath(g, path):
    Gr = nx.Graph()
    path.pop()
    color_map=[]
    # menambahkan simpul
    for i in range(g.getNSimpul()):
        Gr.add_node(g.getDict()[i], pos=g.getKoor()[i])
        if i not in path:
            color_map.append('blue')
        else:
            color_map.append('red')
    
    # menambahkan sisi
    for i in range(g.getNSimpul()):
        temp = g.getGraf()[i]
        for j in range(len(temp)):
            src = g.getDict()[i]
            dest = g.getDict()[temp[j][0]]
            weighted = temp[j][1]
            if(i in path and temp[j][0] in path):
                Gr.add_edge(src, dest, color='r', weight=weighted)
            else:
                Gr.add_edge(src, dest, color='b', weight=weighted )
    
    edges = Gr.edges()
    colors = [Gr[u][v]['color'] for u,v in edges]
    print(colors)
    pos = nx.get_node_attributes(Gr,'pos')
    labels = nx.get_edge_attributes(Gr,'weight')
    nx.draw(Gr, pos, node_color=color_map, edge_color=colors, with_labels=True, font_weight='bold')
    nx.draw_networkx_edge_labels(Gr,pos,edge_labels=labels)
    plt.show()
    #plt.savefig('static/foo.png')
    #plt.clf()

def findBest(arr, open):
    best = open[0]
    for i in (open):
        if arr[i]<arr[best]:
            best = i
    return best

def findNeighbors(graph,curr):
    neighbors = []
    for i in (graph.getGraf()[curr]):
        neighbors.append(i[0])
    return neighbors

def displayPath(cameFrom,curr,cost):
    result = [curr]
    while cameFrom[curr] != -999:
        curr = cameFrom[curr]
        result.insert(0,curr)
    result.append(cost)
    return result

def AStar(graph,startNode,goalNode):
    toEvaluate = [startNode] # to be evaluated
    evaluated = [] # already evaluated
    # Total cost
    fcost = {}
    for i in range(len(g.getGraf())):
        fcost[i] = graph.euclideanDistance(i,goalNode)
    # Initialize cost
    gcost = [999] * len(g.getGraf()) # from start to current Node
    gcost[startNode] = 0
    # initialize array
    cameFrom = [-999] * len(g.getGraf())
    while(toEvaluate): # Not yet empty
        # Find the minimum
        currentNode = findBest(fcost,toEvaluate)
        if(currentNode==goalNode):
            # Found
            return(displayPath(cameFrom,currentNode,gcost[currentNode]))
        else:
            # remove from the list to be evaluated
            toEvaluate.remove(currentNode)
            evaluated.insert(0,currentNode)
            neighbors = findNeighbors(graph,currentNode)
            for neighbor in neighbors:
                if not (neighbor in evaluated): # not yet evaluated
                    if not (neighbor in toEvaluate): # no duplicates
                        toEvaluate.append(neighbor)
                    temporaryCost = gcost[currentNode] + graph.euclideanDistance(currentNode,neighbor) 
                    # finding a better path
                    if temporaryCost < gcost[neighbor]:
                        cameFrom[neighbor] = currentNode
                        gcost[neighbor] = temporaryCost
                        fcost[neighbor]=gcost[neighbor]+graph.euclideanDistance(neighbor,goalNode)
    return None

# driver
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
os.chdir('test')
#directory = '..\\test\\'
namafile = input("Masukkan nama file : ")
g = readFile(namafile)
print(g.getGraf(),"\n")
print(g.getDict(),"\n")
#print(arrayOfCost(g))
namaSimpul1 = int(input("Masukkan nama simpul pertama: "))
namaSimpul2 = int(input("Masukkan nama simpul kedua: "))
if(AStar(g,namaSimpul1,namaSimpul2)!=None):
    print(AStar(g,namaSimpul1,namaSimpul2))
else:
    print("No path")
# visualisasi graf mula2
visualizePath(g,AStar(g,namaSimpul1,namaSimpul2))