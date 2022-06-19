# dijkstra's algorithm in Binary heap
from collections import defaultdict
import tkinter as tk
from os import path
from tkinter import *
import time

inf = float('inf')

root = Tk()

root.geometry("500x500")

root.resizable(False, False)

root.title("Dijkstra's algorithm")

canvas = tk.Canvas(root, height=500, width=500, bg="wheat")
canvas.pack()

graph_number = 0

def make_circle(center_x,center_y,r):
    canvas.create_oval(center_x-r,center_y-r,center_x+r,center_y+r,fill="white")

# (log N) for class Heap
class Heap():

    def __init__(self): #O(1)
        self.array = []
        self.size = 0
        self.pos = []

    def newMinHeapNode(self, v, dist): #O(1)
        minHeapNode = [v, dist]
        return minHeapNode

    # to swap two nodes of min heap I needed it in heapify
    def swapMinHeapNode(self, a, b): #O(1)
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t

    # Here I'm going to updates position of nodes when they are swapped
    # Position is needed for decreaseKey()
    def minHeapify(self, idx): # O(log N)
        smallest = idx
        left = 2*idx + 1
        right = 2*idx + 2

        if (left < self.size and self.array[left][1]< self.array[smallest][1]):
            smallest = left

        if (right < self.size and self.array[right][1] < self.array[smallest][1]):
            smallest = right


        if smallest != idx: # The nodes to be swapped in min heap if idx is not smallest

            # Swap positions
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest

            # Swap nodes
            self.swapMinHeapNode(smallest, idx)
            self.minHeapify(smallest)

    # to extract minimum node from heap
    def extractMin(self):  #O(log N)


        if self.isEmpty() == True:# Return NULL if heap is empty
            return


        root = self.array[0]     # Store the root node

        # Replace root node with last node (the leaf)
        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode

        # Update position of last node
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1

        # Reduce heap size and heapify root
        self.size -= 1
        self.minHeapify(0)

        return root

    def isEmpty(self):  #O(1)
        return True if self.size == 0 else False

    def decreaseKey(self, v, dist): #O(log N)


        i = self.pos[v] # Get the index of v in  heap array

        self.array[i][1] = dist   # Get the node and update its dist value

        # Travel up while the complete tree is
        # not hepified. This is a O(Logn) loop
        while (i > 0 and self.array[i][1] <
                  self.array[(i - 1) // 2][1]):

            # Swap this node with its parent
            self.pos[ self.array[i][0] ] = (i-1)//2
            self.pos[ self.array[(i-1)//2][0] ] = i
            self.swapMinHeapNode(i, (i - 1)//2 )

            # move to parent index
            i = (i - 1) // 2

    # to check if a given vertex 'v' is in min heap or not
    def isInMinHeap(self, v): #O(1)

        if self.pos[v] < self.size:
            return True
        return False

def printArr(dist, n):  #O(N)
    print ("Vertex\tDistance from source ")
    for i in range(n):
        print ("%d\t\t\t\t%d" % (i,dist[i]))

# O((E+V)log V) for class Graph
class Graph():

    def __init__(self, V): # O(1)
        self.V = len(V)
        self.vertices_positions = V
        self.graph = defaultdict(list)

        self.startTime = 0
        self.endTime = 0

        self.timetext = canvas.create_text(250,350,fill="darkblue",text="total time = 0")

    def draw_vertices(self):
        for i in range(self.V):

         #draw the vertice and its number
         make_circle(self.vertices_positions[i][0],self.vertices_positions[i][1],20)
         canvas.create_text(self.vertices_positions[i][0],self.vertices_positions[i][1],fill="black",text=str(i))


    # Adds an edge to an undirected graph
    def addEdge(self, src,dest,weight):  # O(1)

        # Add an edge from src to dest.The node is added at the beginning.
        newNode = [dest, weight]
        self.graph[src].insert(0, newNode)

        # Since graph is undirected, add an edge rom dest to src also
        newNode = [src, weight]
        self.graph[dest].insert(0, newNode)

        canvas.create_line(self.vertices_positions[src][0],self.vertices_positions[src][1],self.vertices_positions[dest][0],self.vertices_positions[dest][1],fill="white")
        canvas.create_text((self.vertices_positions[src][0]+self.vertices_positions[dest][0])/2,(self.vertices_positions[src][1]+self.vertices_positions[dest][1])/2+5,fill="darkblue",text=str(weight))


    # this function will calculates distances of shortest paths from src to all vertices.
    def dijkstra(self,src): # O(ELogV)
        self.startTime = time.time_ns()

        V = self.V  # Get the number of vertices in graph
        dist = []  # dist values used to pick minimum weight edge

        minHeap = Heap()  # minHeap represents set E

        # Initialize min heap with all vertices and dist value of all vertices
        V=int(V)
        for v in range(V):
            dist.append(1e7)
            minHeap.array.append( minHeap. newMinHeapNode(v, dist[v]))
            minHeap.pos.append(v)



        minHeap.pos[src] = src #dist value of src vertex 0 so that it is extracted first
        dist[src] = 0
        minHeap.decreaseKey(src, dist[src])


        minHeap.size = V # Initially size of min heap is equal to V

        # min heap contains all nodes whose shortest distance is not yet finalized.
        while minHeap.isEmpty() == False:  #O(V)


            newHeapNode = minHeap.extractMin() #Extract the vertex with minimum distance value
            u = newHeapNode[0]

            # Traverse through all neighbour vertices of u and update their distance values
            for pCrawl in self.graph[u]:  #O(V)

                v = pCrawl[0]

                # If shortest distance to v is not finalized yet, and distance
                # to v through u is less than its previously calculated distance
                # O(log V)  لانه قاعدين نغير القيمة
                if (minHeap.isInMinHeap(v) and
                     dist[u] != 1e7 and \
                   pCrawl[1] + dist[u] < dist[v]):
                        dist[v] = pCrawl[1] + dist[u]

                        minHeap.decreaseKey(v, dist[v]) #update distance value in min heap also

        self.endTime = time.time_ns()
        canvas.itemconfig(self.timetext, text="total time = {}".format(self.endTime-self.startTime))
        printArr(dist,V)


a_file = open("data.txt", "r")

list_of_graphs = []
list_of_graphs = a_file.read().split("-graph-")
list_of_graphs = list(filter(('').__ne__, list_of_graphs))


a_file.close()

def make_graph(graph_number):

 canvas.delete("all")

 print(graph_number)

 graph = list_of_graphs[graph_number]

 #getting vertices positions 
 vertices_positions_string = list(filter(('').__ne__, graph.split("-vertices_positions-")[1].split("\n")))
 vertices_positions = []
 for i in vertices_positions_string:
     ver = i.split(" ")
     vertices_positions.append([int(ver[0]),int(ver[1])])

 #adding the vertices positions 
 g = Graph(vertices_positions)

 #getting edge values 
 edge_values_string = list(filter(('').__ne__, graph.split("-graph_edges-")[1].split("\n")))

 for i in edge_values_string:
      edge = i.split(" ")

      #adding each edge values 
      g.addEdge(int(edge[0]), int(edge[1]), int(edge[2]))

 g.draw_vertices()

 solve = tk.Button(root,text="solve" , padx=-10, pady=-5,width=10, height=3, bg="rosybrown",command=lambda:g.dijkstra(0))
 solve.place(relx=0.3, rely=0.9, anchor=CENTER)

def next_graph():
    global graph_number
    graph_number += 1
    if(graph_number == len(list_of_graphs)):
        graph_number = 0
    make_graph(graph_number)

make_graph(graph_number)

next = tk.Button(root,text="next graph" , padx=-10, pady=-5,width=10, height=3, bg="rosybrown",command=lambda:next_graph())
next.place(relx=0.7, rely=0.9, anchor=CENTER)
root.mainloop()