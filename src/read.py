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
        return e

    def generateGraphfromFile(self, koor, dataAdj, dictionary):
        self.koor = koor
        self.dict = dictionary

        for i in range(len(dataAdj)):
            for j in range(1,len(dataAdj[i])):
                index1 = self.getKey(dataAdj[i][0], self.dict)
                index2 = self.getKey(dataAdj[i][j], self.dict)
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
                dataAdj.append(line.split())
                
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

    # buat grafnya :DDD
    g = Graf(n)
    g.generateGraphfromFile(mapkoor,dataAdj,map)
    return g

    
# driver
directory = '..\\test\\'
namafile = input("Masukkan nama file : ")
g = readFile(directory+namafile)
print(g.getGraf(),"\n")
print(g.getDict(),"\n")