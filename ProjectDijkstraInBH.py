# -*- coding: utf-8 -*-
"""
Created on Sun 1:02:16 2022

@author: Alaa
"""

  
from collections import defaultdict
import sys
import random
import tkinter as tk
from os import path
from tkinter import *
import timeit

# start = timeit.default_timer()

# start the interface 
root = Tk()
root.geometry("500x500")
root.minsize(460,370)
root.maxsize(460, 370)
root.title("Dijkstra's algorithm")
canvas = tk.Canvas(root, height=500, width=500, bg="#2C2C2C")
canvas.pack()


fram2=tk.Frame(root, bg="#262626")
fram2.place(relx=0, rely=0)

#set the image 
img = PhotoImage(file="DikstraImage.png")   
label = Label(fram2, image = img)
label.pack()


#to get from a user number 
numberEntred=IntVar() 

label2 = tk.Label(root, text='START number :',fg="white", bg='#8C4A69')
label2.config(font=('helvetica', 10))
canvas.create_window(200, 100, window=label2)
label2.place(relx=0.5, rely=0.5, anchor=CENTER)
entry1 = tk.Entry(root, textvariable=numberEntred)
canvas.create_window(200, 140, window=entry1)
entry1.place(relx=0.5, rely=0.6, anchor=CENTER)



# (log N) for class Heap 
class Heap():
    def __init__(self):  #O(1)
        self.array = [] # to stote the data 
        self.size = 1
        self.pos = []
  
    def newHeap(self, v, dist):  #O(1)
        minHeapNode = [v, dist]
        return minHeapNode
  
    # to swap two nodes of min heap I needed it in heapify
    def swapMinHeapNode(self, a, b):  #O(1)
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t
  
  
    # Here I'm going to updates position of nodes when they are swapped
    # Position is needed for decreaseKey()
    def minHeapify(self, idx): # O(log N) 
        smallest = idx
        left = 2*idx    
        right = 2*idx +1
  
        if (left < self.size and self.array[left][1]< self.array[smallest][1]):
            smallest = left
  
        if (right < self.size and self.array[right][1] < self.array[smallest][1]):
            smallest = right
  
        if smallest != idx: # The nodes to be swapped in min heap if idx is not smallest
  
            # Swap positions
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest
  
            self.swapMinHeapNode(smallest, idx) # Swap nodes
            self.minHeapify(smallest)
  
    def isEmpty(self):   #O(1)
        return True if self.size == 0 else False
    

    
    # to extract minimum node from heap
    def extractMin(self):   #O(log N) 
        
        if self.isEmpty() == True:  # Return NULL if heap is empty
            return
        
        root = self.array[0] # Store the root node
  
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
  
    
    def decreaseKey(self, v, dist): #O(log N)
  
        i = self.pos[v]  # Get the index of v in  heap array
  
        self.array[i][1] = dist # Get the node and update its dist value
  
        # Travel up while the complete tree is
        # not hepified. This is a O(Logn) loop
        while (i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]):
  
            # Swap this node with its parent
            self.pos[ self.array[i][0] ] = (i-1)//2
            self.pos[ self.array[(i-1)//2][0] ] = i
            self.swapMinHeapNode(i, (i - 1)//2 )
  
            # move to parent index
            i = (i - 1) // 2;
  
    # to check if a given vertex 'v' is in min heap or not
    def isInMinHeap(self, v):  #O(1)
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
        self.V = V
        self.graph = defaultdict(list) # holds key value in pair
  
    
    # Adds an edge to an undirected graph using adjacency list
    def addEdge(self, src,dest,weight):  # O(1)
        
        # Add an edge from src to dest.The node is added at the beginning.  
        newNode = [dest, weight]
        self.graph[src].insert(0, newNode)
  
        # Since graph is undirected, add an edge rom dest to src also
        newNode = [src, weight]
        self.graph[dest].insert(0, newNode)
  
    
    # this function will calculates distances of shortest paths from src to all vertices. 
    def dijkstra(self,src): # O(ELogV) 
    
        V = self.V  # Get the number of vertices in graph
        dist = []   # dist values used to pick minimum weight edge                     
    
        minHeap = Heap()    # minHeap represents set E
        
        # Initialize min heap with all vertices and dist value of all vertices
        V=int(V)
        for v in range(V):  #O(V)
            dist.append(1e7)
            minHeap.array.append( minHeap.newHeap(v, dist[v]))
            minHeap.pos.append(v)
            
        
        minHeap.pos[src] = src #dist value of src vertex 0 so that it is extracted first
        dist[src] = 0
        minHeap.decreaseKey(src, dist[src])
        
       
        minHeap.size = V  # Initially size of min heap is equal to V


        # min heap contains all nodes whose shortest distance is not yet finalized.
        while minHeap.isEmpty() == False: #O(V)
        
            newHeapNode = minHeap.extractMin() #Extract the vertex with minimum distance value
            u = newHeapNode[0]
            
            # Traverse through all neighbour vertices of u and update their distance values 
            for neighbour in self.graph[u]:  #O(V)
                v = neighbour[0]
                
                # If shortest distance to v is not finalized yet, and distance 
                #to v through u is less than its previously calculated distance 
                #O(log V)  لانه قاعدين نغير القيمة
                if (minHeap.isInMinHeap(v)  and  neighbour[1] + dist[u] < dist[v]):
                        dist[v] = neighbour[1] + dist[u]
                        minHeap.decreaseKey(v, dist[v]) #update distance value in min heap also
            
        printArr(dist,V)
        
    def printNodes(self):#O(V)
           print("Vertex ")
           for node in range(self.V):
               print(node)
             
  
        
graph = Graph(9)  
def main():
    graph.addEdge(0, 1, 4)
    graph.addEdge(0, 7, 8)
    graph.addEdge(1, 2, 8)
    graph.addEdge(1, 7, 11)
    graph.addEdge(2, 3, 7)
    graph.addEdge(2, 8, 2)
    graph.addEdge(2, 5, 4)
    graph.addEdge(3, 4, 9)
    graph.addEdge(3, 5, 14)
    graph.addEdge(4, 5, 10)
    graph.addEdge(5, 6, 2)
    graph.addEdge(6, 7, 1)
    graph.addEdge(6, 8, 6)
    graph.addEdge(7, 8, 7)
    

    
    # graph.addEdge(0, 1, 4)
    # graph.addEdge(0, 2, 4)
    # graph.addEdge(1, 2, 2)
    # graph.addEdge(1, 0, 4)
    # graph.addEdge(2, 0, 4)
    # graph.addEdge(2, 1, 2)
    # graph.addEdge(2, 3, 3)
    # graph.addEdge(2, 5, 2)
    # graph.addEdge(2, 4, 4)
    # graph.addEdge(3, 2, 3)
    # graph.addEdge(3, 4, 3)
    # graph.addEdge(4, 2, 4)
    # graph.addEdge(4, 3, 3)
    # graph.addEdge(5, 2, 2)
    # graph.addEdge(5, 4, 3)
    
    num = numberEntred.get()
    
    nodes=[]
    for v in range(graph.V):
        nodes.append(v)
          
    if(num in nodes):
        graph.dijkstra(num)
    else:
        print("Wrong number,this number is not exit enter again")



        
show = tk.Button(root, text="show nodes", padx=-10, pady=-5, fg="white", 
                 bg="#168C8C", command=lambda:graph.printNodes())
show.place(relx=0.5, rely=0.3, anchor=CENTER)



def findShotest():
  
    find = tk.Button(root,text="Find", padx=-10, pady=-5, fg="white", 
                      bg="#168C8C", command=main)
    find.place(relx=0.5, rely=0.7, anchor=CENTER)
    
  
   
findShotest()
root.mainloop()

# stop = timeit.default_timer()
# print('Time: ', stop - start)      

