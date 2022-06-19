# -*- coding: utf-8 -*-
"""
Created on Wed May  4 07:34:51 2022

@author: Mawadah
"""
# Kruskal's algorithm in Python

from os import path
from tkinter import *
import tkinter as tk
import time

from numpy import insert, place

inf = float('inf')

root = Tk()

root.geometry("500x500")

root.resizable(False, False)

root.title("Kruskal's algorithm")

canvas = tk.Canvas(root, height=500, width=500, bg="wheat")
canvas.pack()

graph_number = 0

def make_circle(center_x,center_y,r):
    canvas.create_oval(center_x-r,center_y-r,center_x+r,center_y+r,fill="white")



class Graph:
    def __init__(self, vertices):
        self.V = len(vertices)
        self.vertices_positions = vertices
        self.graph = []
        self.parent = [i for i in range(self.V)]

        self.startTime = 0
        self.endTime = 0

        self.timetext = canvas.create_text(250,350,fill="darkblue",text="total time = 0")
        self.costtext = canvas.create_text(250,400,text="Minimum cost = 0",fill="black")

        for i in range(self.V):
         self.graph.append([]) 
         for j in range(self.V): 
           self.graph[i].append(inf) 

    def draw_vertices(self):
        for i in range(self.V):

         #draw the vertice and its number
         make_circle(self.vertices_positions[i][0],self.vertices_positions[i][1],20)
         canvas.create_text(self.vertices_positions[i][0],self.vertices_positions[i][1],fill="black",text=str(i))

        
    def add_edge(self, u, v, w):
        self.graph[u][v] = w

        #draw the edge and its Weight
        canvas.create_line(self.vertices_positions[u][0],self.vertices_positions[u][1],self.vertices_positions[v][0],self.vertices_positions[v][1],fill="white")
        canvas.create_text((self.vertices_positions[u][0]+self.vertices_positions[v][0])/2,(self.vertices_positions[u][1]+self.vertices_positions[v][1])/2+5,fill="darkblue",text=str(w))

    def print(self):
        print(self.graph)
    
    def find(self,i):

     while self.parent[i] != i:

         i = self.parent[i]

     return i

    def union(self,i, j):

     a = self.find(i)

     b = self.find(j)

     self.parent[a] = b
 
    def kruskalMST(self):
     self.startTime = time.time_ns()
     mincost = 0 # Cost of min MST
 

    # Initialize sets of disjoint sets

     for i in range(self.V):

       self.parent[i] = i
 

    # Include minimum weight edges one by one 

     edge_count = 0

     while edge_count < self.V - 1:

        min = inf

        a = -1

        b = -1

        for i in range(self.V):

            for j in range(self.V):

                if self.find(i) != self.find(j) and self.graph[i][j] < min:

                    min = self.graph[i][j]

                    a = i

                    b = j

        self.union(a, b)
        canvas.create_line(self.vertices_positions[a][0],self.vertices_positions[a][1],self.vertices_positions[b][0],self.vertices_positions[b][1],fill="green")
        print("%d - %d: %d" % (a, b, min))

        edge_count += 1

        mincost += min
 
     self.endTime = time.time_ns()
     print("Minimum cost= {}".format(mincost))

     canvas.itemconfig(self.timetext, text="total time = {}".format(self.endTime-self.startTime))
     canvas.itemconfig(self.costtext, text="Minimum cost = {}".format(mincost))

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
      g.add_edge(int(edge[0]), int(edge[1]), int(edge[2]))

 g.draw_vertices()

 solve = tk.Button(root,text="solve" , padx=-10, pady=-5,width=10, height=3, bg="rosybrown",command=lambda:g.kruskalMST())
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